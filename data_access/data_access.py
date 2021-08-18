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
    def __init__(self,data,version=3,reference_file=""):
        self._data = data
        self._version = version
        self._reference_file = reference_file

    # I NEED TO MAKE THIS A @CLASSMETHOD SO I CAN CREATE OBJECTS
    @classmethod
    def get_all_info(self):
        # Fetches every single item's historical data
        final_value = {}
        for i in range(1,14):
            with cm.ContextManager(f'data/group_{i}/daily/{str(date_today)}.json') as file:
                use_file = json.loads(file.read())
            
            for value in use_file.values():
                value = analysis.Analysis.create_list_fetch_all(value)
            # MERGES ALL THE JSON FILES TOGETHER
            final_value.update(use_file)
        # SO THIS VERY USEFUL LOOP THAT FETCHES ALL PAST DAY INFO
        onlyfiles = len(os.listdir("data/group_2/daily"))
        use_date = date_today
        for a in range(onlyfiles-1):
            use_date -= day_delta
            for i in range(1,14):
                with cm.ContextManager(f"data/group_{i}/daily/{str(use_date)}.json") as file:
                    lookback_file = json.loads(file.read())
                for key,value in lookback_file.items():
                    print(key,value)
                    final_value[key]['stock'].append(value['stock'])
                    final_value[key]['volume'].append(value['volume'])
                    final_value[key]['price'].append(value['price'])
                    # print(final_value[key])
        return Data_Access(final_value)

    @staticmethod
    def calculate_change(info,change_type='price',reversed=False,start_date=0,end_date=1):
        return_info = info
        final_list = []
        for key,value in info.items():
            # Calculates % change between today and yesterday's price
            try:
                change_amount = 100 * (int(value[change_type][start_date]) / int(value[change_type][end_date]) - 1)
            except ZeroDivisionError as err:
                # print(f"{value[change_type]}: {err}")
                change_amount = -100
            # change_amount = 
            # Creates a Variable with name: change amount
            change_variable = (change_amount,value['name'])
            # print(f"{change_amount}%")
            return_info[key][f"{change_type}_change"] = change_amount
            final_list.append(change_variable)
        # final_list.sort(reverse=reversed)
        # print(final_list)
        return return_info

    def make_indicators(self,start_date=0,end_date=7):
        # calculates and appends change % to each item's data
        stock_filter = self.calculate_change(self._data,reversed=False,end_date=end_date,change_type='stock')
        volume_filter = self.calculate_change(stock_filter,reversed=False,end_date=end_date,change_type='volume')
        final_dict = self.calculate_change(volume_filter,reversed=False,end_date=end_date,change_type='price')
        return final_dict
    

    def __Repr__(self):
        return self._data



            


def version_3(data):
    final_dict = data
    calculate_ratio = []
    for key,value in final_dict.items():
        working_stock = value['stock_change']
        working_price = value['price_change']
        working_volume = value['volume_change']
        # I am trying to find items with the biggest price drop and highest stock gain
        if working_price < -10 and working_stock > 0 and working_volume > 0:
            # print(value['price'][0])
            calculate_ratio.append((value['name'],(2*working_price*working_stock)*working_volume))



    # used by working_list to reference names for later
    reference_dict = {}
    working_list = []
    for item in calculate_ratio:
        reference_dict[item[1]] = item
        working_list.append(item[1])

    loop_filter = -1

    working_list = [a for a in working_list if a < loop_filter]
    working_list.sort()

    # All change is in %, between 0-100
    # Formula: ratio(price_change,stock_change)*volume_change*price(this is to favor more expensive items)
    # the final print() prints out the top 10 best purchases, not taking into account price and relevancy
    top_10 = [reference_dict[a] for a in working_list[:10]]
    return top_10
    print(top_10)


if __name__ == "__main__":
    
    # I DID SOME MASSIVE THINGS HERE IN TEST_BRANCH_1, I CANNOT WAIT TO GO EVEN FURTHER WITH THIS, AFTER SOME BUG FIXES AND ERROR HANDLING
    # I WILL BE READY TO TRY BUILD AN API AND TEST IT ON A TELEGRAM BOT

    # 
    all_item_info = Data_Access.get_all_info()._data

    with cm.ContextManager('../data/mp_reference.json') as item_reference_file:
        reference_json = json.loads(item_reference_file.read())

    # print(reference_json)
    # This currently has absolutely no error handling treat it with a grain of salt
    version_input = int(input("Version n: "))
    version = version_input

    """if version == 1:
        input_name = input("Input part of searched item, it'll return all items with it in their name: ")

        returned_item_from_input = list(filter(lambda a: input_name in a[1],reference_json))
        # Prints out all the searched for items' past data
        for items in returned_item_from_input:
            try:
                print("------------------------")
                print(f"{all_item_info[items[0]]['name']}:")
                print(f"Stock: \n{all_item_info[items[0]]['stock']}")
                print(f"Stock Change: \n{final_dict[items[0]]['stock_change']}")
                print(f"Volume: \n{all_item_info[items[0]]['volume']}")
                print(f"Volume Change: \n{final_dict[items[0]]['volume_change']}")
                print(f"Price: \n{all_item_info[items[0]]['price']}")
                print(f"Price Change: \n{final_dict[items[0]]['price_change']}")
            except KeyError as err:
                print(f"Could not find information on {err}")

            finally:
                str(input("Would you like to search another item?(y/n): "))
                main()"""


    lookback = 0
    if version == 0:
        print(all_item_info)

    """if version == 2:
        Data_Access.calculate_change(all_item_info,reversed=False,end_date=7,change_type='price')
    """

    if version == 3:
        version_3(all_item_info)

            
        
        
        


        

        

