from contracts import Contract
import websocket
import copy


class ExchangeWebSocket:
    
    # Public
    def __init__(self, contracts):
        self.contracts = [(c,self.contract_symbol(c)) for c in contracts]
        self.symbol_to_contract = {s:c for c,s in self.contracts}

        self.ws = None
        self.thread = None
        self.url = self.initialize_url()

    def connect(self):
        self.ws = websocket.WebSocketApp(self.url,
                                         on_message=self.on_message,
                                         on_open=self.on_open,
                                         on_close=self.on_close,
                                         on_error=self.on_error)
        self.thread = threading.Thread(target=self.ws.run_forever(),
                                       daemon=True)
        self.thread.start()
    
    # Internal
    def send_message(self, msg):
        pass
    def initialize_url(self):
        return ""

    def close(self):
        raise NotImplementedError
    def on_error(self,ws,msg):
        pass
    def on_open(self, ws):
        pass
    def on_close(self,ws,a,b):
        pass
    def on_message(self,ws,msg):
        pass