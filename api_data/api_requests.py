
import requests as r
import json

use_headers = {
    "Content-Type": "application/json",
    "User-Agent": "BlackDesert"
}
example_url = 'https://eu-trade.naeu.playblackdesert.com/Trademarket/GetWorldMarketList'

# Class to create requests for the api
class Api_Request:
    def __init__(self,url,headers={},payload = {}):
        self._headers = headers
        self._payload = payload
        self._url = url
        self.content = self.send_request()


    def get_payload(self):
        return self._payload

    # Creates object for a group category items request
    @classmethod
    def sub_class_request(self,url,mainkey=1):
        return Api_Request(
            headers=use_headers,
            payload= {
                "keyType": 0,
                "mainCategory": mainkey,
            },
            url = url
        )

    def send_request(self):
        response = r.request('POST',url = self._url,json = self._payload,headers = self._headers)
        return response

if __name__ == "__main__":
    # This is for debugging, if you run the file this'll run
    raw_msg = json.loads((Api_Request.sub_class_request(url=example_url,mainkey=20).content).content)['resultMsg']
    # Items in the api are returned separated by '|' so we split the request by that first
    raw_split_msg = str(raw_msg).split('|')
    mapped_msg = map(lambda item: item.split('-'),raw_split_msg)
    msg_ids = map(lambda item: item[0],mapped_msg)
    # print(list(mapped_msg))

    class ContextManager:
        def __init__(self,filename):
            self.file = open(filename)

        def __enter__(self):
            return self.file

        def __exit__(self, type, value, traceback):
            self.file.close()

    def look_through_msg(msg):
        use_msg = msg_ids
        for item in msg:
            if item in use_msg:
                print(msg)

    
    with ContextManager('../data/mp_reference.json') as file:
        use_file = file.read()
        map_item = list(mapped_msg)[0]
        def filter_price(item):
            conditional = bool(item[0] == map_item[0])
            return item if conditional else None
                
        final_print = filter(filter_price,json.loads(use_file))
        file_ids = map(lambda item: item[0],json.loads(use_file))
        print(list(final_print))
        


    
