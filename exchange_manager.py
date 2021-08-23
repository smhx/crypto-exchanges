class ExchangeManager:
    def __init__(self, contracts):
        self.contracts=[list() for _ in range(Contract.NUM_TYPES)]
        for c in contracts:
            self.contracts[c.type].append(c)
    def init_orderbook(self,mindepth):
        pass
    def init_bbo(self):
        pass
    def init_fundrate(self):
        pass
    def get_orderbooks(self):
        pass
    def get_bbo(self):
        pass