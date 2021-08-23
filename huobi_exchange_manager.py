from exchange_manager import ExchangeManager

class HuobiExchangeManager(ExchangeManager):
    def __init__(self,contracts):
        super.__init__(contracts)
        self.spot_book_ws = None
        self.fut_ws = None
        self.linswap_ws = None
        self.invswap_ws = None

    def init_orderbook(self,mindepth):
        if len(self.contracts[Contract.SPOT_TYPE]):
            c = self.contracts[Contract.SPOT_TYPE]
            self.spot_book_ws=HuobiSpotOrderbookWebSocket(c)

            depth = 20 # Change

            self.spot_book_ws.init_orderbook(depth)
        types = [Contract.FUT_TYPE,Contract.LINSWAP_TYPE,Contract.INVSWAP_TYPE]
        for t in types:
            if len(self.contracts[t]):
                # self.