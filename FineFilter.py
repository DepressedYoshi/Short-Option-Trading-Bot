class RefinedFilter(QCAlgorithm):
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

    def OnData(self, data):
        pass
