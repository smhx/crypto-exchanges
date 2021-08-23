from huobi_websocket import HuobiWebsocket

class HuobiSpotBookKeeper:

    def __init__(self, orderbook, contract, huobi_ws):
        self.book = orderbook
        self.huobi = huobi_ws
        self.contract = contract
        self.wait = 10 # constant

        self.reset()

    def reset(self):
        self.num_requests = 0
        self.last_seqnum = 0
        self.state = 0
        self.snapshot_seqnum = 0
        self.cache = [] # [seqnum,prev_seqnum,bids,asks,ts]
        self.book.reset()

    def take_snapshot(self):
        self.huobi.request_snapshot(self.contract)

    def set_snapshot(self,seqnum,bids,asks,ts=0):
        self.snapshot_seqnum = seqnum
        self.book.snapshot(bids,asks,ts)

    def update_book(self,seqnum,prev_seqnum,bids,asks,ts):
        if self.last_seqnum != 0 and self.last_seqnum != prev_seqnum:
            self.reset()
            return
        self.last_seqnum = seqnum
        if self.state == 0:
            if len(self.cache) == 0 or self.cache[0][1] > self.snapshot_seqnum:
                self.cache.append([seqnum,prev_seqnum,bids,asks,ts])
                self.num_requests += 1
                if self.num_requests == self.wait:
                    self.take_snapshot()
            elif len(self.cache)>0 and self.cache[-1][0] < self.snapshot_seqnum:
                self.cache = []
            else:
                for [s,ps,b,a,t] in self.cache:
                    if s>self.snapshot_seqnum:
                        self.book.update(b,a,t)

# State 0 means listen to updates and push to a cache
# If snapshot_seqnum < min(prev_seqnum), wait for prelim_msgs
# number of updates and then do another snapshot
# If snapshot > max(seqnum), delete cache and wait
# Else, should have snapshot == prev_seqnum of something.
# If at any point, prev_seqnum doesn't match with our last seqnum,
# go to state 0

# https://huobiapi.github.io/docs/spot/v1/en/#market-by-price-incremental-update
class HuobiSpotOrderbookWebSocket(HuobiWebSocket):

    def __init__(self,contracts):
        super.__init__(self, contracts)
        self.track_orderbook = False

    def init_orderbook(self,depth):
        self.track_orderbook = True

        self.orderbook_depth = depth
        self.orderbook = {c:OrderBook() for c,_ in self.contracts}
        self.book_keeper = {c:HuobiSpotBookKeeper(self,self.orderbook[c],c) for c,_ in self.contracts}

    def initialize_url(self):
        return "wss://api.huobi.pro/feed"

    def request_snapshot(self,c):
        s = self.contract_symbol(c)
        self.request(f"market.{s}.mbp.{self.depth}")

    def subscribe_orderbook(self):
        if self.
        for _,s in self.contracts:
            self.subscribe(f"market.{s}.mbp.{self.depth}")

    def handle_update(self,c,channel,tick,res_ts):
        if channel[-2] == 'mbp':
            depth=int(channel[-1])
            seqnum=tick['seqNum']
            prev_seqnum=tick['prevSeqNum']
            bids = tick['bids'] if 'bids' in tick else []
            asks = tick['asks'] if 'asks' in tick else []
            self.book_keeper[c].update_book(seqnum,prev_seqnum,bids,asks,res_ts)

    def handle_request(self,contract,channel,data,ts,id,status):
        if status != "ok":
            return
        if channel[-2]=='mbp':
            seqnum=data['seqNum']
            bids = data['bids'] if 'bids' in data else []
            asks = data['asks'] if 'asks' in data else []
            self.book_keeper[contract].set_snapshot(seqnum,bids,asks)

    def on_open(self,ws):
        if self.track_orderbook:
            self.subscribe_orderbook()