# 3 folder:
#   . : folder to the current python file, new file is writen here
#   ./waiting: folder to hold all the files waiting for upload
#   ./uploaded: folder to hold all files has been uploaded
# check folder 'waiting' is empty
#   if empty: wait 10sec
#   if not empty: start upload files, then wait 10sec

import ftplib
import os
import time

WAITING_DIR = 'waiting'
UPLOADED_DIR = 'uploaded'
UPLOAD_TIMEWAIT = 600

server = ftplib.FTP()
server.connect('117.7.238.220', 21)
server.login('PACT-1CT','abc@12345')
server.cwd('/TQTPXCĐ/')
server.encoding = "utf-8"
try: 
    os.mkdir(UPLOADED_DIR) 
except OSError as error: 
    print(error)

def upload_csv():
    for file in os.listdir(WAITING_DIR):
        if file.endswith(".csv"):
            print('uploading ' + os.path.join(WAITING_DIR, file))
            cur_file = open(os.path.join(WAITING_DIR, file), 'rb')
            server.storbinary(f'STOR {file}', cur_file)
            cur_file.close()
            os.replace(WAITING_DIR + '/' + file, UPLOADED_DIR + "/" + file)

try:
    while True:
        if(len(os.listdir(WAITING_DIR)) == 0):
            time.sleep(UPLOAD_TIMEWAIT)
        else:
            upload_csv()
            time.sleep(UPLOAD_TIMEWAIT)
except KeyboardInterrupt:
    ser.close()
#DoseRateValue 0.09-0.15
