import requests as r
import data.url_list as urls

url = urls.url_list['item_details']

headers = {
    "Content-Type": "application/json",
    "User-Agent": "BlackDesert"
}
payload = {
  "keyType": 0,
  "mainKey": 12061,
  # "subKey": 3
}


response = r.request('POST',url,json = payload,headers = headers)


def item_info_cleanser(rsp,enhancement):
    rsp = rsp.split(':')
    rsp = rsp[2]
    rsp = rsp.split('|')
    rsp = rsp[enhancement]
    rsp = rsp.split('-')
    return rsp

print(item_info_cleanser(response.text,3))

class Api_Request:
    def __init__(self,headers={},payload = {}):
        self._headers = headers
        self._payload = payload