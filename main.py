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
    # Dev V3 will focus on the group search and saving methods, and making sure everything runs just right

    # Using the API interaction module, it fetches and returns a raw message from the endpoint
    # Decodes the raw returned message into a processable data-type using the Analysis module

    # Open reference file to translate IDs
    with cm.ContextManager('data/mp_reference.json') as file:
        use_file = json.loads(file.read())
    
        
    # List of item-groups as they are organised in bdo-mp
    # TO BE MOVED TO ITS OWN FILE
    group_list = [(1,"Main Weapons"),(5,"Sub Weapons"),(10,"Awakening Weapons"),(15,"Armors"),(20,"Accessories"),(25,"Materials"),(30,"Enchancements/Upgrades"),(35,"Consumables"),(40,"Life Tools"),(45,"Alchemy Stones"),(50,"Crystals"),(65,"Mount"),(70,"Ship"),(75,"Wagon"),(80,"Furniture")]

    for i in group_list:
        # Step 1: (fetches the info from the mp for the currently selected group, selecting the group with the value from "group_list")
        raw_msg = json.loads((api_requests.Api_Request.sub_class_request(url=example_url,mainkey=i[0]).content).content)['resultMsg']
        # Step 2: (decodes the message and converts it to usable data)
        decoded_msg = analysis.decode_msg(raw_msg)
        # This is how you find the index of a value in a list

        final_print = []
        for a in decoded_msg:
            # This sorts through all the item references in the json file and match them to the api returned data
            # by ID, and return both data in a tuple
            for item in use_file:
                if item[0] == a[0]:
                    final_print.append((item,a[1:]))
        # THIS SEGMENT IS GOING TO BE MOVED TO SAVE_DATA MODULE
        import datetime
        to_save_json = analysis.reformat_sub_group(final_print)
        to_save_json = json.dumps(to_save_json,indent=4)
        date_today = str(datetime.date.today())
        folder_index = group_list.index(i)+1
        with open(f"data/group_{folder_index}/daily/{date_today}.json","w") as file:
            file.write(to_save_json)

        progress_percent = (group_list.index(i) / (len(group_list))) * 100
        print(f"Completion: {progress_percent}% - {i[1]} complete", end='\r')
        # print(f"group {i[1]} is complete")








