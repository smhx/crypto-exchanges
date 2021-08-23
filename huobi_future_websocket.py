class HuobiFutureWebsocket(HuobiWebsocket):

    def initialize_url(self):
        if self.contract_type == Contract.FUTURE_TYPE:
            return "wss://api.hbdm.com/ws"
        elif self.contract_type == Contract.INVPERP_TYPE:
            return "wss://api.hbdm.com/swap-ws"
        elif self.contract_type==Contract.PERP_TYPE:
            return "wss://api.hbdm.com/linear-swap-ws"
        raise

    def __init__(self, contract, contract_type):
        self.contract_type = contract_type
        super.__init__(self,contract)
        self.track_orderbook = False
        self.track_bbo = False

    def init_bbo(self,depth):
        self.track_bbo = True
        self.bbo = {c:BBO() for c,_ in self.contracts}

    # depth can be 20 or 150
    def init_orderbook(self, depth):
        self.track_orderbook = True
        self.orderbook_depth = depth
        self.orderbook = {c:OrderBook() for c,_ in self.contracts}

    def handle_update(self,c,channel,tick,res_ts):
        if channel[2] == 'depth':
            depth = int(channel[-1])
            seqnum=tick['seqNum']
            prev_seqnum=tick['prevSeqNum']
            bids = tick['bids'] if 'bids' in tick else []
            asks = tick['asks'] if 'asks' in tick else []
            if tick['event']=='snapshot':
                self.orderbook[c].snapshot(bids,asks,res_ts)
            else: # tick['event']=='update'
                self.orderbook[c].update(bids,asks,res_ts)
        elif channel[-1]=='bbo':
            [b,bsz] = tick['bid']
            [a,asz] = tick['ask']
            self.bbo[c].set_bid(b,res_ts)
            self.bbo[c].set_bidsize(bsz,res_ts)
            self.bbo[c].set_ask(a,res_ts)
            self.bbo[c].set_asksize(asz,res_ts)

    def subscribe_orderbook(self):
        for _,s in self.contracts:
            channel = "market.{s}.depth.size_{self.orderbook_depth}.high_freq"
            self.subscribe(channel,"incremental")

    def subscribe_bbo(self):
        for _,s in self.contracts:
            channel="market.{s}.bbo"
            self.subscribe(channel)
    
    def on_open(self,ws):
        if self.track_bbo:
            self.subscribe_bbo()
        if self.track_orderbook:
            self.subscribe_orderbook()