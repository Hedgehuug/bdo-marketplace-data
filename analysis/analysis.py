
class Analysis:
    def __init__(self,payload):
        self.__payload = payload

    # Decodes the raw returned message from hitting the endpoint
    @staticmethod
    def decode_msg(raw_payload):
        raw_split_msg = str(raw_payload).split('|')
        mapped_msg = map(lambda item: item.split('-'),raw_split_msg)
        mapped_msg = list(mapped_msg)[:-1]
        return list(mapped_msg)

    # Used at the start of option 3:ranking, to filter items based on desired input
    @staticmethod
    def filter_condition(data={}):
        price_threshold = int(data['price'][0]) > 1000
        stock_threshold = int(data['stock'][0]) > 10
        volume_threshold = int(data['volume_change']) > 0
        price_change_threshold = int(data['price_change']) < -12

        return all([price_threshold,stock_threshold,volume_threshold,price_change_threshold])
        



    # This is going to convert working data to savable json data for sub_group searches
    @staticmethod
    def reformat_sub_group(data):
        return_dict = {}
        for line in data:
            return_dict[line[0][0]] = {
            "name": line[0][1],
            "stock": line[1][0],
            "volume": line[1][1],
            "price": line[1][2]
            }
        return return_dict


    # Used for creating lists out of the initially fetched files going backwards from today, it's meant to be used in recursive steps
    @staticmethod
    def create_list_fetch_all(item):
        item['stock'] = [item['stock']]
        item['volume'] = [item['volume']]
        item['price'] = [item['price']]
        return item




        """
            converted_line = {
            "name": line[0[1]],
            "stock": line[1[0]],
            "volume": line[1[1]],
            "price": line[1[2]]
            }"""


    """
    Data Layout for saving:

    as of 11-06-21 this can be used to reference how final_print is laid out
    id = {
        name = i[0[1]],
        stock = i[1[0]],
        volume = i[1[1]],
        price = i[1[2]]
    }
    """

        

        
    


