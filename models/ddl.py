import sys

from flask import Flask
from models import *
from populatedb import initPopulateDB
from pathlib import Path

# Enables Flask instance 
app = Flask(__name__)

# Configuration file from environment variable
app.config['ENV'] = 'development'
app.config['DEBUG'] = True
sys.path.append((Path(__file__).parent.parent.resolve() / 'instance').as_posix())
from config_models import configType as cfgmodels
app.config.from_object(cfgmodels[app.config['ENV']])

# Enable instance of SQLAlchemy
db.init_app(app)

def main(argv):
    #Database DDL
    with app.app_context():
        # At least one parameter has been received
        if len(argv) > 1:

            # Creates all Database Tables
            if argv[1] == "create_all":
                print("Executing SQLAlchemy create_all")
                db.create_all()
                initPopulateDB()

            # Drops all Database Tables
            elif argv[1] == "drop_all":
                print("Executing SQLAlchemy drop_all")
                db.drop_all()
            
            else:
                print("Command not supported")

        else:
            print("No command specified. Commands supported:")
            print("$ python3 ddl.py [create_all | drop_all]")


# Executes main() function if this file is executed as "__main__"
if __name__ == "__main__":
    main(sys.argv)