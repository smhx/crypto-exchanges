from exchange_websocket import ExchangeWebSocket
from orderbook import OrderBook
from bbo import BBO

class HuobiWebsocket(ExchangeWebSocket):
    # def subscribe_bbo(self):
    #     self.bbo = {c: BBO() for c,_ in self.contracts}
    #     for c,s in self.contracts:
    #         s=self.contract_symbol(c)
    #         channel=f"market.{s}.bbo"
    #         self.subscribe(channel)            

    # depth can be 20 or 150
    # def subscribe_orderbook(self, depth):
    #     for c,s in contracts:
    #         s=self.contract_symbol(c)
    #         channel=f"market.{s}.depth.size_{depth}.high_freq"
    #         id = f"orderbook.{c}"
    #         data_type="incremental" # or 'snapshot'
    #         self.subscribe(channel,id,data_type)

    def subscribe(self, channel, id='default_sub_id',data_type=None):
        request = {'sub':channel,'id':id}
        if data_type:
            request['data_type'] = data_type
        self.send_message(request)

    def request(self, channel, id='default_req_id'):
        request = {'req': channel, 'id':id}
        self.send_message(request)

    def on_message(self, ws, m):
        self.decrypt(m)
        if 'ping' in m:
            self.handle_ping(m['ping'])
        elif 'subbed' in m:
            channel = m['subbed'].split('.')
            res_ts=m['ts']
            status=m['status']
            id=m['id'] if 'id' in m else None
            self.handle_subscribed(channel,res_ts,status,id)
        elif 'unsubbed' in m:
            channel = m['unsubbed'].split('.')
            res_ts=m['ts']
            status=m['status']
            id=m['id'] if 'id' in m else None
            self.handle_unsubscribed(channel,res_ts,status,id)
        elif 'ch' in m:
            res_ts = m['ts'] if 'ts' in m else None
            channel = m['ch'].split('.')
            tick = m['tick']
            contract = self.symbol_to_contract[channel[1]]
            self.handle_update(contract,channel,tick,res_ts)
        elif 'rep' in m:
            channel = m['rep'].split('.')
            id = m['id'] if 'id' in m else None
            status = m['status']
            data = m['data']
            contract = self.symbol_to_contract[channel[1]]
            self.handle_request(contract,channel,data,reponse_ts,id,status)

    def handle_ping(self,ping):
        self.send_message({'pong':ping})
    def handle_subscribed(self,channel,res_ts,status,id):
        pass
    def handle_unsubscribed(self,channel,res_ts,status,id):
        pass
    def handle_update(self,contract,channel,tick,res_ts):
        pass
    def handle_request(channel,contract,data,res_ts,id,status):
        pass