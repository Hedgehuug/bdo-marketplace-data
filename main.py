import os
import json
import data
import datetime
import requests
import data.context_manager as cm
import api_data.api_requests as api_requests
from analysis.analysis import Analysis as analysis
from data_access import data_access
import services


# Main file

# Temporary Link, will turn into a selection
abspath = os.path.abspath('bdo-marketplace-data')
print(abspath)
with cm.ContextManager(f"{abspath}/data/settings.json") as file:
    settings = json.loads(file.read())
temporary_link = 'https://eu-trade.naeu.playblackdesert.com/Trademarket/GetWorldMarketList'
offile_mode = False


# Option one hits the api and saves all the data for that day
def option_one(url):
    try:
        services.fetch_and_store_data(url)
    except requests.exceptions.ConnectionError as err:
        print(f"Could not connect to API: {err}\n")
        print("Marketplace info not fetched")
        print("Starting in Offline Mode")
        offline_mode = True


# Option Two is for the accessing of data, this might get broken up further later
def option_two():
    # Item id-name references
    while True:
        with cm.ContextManager(f"{abspath}/data/mp_reference.json") as item_reference_file:
            reference_json = json.loads(item_reference_file.read())
        all_data = data_access.Data_Access.get_all_info()

        version_list = ['Fetch Item Info','All Data','Rankings','Back to Main Menu']
        for x in version_list:
            print(f"{version_list.index(x) +1}: {x}")


        version_input = int(input("Input Version: "))
        # try:
        if version_input != 4:
            data_object = services.Data_Access_Version(all_data.make_indicators(),version=version_input,reference = reference_json)

        elif version_input == 4:
            break

        """
        except TypeError as err:
            print(f"TypeError: {err}")"""





def main():
    # Fetched date of last fetch from settings
    date_today = datetime.date.today()
    settings_date = datetime.date.fromisoformat((settings['last-fetched']))
    if date_today == settings_date:
        # If the data for today is already fetched:
        print("Information already fetched for the day")

    elif date_today != settings_date:
        # if it is not fetched
        option_one(temporary_link)
        settings['last-fetched'] = str(date_today)
        with open(f"{abspath}/data/settings.json",'w') as file:
            json.dump(settings,file)
        print('\n')
        


    # Used by input() for user inputs later
    menu_options = [
        "Fetch Daily Data",
        "Get Item Info",
        "Leaderboard",
        "Exit"
    ]

    # Step 1: Print the main menu options
    while True:
        for option in menu_options:
            print(f"{menu_options.index(option) +1}: {option}")

        # Step 2: Take input
        menu_input= int(input("Enter Num. for menu option: "))

        # Step 3: Logic

        # Option 1 will override the day's info fetch
        if menu_input == 1:
            option_one(temporary_link)

        # Option 2 prints all price changes
        if menu_input == 2:
            option_two()
        if menu_input == 4:
            break
    print('Thank you for using the bdo marketplace analyzer')
    print('Goodbye!')

if __name__ == "__main__":
    main()








