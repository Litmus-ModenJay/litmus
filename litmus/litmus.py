import os
import json
import math

class LitmusDB():
    db = []
    
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
    
    @staticmethod
    def all():
        return LitmusDB.db

    @staticmethod
    def count():
        return len(LitmusDB.db)
    
