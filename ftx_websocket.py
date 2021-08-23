from exchange_websocket import ExchangeWebSocket

class FtxWebSocket(ExchangeWebSocket):
    def initialize_url(self):
        return "wss://ftx.com/ws/"

    def on_message(self, m):
        channel = m['channel']
        market = m['market']
        type = m['type']
        code = m['code'] if 'code' in m else None
        msg = m['msg'] if 'msg' in m else None
        data = m['data'] if 'data' in m else None
        # https://docs.ftx.com/?python#response-format
        if type == 'error':
            self.handle_error(channel, market, code, msg)
        elif type == 'subscribed':
            self.handle_subscribed(channel,market)
        elif type == 'unsubscribed':
            self.handle_unsubscribed(channel,market)
        elif type == 'info':
            self.handle_info(channel,market,code,msg)
        else:
            # type == 'partial' or 'update'
            self.handle_data(channel, market, data, type)
    def handle_message(self, channel, market, type, code, msg, data):
        if type == 'error':
