#######################
# @author: RaffaDNDM
# @date:   2022-02-27
#######################

import csv
from termcolor import cprint, colored
import pyfiglet
import socket
import utility

class TCPScanner:
    '''
    Sequential TCP port scanner.

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
        self.ip_address = utility.IP_from_host(remote_host)
        cprint(colored('Target IP address: ', 'red')+self.ip_address, end='\n\n')

        with open('dat/TCP_ports.csv', mode='r') as f:
            csv_reader = csv.reader(f, delimiter=',')
            self.TCP_ports = {int(row[0]):row[1] for row in csv_reader}


    def scan(self):        
        '''
        Scan all the known TCP ports.
        '''
        
        count = 0
        count_open = 0

        try:
            #Scan sequentially all the known TCP ports
            for port in self.TCP_ports:
                count += 1

                #If the port is open, add it to the list of open ports
                if self.is_open(port):
                    count_open += 1
                    self.OPEN_PORTS[port] = self.TCP_ports[port]

        except KeyboardInterrupt:
            pass  

        print('Number of scanned ports: '+colored(f'{count}','yellow'))
        print('Number of open ports: '+colored(f'{count_open}','yellow'))
        cprint('_________________________________________________', 'blue')
        
        for port in self.OPEN_PORTS:
            print(colored(f'{port}', 'green')+\
                          f' {self.OPEN_PORTS[port]} '+\
                          colored('---> ', 'green') +\
                          colored('OPEN', 'yellow'))

        cprint('_________________________________________________\n', 'blue')


    def is_open(self, port):
        '''
        Scan a single TCP port.

        Args:
            port (int): TCP port to be scanned
        
        Returns:
            state (bool): True if open port, False otherwise
        '''

        #Create TCP socket
        sd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #Set timeout
        sd.settimeout(1.0)
        #Test if port is open
        state = sd.connect_ex((self.ip_address, port))
        #Close the TCP socket
        sd.close()
        
        return state==0

def main():
    title = pyfiglet.figlet_format("TCP Port Scanner") 
    cprint(title, 'blue')
    cprint('_________________________________________________', 'blue')
    remote_host = input(colored('Insert the IP address or the domain name: \n','blue'))
    
    print('')
    scanner = TCPScanner(remote_host)
    cprint('\nOpen Ports on IP address', 'blue')
    scanner.scan()

if __name__=='__main__':
    main()