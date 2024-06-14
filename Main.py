class MasterAlgorithm(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2023, 1, 1)
        self.SetEndDate(2023, 12, 31)
        self.SetCash(100000)
        
        self.rough_filter = RoughFilter()
        self.refined_filter = RefinedFilter()
        self.trade_evaluation = ShortProfitabilityEvaluation()
        self.trade_execution = TradeExecution()
        self.portfolio_management = PortfolioManagement()

    def OnData(self, data):
        self.portfolio_management.OnData(data)
        self.trade_evaluation.OnData(data)
        self.trade_execution.OnData(data)

    def CoarseSelectionFunction(self, coarse):
        return self.rough_filter.CoarseSelectionFunction(coarse)

    def FineSelectionFunction(self, fine):
        return self.refined_filter.FineSelectionFunction(fine)
