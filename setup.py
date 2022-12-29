import json
import os
import sqlite3


# installs requirements, in case u don't have venv
def install_requirements():
    print("Installing requirements")
    os.system("pip install -r requirements.txt")


# Creates data/ & creates and fills data/config.json
def create_config():
    if not os.path.exists("data"):
        os.makedirs("data")

    if not os.path.exists("data/config.json"):
        print("config.json not found. Creating it now")
        with open("data/config.json", "w") as f:
            f.write("{}")

        data = dict()
        data["channel_id"] = input("What channel id would you like to use? ")

        with open("data/config.json", "w") as f:
            f.write(json.dumps(data))


# creates .env file if you don't have one, and fills in the token
def create_dotenv():
    if not os.path.exists(".env"):
        token = input("What bot token would you like to use? ")
        with open(".env", "w") as env:
            env.write(f'TOKEN="{token}"')


def create_db():
    if not os.path.exists("data/database.db"):
        print("database.db not found. Creating it now")
        con = sqlite3.connect("data/database.db")
        cur = con.cursor()
        cur.execute(
            "CREATE TABLE IF NOT EXISTS anypercent(user_id INTEGER, time FLOAT)"
        )
        cur.execute(
            "CREATE TABLE IF NOT EXISTS arb(user_id INTEGER, time FLOAT)"
        )
        cur.execute(
            "CREATE TABLE IF NOT EXISTS trueending(user_id INTEGER, time FLOAT)"
        )

def setup():
    install_requirements()
    create_config()
    create_dotenv()
    create_db()

    input("Setup finished. Press enter to exit.")
    exit()


if __name__ == "__main__":
    setup()
