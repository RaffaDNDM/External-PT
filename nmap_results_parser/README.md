# NMAP file parser
The program will parse results of nmap scan from an input file, provided to the program:

## Installation
```bash
pip3 install -r requirements.txt
```

## Cheat sheet
```bash
python3 nmap_parser.py -in input_file.gnmap
```
or
```bash
python3 nmap_parser.py -in input_file.xml
```

After parsing the file, the results will be organized in an output csv file, called `{input_file}_xml.csv` or `{input_file}_gnmap.csv` and stored in the working directory.

## Help command
```bash
python3 nmap_parser.py --help
```