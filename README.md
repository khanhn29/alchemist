# Urban Planning Data Collection and Upload

This Python project collects data from a UART device (specifically GPS data from `/dev/ttyAMA0` and dose rate data from `/dev/ttyAMA1`), saves it to CSV files, and uploads those files to an FTP server. It's designed for urban planning applications, likely related to radiation monitoring.

## Features

* **Dual UART Reading:** Reads GPS data from one UART port and dose rate data from another.
* **Data Parsing:** Parses NMEA sentences from the GPS data and extracts latitude and longitude.  Parses the dose rate data from a specific byte stream.
* **Data Logging:** Logs events and data to a file (`log.txt`).
* **CSV File Generation:** Creates CSV files with timestamps, GPS coordinates, dose rate, and a threshold indicator.  Files are named with the format `MD1_DDMMYYYY_N.csv`.
* **File Management:**  Organizes files into `waiting` (for upload) and `uploaded` directories.
* **FTP Upload:** Uploads CSV files to a specified FTP server.  Handles FTP connection and reconnection.
* **Threading:** Uses separate threads for data collection and FTP upload to ensure continuous operation.
* **Error Handling:** Includes error handling for UART communication, data parsing, file operations, and FTP connections.
* **Configuration:**  Parameters like UART ports, baud rates, FTP server details, upload interval, and data thresholds are configurable within the script.

## Requirements

* Python 3.x
* `pyserial`: For serial communication. Install with: `pip install pyserial`
* `pynmea2`: For parsing NMEA sentences. Install with: `pip install pynmea2`
* `ftplib`: For FTP communication (built-in to Python's standard library).

## Installation

1. Clone the repository (replace with your actual repository URL if applicable):
   ```bash
   git clone https://github.com/khanhn29/UART2CSV2FTP.git
   cd UART2CSV2FTP
