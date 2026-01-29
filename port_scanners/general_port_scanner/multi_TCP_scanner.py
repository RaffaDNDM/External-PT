#######################
# @author: RaffaDNDM
# @date:   2022-02-27
#######################

import csv
from termcolor import cprint, colored
import pyfiglet
import socket
import utility
import os
from multiprocessing.pool import ThreadPool

class TCPScanner:
    '''
    Multi-threaded TCP port scanner.

    Args:
        remote_host (str): Remote host to be solved and analysed

    Attributes:
        OPEN_PORTS (dict): Dictionary of open ports and related services

        ip_address (str): IP address obtained from DNS resolution of remote
                          host

        TCP_ports (dict): Dictionary of known TCP ports and related services 
                          to be analysed by the program
    '''

    OPEN_PORTS = {}

    def __init__(self, remote_host):
        #IP address of remote host
        self.ip_address = utility.IP_from_host(remote_host)
        cprint(colored('Target IP address: ', 'red')+self.ip_address, end='\n\n')

        #Dictionary of TCP ports and related services
        with open('dat/TCP_ports.csv', mode='r') as f:
            csv_reader = csv.reader(f, delimiter=',')
            self.TCP_ports = {int(row[0]):row[1] for row in csv_reader}


    def scan(self):
        '''
        Scan all the known TCP ports.
        '''

        try:
            #Number of threads = number of virtual processors
            workers_num = os.cpu_count()
            
            #Each thread analyses a TCP port of TCP_ports
            #by using the function is_open.
            #When a thread terminates the analysis of a TCP
            #port, it will analyse another TCP port  
            with ThreadPool(workers_num) as pool:
                for loop_index, _ in enumerate(pool.imap(self.is_open, self.TCP_ports)):
                    print(colored(f'\r{loop_index/len(self.TCP_ports)*100:.2f}%', 'yellow')+' ports scanned.', end='')

        except KeyboardInterrupt:
            pass  

        cprint('\n_________________________________________________', 'blue')
        
        for port in self.OPEN_PORTS:
            print(colored(str(port), 'green')+' '+\
                          str(self.OPEN_PORTS[port])+' '+\
                          colored('---> ', 'green') +\
                          colored('OPEN', 'yellow'))

        cprint('_________________________________________________\n', 'blue')


    def is_open(self, port):
        '''
        Scan a single TCP port.

        Args:
            port (int): TCP port to be scanned
        '''

        #Create TCP socket
        sd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #Set timeout
        sd.settimeout(1.0)
        #Test if port is open
        state = sd.connect_ex((self.ip_address, port))
        #Close the TCP socket
        sd.close()

        #Port open
        if state == 0:
            self.OPEN_PORTS[port] = self.TCP_ports[port]


def main():
    title = pyfiglet.figlet_format("TCP Port Scanner") 
    cprint(title, 'blue')
    cprint('_________________________________________________', 'blue')
    remote_host = input(colored('Insert the IP address or the domain name: \n','blue'))
    
    print('')
    scanner = TCPScanner(remote_host)
    cprint('Open Ports on IP address', 'blue')
    scanner.scan()


if __name__=='__main__':
    main()