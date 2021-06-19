import json
import datetime

import sys
sys.path.append('..')
import data as data
import data.context_manager as cm
import os
import analysis.analysis as analysis

date_today = datetime.date.today()
day_delta = datetime.timedelta(days=1)
data_folder_reference = "../data"

class Data_Access:
    def __init__(self,data):
        self.__data = data

    # I NEED TO MAKE THIS A @CLASSMETHOD SO I CAN CREATE OBJECTS
    @staticmethod
    def get_all_info():
        # Fetches every single item's historical data
        final_value = {}
        for i in range(1,14):
            with cm.ContextManager(f'../data/group_{i}/daily/{str(date_today)}.json') as file:
                use_file = json.loads(file.read())
            
            for value in use_file.values():
                value = analysis.Analysis.create_list_fetch_all(value)
            # MERGES ALL THE JSON FILES TOGETHER
            final_value.update(use_file)
        # SO THIS VERY USEFUL LOOP THAT FETCHES ALL PAST DAY INFO
        onlyfiles = len(os.listdir("../data/group_2/daily"))
        use_date = date_today
        for a in range(onlyfiles-1):
            use_date -= day_delta
            # print(use_date)
            for i in range(1,14):
                with cm.ContextManager(f"../data/group_{i}/daily/{str(use_date)}.json") as file:
                    lookback_file = json.loads(file.read())
                for key,value in lookback_file.items():
                    final_value[key]['stock'].append(value['stock'])
                    final_value[key]['volume'].append(value['volume'])
                    final_value[key]['price'].append(value['price'])
                    # print(final_value[key])
        return final_value



if __name__ == "__main__":
    # I DID SOME MASSIVE THINGS HERE IN TEST_BRANCH_1, I CANNOT WAIT TO GO EVEN FURTHER WITH THIS, AFTER SOME BUG FIXES AND ERROR HANDLING
    # I WILL BE READY TO TRY BUILD AN API AND TEST IT ON A TELEGRAM BOT
    # print(Data_Access.get_all_info())
    all_item_info = Data_Access.get_all_info()

    with cm.ContextManager('../data/mp_reference.json') as item_reference_file:
        reference_json = json.loads(item_reference_file.read())

    # print(reference_json)
    # This currently has absolutely no error handling treat it with a grain of salt
    input_name = input("Input part of searched item, it'll return all items with it in their name: ")

    returned_item_from_input = list(filter(lambda a: input_name in a[1],reference_json))
    # Prints out all the searched for items' past data
    for items in returned_item_from_input:
        try:
            print("------------------------")
            print(f"{all_item_info[items[0]]['name']}:")
            print(f"Stock: \n{all_item_info[items[0]]['stock']}")
            print(f"Volume: \n{all_item_info[items[0]]['volume']}")
            # ADD DAILY VOLUME RIGHT HERE, IT'LL BE WAY MORE USEFUL THAN TOTAL VOLUME
            print(f"Price: \n{all_item_info[items[0]]['price']}")
        except KeyError as err:
            print(f"Could not find information on {err}")

        

