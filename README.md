# UART to CSV to FTP

This Python project reads data from a UART (Universal Asynchronous Receiver-Transmitter) device, saves it to a CSV file, and then uploads the CSV file to an FTP server.  This is useful for logging data from embedded systems or other devices that communicate via UART.

## Features

* **UART Reading:** Reads data from a specified UART port.
* **CSV Saving:** Saves the received data to a CSV file, including timestamps.
* **FTP Upload:** Uploads the generated CSV file to a specified FTP server.
* **Configurable:**  Allows configuration of UART port, baud rate, CSV filename, FTP server details, etc. through a configuration file (e.g., `config.ini`).
* **Error Handling:** Includes basic error handling for UART communication, file operations, and FTP connection.
* **Logging:** Uses a logging mechanism to record events and potential errors.

## Requirements

* Python 3.x
* `pyserial`: For serial communication.  Install with: `pip install pyserial`
* `ftplib`: For FTP communication (built-in to Python's standard library).
* `configparser`: For reading configuration files (built-in to Python's standard library).

## Installation

1. Clone the repository:
   ```bash
   git clone [https://github.com/](https://github.com/)[your-username]/uart-csv-ftp.git
   cd uart-csv-ftp
