import os
import json

#none of this works yet :3

def create_config():
    print("file not found")
    with open('data/config.json','w') as f:
        print("the")
        f.write('{}')
        print("impost")

def setup():

    if not os.path.exists('data'):
        os.makedirs('data')

    try:
        with open('data/config.json','r') as f:
            print("Config file already exists.")
    except FileNotFoundError:
        create_config()
        ChannelID = input("What channel ID would you like to use? ")

        with open('data/config.json','w') as f:
            f = f.read()
            print(f)
            f = json.load(f)
            print(f)
            f['channel_id'] = ChannelID
            f.write(json.dumps(f))


if __name__ == '__main__':
    setup()
