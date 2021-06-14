import json
import datetime
import data.context_manager as cm

date_today = str(datetime.date.today())



# This can fetch and print all the lines saved in every json file for the day
for i in range(1,14):
    with cm.ContextManager(f"data/group_{i}/daily/{date_today}.json") as file:
        use_file = json.loads(file.read())
    for item in use_file.values():
        print(item)
        