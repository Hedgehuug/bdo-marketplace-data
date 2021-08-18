import json
import datetime
import os
import data.context_manager as cm
import api_data.api_requests as api_requests
from analysis.analysis import Analysis as analysis
from data_access.data_access import Data_Access as data_access
import requests

date_today = datetime.date.today()
day_delta = datetime.timedelta(days=1)


# Going to repurpose this file to bunch up all the encompassing micro-services for the main loop


def fetch_and_store_data(url):
    work_url = 'https://eu-trade.naeu.playblackdesert.com/Trademarket/GetWorldMarketList'
    

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
    sub_lists = [17,15,22,6,4,8,2,8,10,4,7,13,9,6,9]
    with requests.Session() as session:
        for i in group_list:
            rawest_msg = (api_requests.Api_Request.sub_class_request(url=work_url,mainkey=i[0],subkey=1,session=session).content).content
            # Step 1: (fetches the info from the mp for the currently selected group, selecting the group with the value from "group_list")
            print(rawest_msg)
            raw_msg = json.loads((api_requests.Api_Request.sub_class_request(url=work_url,mainkey=i[0],session=session).content).content)['resultMsg']
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
            to_save_json = analysis.reformat_sub_group(final_print)
            to_save_json = json.dumps(to_save_json,indent=4)
            date_today = str(datetime.date.today())
            folder_index = group_list.index(i)+1
            with open(f"data/group_{folder_index}/daily/{date_today}.json","w") as file:
                file.write(to_save_json)

            # Progress bar
            progress_percent = ((group_list.index(i)+1) / (len(group_list))) * 100
            print(f"Completion: {progress_percent}% - {i[1]}", end='\r')




# This service(data_access_version) is for determining the type of access we want to the files, and how they get retrieved
class Data_Access_Version:
    def __init__(self,all_data,version=3,reference=[]):
        self._all_data = all_data
        self._version = version
        self._reference = reference

        if version == 1:
            self.version_1()
        elif version == 2:
            self.version_2()
        elif version == 3:
            self.version_3(self._all_data)
        else:
            print(f"incorrect version: {version}")

    # Search info 
    def version_1(self):
        input_name = input("Input part of searched item, it'll return all items with it in their name: ")

        returned_item_from_input = list(filter(lambda a: input_name in a[1],self._reference))
        # Prints out all the searched for items' past data
        for items in returned_item_from_input:
            try:
                print("------------------------")
                print(f"{self._all_data[items[0]]['name']}:")
                print(f"Stock: \n{self._all_data[items[0]]['stock']}")
                print(f"Stock Change: \n{self._all_data[items[0]]['stock_change']}")
                print(f"Volume: \n{self._all_data[items[0]]['volume']}")
                print(f"Volume Change: \n{self._all_data[items[0]]['volume_change']}")
                # ADD DAILY VOLUME RIGHT HERE, IT'LL BE WAY MORE USEFUL THAN TOTAL VOLUME
                print(f"Price: \n{self._all_data[items[0]]['price']}")
                print(f"Price Change: \n{self._all_data[items[0]]['price_change']}")
            except KeyError as err:
                print(f"Could not find information on {err}")
            except:
                print('Big problem')

        while True:
            restart_input = str(input("Search for another Item?(y/n): "))
            if restart_input == 'y':
                self.version_1()
                break
            if restart_input == 'n':
                break
            else:
                print(f"Incorrect Input: {restart_input}")



    def version_2(self,start_date=0,end_date=7):
        data_access.calculate_change(self._all_data,reversed=False,end_date=end_date,change_type='price')

    def version_3(self,list_with_indicators):
        calculate_ratio = []
        for key,value in list_with_indicators.items():
            working_stock = value['stock_change']
            working_price = value['price_change']
            working_volume = value['volume_change']
            # I am trying to find items with the biggest price drop and highest stock gain

            # Filters the item pre-maths to limit absurdities and favor certain items
            value_filters = analysis.filter_condition(value)
            if value_filters:
                # print(value['price'][0])
                try:
                    appendable_value = (value['name'],working_volume/(2*working_price*working_stock))
                    calculate_ratio.append(appendable_value)
                except ZeroDivisionError as err:
                    print(err,appendable_value)



        # used by working_list to reference names for later
        reference_dict = {}
        working_list = []
        for item in calculate_ratio:
            reference_dict[item[1]] = item
            working_list.append(item[1])

        loop_filter = 0

        working_list = [a for a in working_list if a < loop_filter]
        working_list.sort()

        # All change is in %, between 0-100
        # Formula: ratio(price_change,stock_change)*volume_change*price(this is to favor more expensive items)
        # the final print() prints out the top 10 best purchases
        top_10 = [reference_dict[a] for a in working_list[:10]]
        print(top_10)
        return top_10






# First tests of a progress bard for Dev_3.V2.2

from time import sleep
if __name__ == "__main__":
    pass
    




        
        