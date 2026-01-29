#######################
# @author: RaffaDNDM
# @date:   2022-02-27
#######################

import nmap
import argparse
import utility
from termcolor import cprint, colored

'''
Parser of command line arguments
'''
def args_parser():
    #Parser of command line arguments
    parser = argparse.ArgumentParser()
    
    #Initialization of needed arguments
    parser.add_argument("-address", "-a", "-ip", dest="ip_address", help="IP address to be scanned")
    parser.add_argument("-port", "-p", dest="ports", help="Ports to be scanned")
 
    #Parse command line arguments
    args = parser.parse_args()
    
    #Check if the arguments have been specified on command line
    if (not args.ip_address) or (not args.ports):
        parser.print_help()
        exit(0)
    
    return utility.IP_from_host(args.ip_address), args.ports

def main():
    ip_address, ports = args_parser()
    scanner = nmap.PortScanner()
    scanner.scan(ip_address, ports)

    # run a loop to print all the found result about the ports
    for host in scanner.all_hosts():
        print(colored('\nTarget IP address : ', 'green')+f'{host} ({scanner[host].hostname()})')
        print(colored('State of remote host: ', 'cyan')+str(scanner[host].state()), end='\n\n')
        for proto in scanner[host].all_protocols():
            cprint(proto.upper(), 'blue')
            cprint('_______________________________________', 'blue')

            lport = list(scanner[host][proto].keys())
            lport.sort()
            for port in lport: 
                print (colored(str(port), 'green')+' ----> '+colored(scanner[host][proto][port]['state'].upper(), 'yellow'))

            cprint('_______________________________________', 'blue', end='\n\n')

if __name__=='__main__':
    main()