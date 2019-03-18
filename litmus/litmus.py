import os
import json
import math

class Litmus():
    data = []
    @classmethod
    def initialize(cls, method):
        if method == "Json":
            with open("litmus/litmus.json") as f:
                dj = json.loads(f.read())
            cls.data = dj['Default']
            return

    @staticmethod
    def data():
        return Litmus.data

    @staticmethod
    def count():
        return len(Litmus.data)


