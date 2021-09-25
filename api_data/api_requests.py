
import requests as r
import json
import datetime

use_headers = {
    "Content-Type": "application/json",
    "User-Agent": "BlackDesert",
    "cookie": "visid_incap_2504216=1c%2FH2VetS%2FeZihDG6z7E9QIIoWAAAAAAQUIPAAAAAAA6X8M83f1Phv%2BPRqqkMjF%2F; nlbi_2504216=w0WTY261IhfxWhLpoDFtLwAAAACqkRKdV1p2v7vzexYYoVQg; incap_ses_876_2504216=G054LgVtC39mlu5grS0oDAIIoWAAAAAAHal%2FMOTTzoq4I6krrEwXCQ%3D%3D"
}
example_url = 'https://eu-trade.naeu.playblackdesert.com/Trademarket/GetWorldMarketList'

# Class to create requests for the api
# I am going to remove this class system for now and just use regular functions
class Api_Request:
    def __init__(self,url,session,headers={},payload = {}):
        self._headers = headers
        self._payload = payload
        self._url = url
        self._session = session
        self.content = self.send_request()


    def get_payload(self):
        return self._payload

    # Creates object for a group category items request
    @classmethod
    def sub_class_request(self,url,session,mainkey=1,subkey=1):
        return Api_Request(
            headers=use_headers,
            payload= {
                "keyType": 0,
                "mainCategory": mainkey,
                "subCategory": subkey,
            },
            url = url,
            session = session
        )
    # Redesigned for the new API specifications and using requests.session
    @staticmethod
    def sub_request(session, mainKey = 1, subKey = 1):
        return Api_Request.send_request(
            session = session,
            payload = {
                "keyType": 0,
                "mainCategory": mainKey,
                "subCategory": subKey,
            },
            url = example_url,
        )


    @staticmethod
    def send_request(session,url,payload):
        response = session.request('POST',url = url,json = payload,headers = session.headers)
        return response


if __name__ == "__main__":
    # This is for debugging, if you run the file this'll run
    """
    Dev V1:
    raw_msg = json.loads((Api_Request.sub_class_request(url=example_url,mainkey=20).content).content)['resultMsg']
    # Items in the api are returned separated by '|' so we split the request by that first
    raw_split_msg = str(raw_msg).split('|')
    mapped_msg = map(lambda item: item.split('-'),raw_split_msg)
    msg_ids = map(lambda item: item[0],mapped_msg)
    # print(list(mapped_msg))
    """

    """
    Dev V1:

    class ContextManager:
        def __init__(self,filename):
            self.file = open(filename)

        def __enter__(self):
            return self.file

        def __exit__(self, type, value, traceback):
            self.file.close()

    # This here is a successful implementation of looping through 2 lists to find the matching items
    def look_through_msg(msg):
        use_msg = msg_ids
        for item in msg:
            if item in use_msg:
                print(msg)"""

    """
    Dev v1:
    with ContextManager('../data/mp_reference.json') as file:
        use_file = file.read()
        # map_item = list(mapped_msg)[0]
    list_msg = list(mapped_msg)
    """
    
    """
    Dev V1:
    final_print = []   
    for a in list_msg:
        if [''] in a:
            print('bullshit')
        # This sorts through all the item references in the json file and match them to the api returned data
        # by ID, and return both data in a tuple
        final_print = final_print + list(filter(lambda item: item if a[0] == item[0] else None,json.loads(use_file)))
        final_print[-1] = (final_print[-1],a[1:])
        
    file_ids = map(lambda item: item[0],json.loads(use_file))
    print(final_print)
        """
        


    
