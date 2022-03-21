import os

try: 
    os.mkdir("uploaded") 
except OSError as error: 
    print(error)