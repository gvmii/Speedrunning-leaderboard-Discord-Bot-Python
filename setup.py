import os
import json

#creates config.json in the data directory

def create_config():
    print("file not found")
    with open('data/config.json','w') as f:
        print("the")
        f.write('{}')
        print("impost")

def setup():
    if not os.path.exists('data'):
        os.makedirs('data')

    data = {}

    create_config()
    data["channel_id"] = input("What channel id would you like to use?")

    with open('data/config.json','w') as f:
        f.write(json.dumps(data))


if __name__ == '__main__':
    setup()
    