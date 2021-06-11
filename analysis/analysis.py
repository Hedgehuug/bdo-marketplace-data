
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

    def reformat_sub_group(self,payload)
    


