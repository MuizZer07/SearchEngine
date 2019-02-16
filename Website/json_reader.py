import json

class Json_Reader():

    def __init__(self):
        with open('Website/product.json', encoding="utf8") as data_file:    
             self.data = json.load(data_file)

    def read_file(self):
        return self.data
