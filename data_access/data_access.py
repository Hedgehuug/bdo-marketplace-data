import json
import datetime
import data.context_manager as cm
import os
import analysis

date_today = datetime.date.today()
day_delta = datetime.timedelta(days=1)
data_folder_reference = "../data"

class Data_Access:
    def __init__(self,data):
        self.__data = data

    # I NEED TO MAKE THIS A @CLASSMETHOD SO I CAN CREATE OBJECTS
    @staticmethod
    def get_all_info():
        final_value = {}
        for i in range(1,14):
            with cm.ContextManager(f"../data/group_{i}/daily/{str(date_today)}.json") as file:
                use_file = json.loads(file.read())
            # this turns all the 
            
            for value in use_file.values():
                value = analysis.Analysis.create_list_fetch_all(value)
            """
            for value in use_file.values():
                value['stock'] = [value['stock']]
                value['volume'] = [value['volume']]
                value['price'] = [value['price']]
            """
            # MERGES ALL THE JSON FILES TOGETHER
            final_value.update(use_file)
        # SO THIS VERY USEFUL LOOP THAT FETCHES ALL PAST DAY INFO
        onlyfiles = len(os.listdir("../data/group_2/daily"))
        use_date = date_today
        for a in range(onlyfiles-1):
            use_date -= day_delta
            print(use_date)
            for i in range(1,14):
                with cm.ContextManager(f"../data/group_{i}/daily/{str(use_date)}.json") as file:
                    lookback_file = json.loads(file.read())
                for key,value in lookback_file.items():
                    final_value[key]['stock'].append(value['stock'])
                    final_value[key]['volume'].append(value['volume'])
                    final_value[key]['price'].append(value['price'])
                    print(final_value[key])
        return final_value


print(Data_Access.get_all_info())

        

