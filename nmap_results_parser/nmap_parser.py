#######################
# @author: RaffaDNDM
# @date:   2022-09-23
#######################

import argparse
import os
from alive_progress import alive_bar
from bs4 import BeautifulSoup
from copy import deepcopy

INFO_NMAP={}
NMAP_FORMATS = [".gnmap", ".xml"]
    
def gnmap_parser(input_file):
    global INFO_NMAP

    #Read gnmap content 
    #(without first two lines that contain details about launched command and nmap version)
    with open(input_file, "r") as f:
        content = [line.replace("\n", "") for line in f.readlines() if line[0]!='#']

    #Number of lines read
    num_lines=len(content)

    #Progress bar
    with alive_bar(num_lines) as bar:
        
        #Read each line
        for line in content:
            line = line.replace("Host: ", "")
            line = line.replace(" (", ";", 1)
            
            #First line of an host in gnmap files (with its status)
            if "Status" in line:
                line = line.replace(")    Status: ", ";")
                info = line.split(";")
                ip = info[0]
                domain = info[1]
                status=info[2].upper()

                #Create a new sict instance for an IP (if seen for first time)
                if ip not in INFO_NMAP:
                    INFO_NMAP[ip] = {}

                #Create dict instance for a domain under an IP
                INFO_NMAP[ip][domain]={ "status": status,
                    "ports": []
                }
                
            #Second line of an host in gnmap files (with its ports details)
            elif "Ports" in line:
                #Read all ports items
                line = line.replace(")    Ports: ", ";")
                info = line.split(";")
                ip = info[0]
                domain = info[1]
                print(info[2])
                ports=info[2].split(", ")

                #For each port, read related information
                for i in range(len(ports)):
                    ports[i]=ports[i].replace("///", "/")
                    ports[i]=ports[i].replace("//", "/")
                    ports[i]=ports[i].replace("/", ",")
                    ports[i]=ports[i].replace("tcp", "TCP")

                    if "Ignored State:" in ports[i]:
                        ports[i] = ports[i][:ports[i].find('Ignored State:')-1]

                    #Remove last spaces and last comma
                    ports[i]=ports[i].strip()[:-1]

                #Store all ports info discovered the couple (ip, domain)
                INFO_NMAP[ip][domain]["ports"]= ports

            bar()

def write_gnmap_results(path_no_extension):
    global INFO_NMAP

    with open(f'{path_no_extension}_gnmap.csv', "w") as f:
        f.write('IP, Domain, Status, Port, Port Status, Protocol, Service, Service description\n')
        
        for ip in INFO_NMAP:
            for domain in INFO_NMAP[ip]:
                for port in INFO_NMAP[ip][domain]["ports"]:
                    if port != "":
                        f.write(f'{ip},{domain},{INFO_NMAP[ip][domain]["status"]},{port}\n')

PORT_INFO = { "IP": "",
    "Domains": "",
    "Port": "",
    "Protocol": "",
    "State": "",
    "Service": "",
    "Product": "",
    "Version": "",
    "Extra Info": "",
    "NMAP Script ID": ""
}

ALL_HOSTS = []

def xml_parser(input_file):
    global PORT_INFO
    global ALL_HOSTS

    content = []
    #Read XML content 
    #(without first two lines that contain details about launched command and nmap version)
    with open(input_file, "r") as f:
        # Read each line in the file, readlines() returns a list of lines
        content = f.readlines()
        content = "".join(content[1:])
        # Combine the lines in the list into a string
        bs_content = BeautifulSoup(content, "lxml")
        #Find all hosts
        hosts = bs_content.find_all("host")
        
        #Find all discovered ports for each host
        for h in hosts:
            IP_address = h.find("address")["addr"]
            hostnames = h.find("hostnames")
            
            domains_str = ''

            if hostnames:
                domain_tags = hostnames.find_all("hostname")
                if domain_tags:
                    domains = [d["name"] for d in domain_tags if 'name' in d.attrs]
                    domains_str = " | ".join(domains)

            open_ports = h.find("ports")
            
            if open_ports:
                ports = open_ports.find_all("port")

                if ports:
                    for p in ports:
                        p_info = deepcopy(PORT_INFO)
                        p_info["IP"] = IP_address
                        p_info["Domains"] = domains_str

                        if "protocol" in p.attrs:
                            p_info["Protocol"] = p["protocol"]

                        if "portid" in p.attrs:
                            p_info["Port"] = p["portid"]
                    
                        state_info = p.find("state")
                        if state_info:
                            if "state" in state_info.attrs:
                                p_info["State"]=state_info["state"]
                        
                        script = p.find("script")
                        if script and ("id" in script.attrs):
                            p_info["NMAP Script ID"] = script["id"]
                        service = p.find("service")
                        
                        if service:
                            if "name" in service.attrs:
                                p_info["Service"] = service["name"]
                            
                            if "product" in service.attrs:
                                p_info["Product"] = service["product"]
                            
                            if "version" in service.attrs:
                                p_info["Version"] = service["version"]
                            
                            if "extrainfo" in service.attrs:
                                p_info["Extra Info"] = service["extrainfo"]

                        ALL_HOSTS.append(p_info)

def write_xml_results(path_no_extension):
    global PORT_INFO
    global ALL_HOSTS

    with open(f'{path_no_extension}_xml.csv', "w") as f:
        f.write(", ".join(list(PORT_INFO.keys()))+"\n")
        
        for info in ALL_HOSTS:
            f.write(", ".join(list(info.values()))+"\n")

def input_parameters():
    """
    Parse command line parameters.

    Return
    ----------
    input_file (str): Name of gnmap/xml file with scan results.
    """    
    
    #Define argument parser
    parser = argparse.ArgumentParser()

    #Create command line arguments
    parser.add_argument('--input', '-in', dest='input_file', help='Input file with nmap results (.gnmap, .xml estension).')
    
    #Parse command line arguments
    args = parser.parse_args()

    #Ask user input filename if not provided as command line argument
    input_file=args.input_file
    wrong_format = True
    while (not input_file) or input_file=='' or (not os.path.exists(input_file)) or (not(os.path.splitext(input_file)[1] in NMAP_FORMATS)):
        print('_Input file_')
        input_file = input()

    return input_file

def main():
    #Read CLI arguments
    input_filename = input_parameters()
    path_no_extension, extension = os.path.splitext(input_filename)

    if extension == ".gnmap":
        #Parse input gnmap file 
        gnmap_parser(input_filename)
        #Store parsed info in a csv file
        write_gnmap_results(path_no_extension)
    elif extension == ".xml":
        #Parse input XML file and return list of ports 
        xml_parser(input_filename)
        #Store parsed info in a csv file
        write_xml_results(path_no_extension)

if __name__=="__main__":
    main()