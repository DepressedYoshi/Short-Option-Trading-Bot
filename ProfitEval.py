class ShortProfitabilityEvaluation(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2023, 1, 1)
        self.SetEndDate(2023, 12, 31)
        self.SetCash(100000)
        
        self.AddUniverse(self.CoarseSelectionFunction, self.FineSelectionFunction)
        self.filtered_stocks = []

    def CoarseSelectionFunction(self, coarse):
        filtered = [x.Symbol for x in coarse if x.HasFundamentalData and x.Price > 15 and x.Option]
        return filtered

    def FineSelectionFunction(self, fine):
        fine = sorted(fine, key=lambda x: x.Price, reverse=True)
        return [x.Symbol for x in fine[:20]]

    def EvaluateStock(self, symbol):
        history = self.History(symbol, 60, Resolution.Daily)
        if history.empty:
            return 0
        
        recent_prices = history['close'][-5:]
        if (recent_prices[-1] / recent_prices[0] - 1) * 100 < 5:
            return 0
        
        long_term_trend = history['close'].pct_change().mean()
        short_term_increase = (recent_prices[-1] / recent_prices[0] - 1) * 100
        
        score = 0
        if long_term_trend < 0:
            score = 50 + short_term_increase
        else:
            score = 10 + short_term_increase

        # Add more technical indicators and scoring logic here
        return score

    def OnData(self, data):
        for symbol in self.filtered_stocks:
            score = self.EvaluateStock(symbol)
            if score >= 75:
                self.SetHoldings(symbol, -0.1)
