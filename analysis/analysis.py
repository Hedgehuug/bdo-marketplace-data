
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

        

        
    


