import os
import json

#creates config.json in the data directory

def create_config():
    print("config.json not found. Creating it now")
    with open('data/config.json','w') as f:
        f.write('{}')

def setup():
    if not os.path.exists('data'):
        os.makedirs('data')

    data = {}

    create_config()
    data["channel_id"] = input("What channel id would you like to use? ")

    with open('data/config.json','w') as f:
        f.write(json.dumps(data))

    if not os.path.exists('.env'):
        token = input("What bot token would you like to use? ")
        with open('.env','w') as env:
            env.write(f'TOKEN="{token}"')

    input("Setup finished. Press enter to exit.")
    exit()


if __name__ == '__main__':
    setup()
    