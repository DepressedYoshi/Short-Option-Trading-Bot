class TradeExecution(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2023, 1, 1)
        self.SetEndDate(2023, 12, 31)
        self.SetCash(100000)
        
        self.filtered_stocks = []
        self.targets = []

    def ExecuteTrade(self, symbol, quantity):
        self.SetHoldings(symbol, -quantity)
        self.targets.append(symbol)
        self.Log(f"Executing trade for {symbol}: Short {quantity}")

    def OnData(self, data):
        for symbol in self.filtered_stocks:
            score = self.EvaluateStock(symbol)
            if score >= 75:
                self.ExecuteTrade(symbol, 0.1)
