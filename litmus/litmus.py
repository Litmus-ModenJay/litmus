import os
import json
import math

class LitmusDB():
    
    def __init__(self):
        self.db = self.initialize()
    
    def initialize(self):
        with open("litmus/litmus.json") as f:
            dj = json.loads(f.read())
        data = []
        for item in dj['Default']:
            name=item['name']
            hexa=item['index']
            data.append({'name':name, 'hexa':hexa})
        return data
    def all(self):
        return self.db
    def count(self):
        return len(self.db)


