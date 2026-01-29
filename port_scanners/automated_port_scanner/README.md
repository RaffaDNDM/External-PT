# Automated port scanner
The program executes automated nmap scanning by leveraging the *scan_input.csv* files in the directories specified in **WORKING_DIR** list of the script.
The script removed duplicated ports in the input files for each couple of *IP address* and *Level 4 Protocol*. 

## Installation
Clone the repository and type the following command:
```bash
pip install -r requirements.txt
```