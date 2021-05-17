import time
import psutil
from datetime import datetime
from pymongo import MongoClient


class MongoTest:
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client['test']
        self.collection = self.db['pc_state']

    def add_data(self, posts):
        return self.collection.insert_many(posts)


def main():
    mongo_test = MongoTest()
    while True:
        posts = [
            {
                'label': 'memory',
                'value': psutil.virtual_memory().percent,
                'datetime': datetime.now()
            },
            {
                'label': 'cpu',
                'value': psutil.cpu_percent(interval=1),
                'datetime': datetime.now()
            },
            {
                'label': 'disk',
                'value': psutil.disk_usage('/').percent,
                'datetime': datetime.now()
            }
        ]
        response = mongo_test.add_data(posts)
        print(response)
        time.sleep(10)


if __name__ == '__main__':
    main()

