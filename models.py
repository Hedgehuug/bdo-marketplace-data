import requests as r
import data.url_list as urls
import json

url = urls.url_list['item_details']
url_2 = urls.url_list['category_list']

headers = {
    "Content-Type": "application/json",
    "User-Agent": "BlackDesert"
}
payload = {
  "keyType": 0,
  "mainKey": 12061,
  # "subKey": 3
}
payload_variety = {
  "keyType": 0,
  "mainKey": 20,
  # "subKey": 3
}


response = r.request('POST',url_2,json = payload,headers = headers)
dict_response = json.loads(response.content)['resultMsg']


def item_info_cleanser(rsp,enhancement):
    rsp = rsp.split('|')
    rsp = rsp[enhancement]
    rsp = rsp.split('-')
    return rsp

#print(item_info_cleanser(dict_response,3))




# Request_info is made to fetch info from saved data, this'll be the primary access point to the data
class Request_info:
    def __init__(
        self,
        group=None,
        item_id=None,
        fetched_data=None,
        method=None
        ):
        self._group = group
        self._item_id = item_id
        self._fetched_data = fetched_data
        self._method = method

    # Using get_item_by_id, you fetch information of enter ID's item
    @classmethod
    def get_item_by_id(self,id):
        return Request_info(item_id=id,group=123,method="item by id")

    def __repr__(self):
        return f"Request Type: {self._method}"

                

# print(Request_info.get_item_by_id(12061))


# Create a file for each of the item categories with all their data saved in there



