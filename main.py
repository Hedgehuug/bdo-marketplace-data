import json
import data
import data.context_manager as cm
import api_data.api_requests as api_requests
from analysis.analysis import Analysis as analysis


# Main file
if __name__ == "__main__":
    # Example URL, being used for development( it is currently for a sub-category fetch)
    example_url = 'https://eu-trade.naeu.playblackdesert.com/Trademarket/GetWorldMarketList'
    

    # Dev V2 will just focus on sending a proper API request to the website

    # Using the API interaction module, it fetches and returns a raw message from the endpoint
    raw_msg = json.loads((api_requests.Api_Request.sub_class_request(url=example_url,mainkey=1).content).content)['resultMsg']
    # Decodes the raw returned message into a processable data-type using the Analysis module
    decoded_msg = analysis.decode_msg(raw_msg)

    # Open reference file to translate IDs
    with cm.ContextManager('data/mp_reference.json') as file:
        use_file = json.loads(file.read())
    
        

    final_print = []
    for a in decoded_msg:
        # This sorts through all the item references in the json file and match them to the api returned data
        # by ID, and return both data in a tuple
        for item in use_file:
            if item[0] == a[0]:
                final_print.append((item,a[1:]))
        # I tried using filter, it did not work very well
        # final_print = final_print +(list(filter(lambda item: item if a[0] == item[0] else None,use_file)))
        print(final_print[-1])
        # final_print[-1] = (final_print[-1],a[1:])
        


    # This is what needs to be translated and then saved to a file
    #print(final_print)
    # Output:
    # (['732313', 'Blackstar Kyve'], ['18', '1667', '655000000'])

    # THIS SEGMENT IS GOING TO BE MOVED TO SAVE_DATA MODULE
    import datetime
    to_save_json = analysis.reformat_sub_group(final_print)
    to_save_json = json.dumps(to_save_json,indent=4)
    date_today = str(datetime.date.today())
    # change this so it loops through groups
    with open(f"data/group_1/daily/{date_today}.json","w") as file:
        file.write(to_save_json)






