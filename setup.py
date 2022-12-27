import os
import json

#installs requirements, in case u don't have venv
def install_requirements():
    print("Installing requirements")
    os.system("pip install -r requirements.txt")


#Creates data/ & creates and fills data/config.json
def create_config():
    if not os.path.exists('data'):
        os.makedirs('data')

    print("config.json not found. Creating it now"
    with open('data/config.json','w') as f:
        f.write('{}')

    data = {}

    data["channel_id"] = input("What channel id would you like to use? ")

    with open('data/config.json','w') as f:
        f.write(json.dumps(data))

#creates .env file if you don't have one, and fills in the token
def create_dotenv():
    if not os.path.exists('.env'):
        token = input("What bot token would you like to use? ")
        with open('.env','w') as env:
            env.write(f'TOKEN="{token}"')

def setup():
    install_requirements()
    create_config()
    create_dotenv()

    input("Setup finished. Press enter to exit.")
    exit()


if __name__ == '__main__':
    setup()
    