#######################
# @author: RaffaDNDM
# @date:   2022-04-10
#######################

import subprocess
from sys import stdout
import os
import csv
from time import sleep
from termcolor import cprint
from alive_progress import alive_bar

#List of directory paths where you will find 'scan_input.csv' file
WORKING_DIR=["example/services1", "example/services2"]

#nmap command to be executed
COMMAND = "nmap {scan_option} {output_option} -p{portList} {ip}"

#nmap options to be launched:
# -n:   disable DNS Name Resolution
# -Pn:  disable host discovery (no ping for each target IP)
# -sC:  default script for discovered port services
# -sV:  identify service version running on a port
# --reason: print reason identified for each scanned port
# --script=vuln:    use non default script, named 'vuln', that
#                   searches for CVEs related to a port service
SCAN_OPTIONS= "-n -Pn -sC -sV --reason --script=vuln -vv"

#Option for output nmap results
# --append-output:  Append results to existing file
# -oA output_scan:  Store results with all the formats 
#                   (files with name 'output_scan' and related format extension)
OUTPUT_OPTION = "--append-output -oA output_scan"

#SPECIFIC OPTIONS
# -sU: Scan UDP port
UDP_OPTION=" -sU"

def scan(scan_name:str):
    cprint(scan_name, "red")
    TARGETS={}
    #Total number of target ports
    ports_num=0

    #Read input file with targets
    with open("scan_input.csv", "r") as fd:
        reader = csv.reader(fd)
        
        #For each row of csv file
        for row in reader:
            ip = row[0]
            port = row[1]
            protocol_l4=row[2]

            #If the target entry with specified IP doesn't exist           
            if not ip in TARGETS.keys():
                #Create a new target entry with specified IP
                TARGETS[ip]={}

            #If the L4 protocol specified value doesn't exist for the specified IP
            if not protocol_l4.upper() in TARGETS[ip].keys():
                #Create empty set of ports for specified L4 protocol value
                TARGETS[ip][protocol_l4.upper()]=set()

            #Number of ports to be scanned for the current IP address and L4 protocol
            length_list = len(TARGETS[ip][protocol_l4.upper()])

            #Update target dictionary
            TARGETS[ip][protocol_l4.upper()].add(port)

            #Update number of ports if number of ports to be scanned was increased
            if len(TARGETS[ip][protocol_l4.upper()])!=length_list:
                ports_num+=1

    #Number of ports already scanned
    scanned_ports=0

    #Create an instance of progress bar
    with alive_bar(total=ports_num) as bar:
        
        #Open detailed output file
        with open("detailed_output_scan.txt", "a") as fd:
            #For each target IP
            for (ip,v) in TARGETS.items():
                #For each list of ports related to Level 4 Protocol
                for (protocol_l4,ports_set) in v.items():
                    #String of all ports related to Level 4 Protocol of the current IP
                    ports=','.join(str(s) for s in ports_set)
                    bar.text(f'[{protocol_l4}] {ip:15} -> {ports}')
                    
                    #Add UDP option to general nmap scanning options
                    option=SCAN_OPTIONS
                    if protocol_l4=="UDP":
                        option+=UDP_OPTION

                    #Define nmap command
                    cmd=COMMAND.format(scan_option=option, output_option=OUTPUT_OPTION, portList=ports, ip=ip)
                    
                    #Run the nmap scan
                    process = subprocess.Popen(cmd, shell=True,stdout=fd)
                    process.wait()
                    
                    #Update progress bar
                    for i in range(len(ports_set)):
                        bar()

def main():
    root_dir = os.getcwd()

    #Read input (target IPs and ports) from csv files
    for dir in WORKING_DIR:
        os.chdir(root_dir+'/'+dir)
        scan(dir)

if __name__=='__main__':
    main()