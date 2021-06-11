import json
import data
import api_data.api_requests as api_requests
from analysis.analysis import Analysis as analysis


# Main file
if __name__ == "__main__":
    # Example URL, being used for development( it is currently for a sub-category fetch)
    example_url = 'https://eu-trade.naeu.playblackdesert.com/Trademarket/GetWorldMarketList'
    

    # Dev V2 will just focus on sending a proper API request to the website

    raw_msg = json.loads((api_requests.Api_Request.sub_class_request(url=example_url,mainkey=1).content).content)['resultMsg']

    decoded_msg = analysis.decode_msg(raw_msg)
    print(decoded_msg)