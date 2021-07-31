import sys
sys.path.append('/Users/Ben 1/Documents/GitHub/bdo-marketplace-data')
print(sys.path)
import data_access.data_access as da
from data_access.data_access import Data_Access as data_access
from flask import Flask
import services
import json

app = Flask(__name__)



@app.route('/')
def get_ranking():
    all_data = data_access.get_all_info()
    all_data = all_data.make_indicators()
    return json.dumps(services.Data_Access_Version(all_data).version_3(list_with_indicators=all_data))