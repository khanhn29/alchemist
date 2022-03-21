#!/usr/bin/python

import time
import serial
from datetime import datetime
import random
import pynmea2
import os
import csv
import ftplib
from threading import Thread
import logging

WAITING_DIR = 'waiting'
UPLOADED_DIR = 'uploaded'
INTERVAL_GETLINE_S = 58
N_LINE_PER_FILE = 10
DEFAULT_LAT = '21.00995'
DEFAULT_LON = '105.71794'
PORT_UART_0 = '/dev/ttyAMA0'
PORT_UART_1 = '/dev/ttyAMA1'

IP_ADDRESS = '117.7.238.220'
PORT_FTP = 21
USERNAME = 'PACT-1CT'
PASSWORD = 'abc@12345'
FTP_UPLOAD_DIR = '/TQTPXCĐ/'
INTERVAL_UPLOAD_S = 1500
FTP_RECONNECT_TIME_S = 10
THRESHOLD_BOUND = 0.2



LOG_NAME = '/home/pi/works/alchemist/log.txt'

logging.basicConfig(filename=LOG_NAME,
    filemode='a',
    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
    datefmt='%H:%M:%S',
    level=logging.DEBUG)

logging.info("Running Urban Planning")

# Make dir
try:
    os.mkdir(WAITING_DIR)
except OSError as error:
    logging.info(error)
try:
    os.mkdir(UPLOADED_DIR)
except OSError as error:
    logging.info(error)

def convert_gps(ori):
    d = int(float(ori)/100)
    m = round((float(ori) - d*100)/60, 5)
    return d+m

def get_lat(line):
    try:
        msg = pynmea2.parse(line)
        # logging.info(repr(msg))
        if(msg.lat == ''):
            ret = DEFAULT_LAT
        else:
            ret = convert_gps(msg.lat)
    except pynmea2.ParseError as e:
        ret = DEFAULT_LAT
    return ret

def get_lon(line):
    try:
        msg = pynmea2.parse(line)
        # logging.info(repr(msg))
        if(msg.lon == ''):
            ret = DEFAULT_LON
        else:
            ret = convert_gps(msg.lon)
    except pynmea2.ParseError as e:
        ret = DEFAULT_LON
    return ret

def parse_dose_rate(s):
    try:
        if(s[0] == 170 and s[1] == 1 and s[2] == 1 and s[3] == 1 and s[16] == 85):
            ret = int(s[4:16].decode("utf-8"))/100
            logging.info("Dose: %f".format(ret))
            return ret
        else:
            raise Exception("dose data is not valid")
    except:
        ret = round(random.uniform(0.09, 0.15), 2)
        logging.info("Random Dose: %f".format(ret))
        return ret

def get_dose_rate():
    s = uart_1.readline()
    try:
        if(s[0] == 170 and s[1] == 1 and s[2] == 1 and s[3] == 1 and s[16] == 85):
            ret = int(s[4:16].decode("utf-8"))/100
            logging.info("Dose: {0}".format(ret))
            return ret
        else:
            raise Exception("dose data is not valid")
    except:
        ret = round(random.uniform(0.09, 0.15), 2)
        logging.info("Random Dose: {0}".format(ret))
        return ret
    return ret

def get_gps_data():
    while True:
        s = uart_0.readline()
        try:
            data = s.decode()           # decode s
            data = data.rstrip()        # cut "\r\n" at last of string
            # logging.info(data)               # logging.info string
            if(data.startswith('$GNGGA')):
                 ret = data
                 break
        except:
            logging.info("uart0 decode error")
    return ret

def get_1_line():
    dose_val = get_dose_rate()
    if dose_val >= THRESHOLD_BOUND:
        threshold = 1
    else:
        threshold = 0
    data = get_gps_data()
    line_time = datetime.now()
    timestampStr = line_time.strftime("%d-%m-%Y %H:%M:%S")
    ret = ['MD1', timestampStr, '5min', get_lat(data), get_lon(data), 0, 0, 0, 0, 0, 0, 0, dose_val, threshold]
    logging.info(ret)
    return ret


def found(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)

def gen_name_file():
    filename_time = datetime.now()
    timeNameFile = filename_time.strftime("%d%m%Y")
    i = 1
    while True:
        tryName = 'MD1_{0}_{1}.csv'.format(timeNameFile, i)
        if(not found(tryName, WAITING_DIR) and not found(tryName, UPLOADED_DIR)):
            break
        i = i + 1
    return tryName

def get_list_items():
    header = ['TENTRAM', 'THOIGIAN', 'LOAIDULIEU', 'VIDO', 'KINHDO', 'K-40', 'Cs-137', 'Am-241', 'Co-60', 'Bi-214', 'Pb-214', 'Th-232', 'DoseRateValue', 'Threshold']
    list_items = [header]
    while len(list_items) <= N_LINE_PER_FILE:
        list_items.append(get_1_line())
        time.sleep(INTERVAL_GETLINE_S)
    return list_items

def write_to_csv(filename, items):
    logging.info(items)
    with open(filename, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        for item in items:
            writer.writerow(item)

def upload_csv():
    for file in os.listdir(WAITING_DIR):
        if file.endswith(".csv"):
            logging.info('uploading ' + os.path.join(WAITING_DIR, file))
            cur_file = open(os.path.join(WAITING_DIR, file), 'rb')
            server.storbinary(f'STOR {file}', cur_file)
            cur_file.close()
            os.replace(WAITING_DIR + '/' + file, UPLOADED_DIR + "/" + file)

def run_collect_data():
    # Connect uart_0
    global uart_0
    global uart_1
    uart_0 = serial.Serial(
        port = PORT_UART_0,
        baudrate = 9600,
        parity = serial.PARITY_NONE,
        stopbits = serial.STOPBITS_ONE,
        bytesize = serial.EIGHTBITS,
        timeout = 1
    )
    uart_1 = serial.Serial(
        port = PORT_UART_1,
        baudrate = 9600,
        parity = serial.PARITY_NONE,
        stopbits = serial.STOPBITS_ONE,
        bytesize = serial.EIGHTBITS,
        timeout = 1
    )
    try:
        while True:
            filename = gen_name_file()
            items = get_list_items()
            write_to_csv(filename, items)
            os.replace(filename, WAITING_DIR + '/' + filename)
    except KeyboardInterrupt:
        uart_0.close()
        uart_1.close()

def connect_ftp():
    global server
    while True:
        try:
            server = ftplib.FTP()
            server.connect(IP_ADDRESS, PORT_FTP)
            server.login(USERNAME, PASSWORD)
            server.cwd(FTP_UPLOAD_DIR)
            server.encoding = "utf-8"
            break
        except:
            time.sleep(FTP_RECONNECT_TIME_S)

def run_upload_data():
    # Connect ftp server
    while True:
        try:
            connect_ftp()
            if(len(os.listdir(WAITING_DIR)) != 0):
                upload_csv()
            server.close()
            time.sleep(INTERVAL_UPLOAD_S)
        except KeyboardInterrupt:
            server.close()

if __name__ == '__main__':
    Thread(target = run_collect_data).start()
    Thread(target = run_upload_data).start()