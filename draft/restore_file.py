import os

WAITING = 'waiting'
UPLOADED = 'uploaded'

def restore_files():
    for file in os.listdir(UPLOADED):
        if file.endswith(".csv"):
            print('moving ' + file)
            os.replace(UPLOADED + '/' + file, WAITING + "/" + file)

restore_files()


