import pandas
class ContextManager:
    def __init__(self,filename):
        self.file = open(filename)

    def __enter__(self):
        return self.file

    def __exit__(self, type, value, traceback):
        self.file.close()

file_url = "data/mp_reference.json"
import json

content = None
with ContextManager(file_url) as file:
    content = json.loads(file.read())

print(content)



# Turn items into tuple with (Item Name, Item ID)
def create_tuple(item):
    print(f' this is the item: {item}')
    # For the JSON I am sourcing from, item[0] is the itemID(as a string) and item[1] is ItemName
    return {
        "Item name": item[1],
        "Item ID": int(item[0])
    }
#tuple_list = list(map(create_tuple,content))

dict_list = {
    'Item Names': [i[1] for i in content],
    'Item IDs': [int(i[0]) for i in content]
}

pandas_list = pandas.DataFrame(dict_list)
pandas_list.to_excel('mp_items_ids.xlsx')

