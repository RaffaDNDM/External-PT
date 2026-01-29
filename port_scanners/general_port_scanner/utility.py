#######################
# @author: RaffaDNDM
# @date:   2022-02-27
#######################

import socket
from termcolor import cprint

def IP_from_host(remote_host):
    '''
    DNS resolution of the remote host.

    Args:
        remote_host (str): Remote host address

    Returns:
        ip_addr (str): IP address obtained from the DNS resolution
                       of remote_host
    '''

    try:
        ip_addr = socket.gethostbyname(remote_host)
    except socket.gaierror:
        cprint('Error in the remote address specified.', 'red')
        exit()

    return ip_addr