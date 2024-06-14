class PortfolioManagement(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2023, 1, 1)
        self.SetEndDate(2023, 12, 31)
        self.SetCash(100000)
        
        self.targets = []
        self.stop_loss_percent = 0.1
        self.take_profit_percent = 0.2

    def ManagePortfolio(self):
        for holding in self.Portfolio.Values:
            if holding.Invested:
                if holding.Price <= holding.AveragePrice * (1 - self.stop_loss_percent):
                    self.Liquidate(holding.Symbol)
                    self.Log(f"Stop loss triggered for {holding.Symbol}")
                elif holding.Price >= holding.AveragePrice * (1 + self.take_profit_percent):
                    self.Liquidate(holding.Symbol)
                    self.Log(f"Take profit triggered for {holding.Symbol}")

    def OnData(self, data):
        self.ManagePortfolio()
