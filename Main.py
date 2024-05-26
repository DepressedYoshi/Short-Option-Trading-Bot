from AlgorithmImports import *

class ShortOptionTradingBot(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2015, 1, 1)    # Set Start Date
        self.SetEndDate(2019, 1, 1)      # Set End Date
        self.SetCash(100000)             # Set Strategy Cash
        self.UniverseSettings.Resolution = Resolution.Daily
        
        self.AddUniverse(self.CoarseSelectionFunction, self.FineSelectionFunction)
        
        self.max_positions = 10
        self.cash_reserve = 0.2
        self.stop_loss_pct = 0.2
        self.pending_orders = []
        
        # Technical indicators
        self.indicators = {}

    def CoarseSelectionFunction(self, coarse):
        filtered = [x for x in coarse if x.Price > 15 and x.HasOptions]
        return [x.Symbol for x in filtered]
    
    def FineSelectionFunction(self, fine):
        filtered = sorted(fine, key=lambda x: (x.Price - x.PrevPrice) / x.PrevPrice, reverse=True)
        selected = [x.Symbol for x in filtered[:20] if (x.Price - x.PrevPrice) / x.PrevPrice > 0.05]
        return selected
    
    def OnData(self, data):
        self.ManagePortfolio(data)
        if self.Time.day == 1 and self.Time.weekday() == 0:  # Bi-weekly on Mondays
            self.EvaluateTrades()
        
    def EvaluateTrades(self):
        for symbol in self.ActiveSecurities.Keys:
            score = self.EvaluateTrade(symbol)
            if score >= 75:
                self.ExecuteTrade(symbol, score)
    
    def EvaluateTrade(self, symbol):
        security = self.Securities[symbol]
        score = 0
        
        # Mid to long term downtrend check
        history = self.History(symbol, 90, Resolution.Daily)
        if not history.empty:
            recent_price = history['close'].values[-1]
            old_price = history['close'].values[0]
            if recent_price < old_price:
                increase_pct = (security.Price - recent_price) / recent_price
                score = 50 + min(max(increase_pct * 100, 0), 20)
        
        # Technical indicators
        score += self.CheckTechnicalIndicators(security)
        
        # Financial report check
        if self.Time.date() in [r.AsOf.date() for r in security.Fundamentals.FinancialStatements]:
            score -= 7
        
        return score
    
    def CheckTechnicalIndicators(self, security):
        symbol = security.Symbol
        if symbol not in self.indicators:
            self.indicators[symbol] = {
                "RSI12": self.RSI(symbol, 12, Resolution.Daily),
                "RSI20": self.RSI(symbol, 20, Resolution.Daily),
                "RSI24": self.RSI(symbol, 24, Resolution.Daily),
                "MA50": self.SMA(symbol, 50, Resolution.Daily),
                "MA200": self.SMA(symbol, 200, Resolution.Daily)
                # Add other indicators here
            }
        
        score = 0
        indicators = self.indicators[symbol]
        
        for name, indicator in indicators.items():
            if not indicator.IsReady:
                continue
            
            value = indicator.Current.Value
            if "RSI" in name:
                if value < 30:
                    score += 1
                elif value > 70:
                    score += 5
                else:
                    score += 3
            elif "MA" in name:
                if name == "MA50" and value > security.Price:
                    score += 2
                elif name == "MA200" and value > security.Price:
                    score += 2
        
        return score

    def ExecuteTrade(self, symbol, score):
        option_chain = self.OptionChainProvider.GetOptionContractList(symbol, self.Time)
        if option_chain:
            # Filter for puts
            puts = [x for x in option_chain if x.Right == OptionRight.Put]
            if not puts:
                return
            
            # Select the contract with the nearest expiry date that's still out of the money
            puts = sorted(puts, key=lambda x: (x.Expiry, x.Strike))
            contract = next((put for put in puts if put.Strike < self.Securities[symbol].Price), None)
            
            if contract and self.Portfolio[symbol].Quantity == 0:
                # Calculate the number of contracts to short
                quantity = int((self.Portfolio.TotalPortfolioValue * 0.1) / contract.Price)
                self.MarketOrder(contract.Symbol, -quantity)
                self.pending_orders.append(contract.Symbol)
                self.Debug(f"Shorted {quantity} contracts of {contract.Symbol} at {contract.Price}")
                
    def ManagePortfolio(self, data):
        for symbol in list(self.pending_orders):
            if symbol in data and data[symbol].Price < data[symbol].Price * (1 - self.stop_loss_pct):
                self.Liquidate(symbol)
                self.pending_orders.remove(symbol)
                self.Debug(f"Liquidated {symbol} due to stop loss")
