

import os
import sys

print("DELETING MESSAGES DATABASE")
os.system("rm -r ./project/static/messages/")
print("DROPPING DATABASE")
os.system("python manage.py drop_db")
print("CREATING DATABASE")
os.system("python manage.py create_db")
print("STARTING SERVER")
os.system("python manage.py runserver")