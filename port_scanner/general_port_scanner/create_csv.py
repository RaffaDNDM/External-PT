#######################
# @author: RaffaDNDM
# @date:   2022-02-27
#######################

import csv

with open('dat/all_ports.csv', mode='r') as f, \
     open('dat/UDP_ports.csv', mode='w') as udp_f, \
     open('dat/TCP_ports.csv', mode='w') as tcp_f:

    csv_reader = csv.reader(f, delimiter=',')
    csv_udp = csv.writer(udp_f, delimiter=',', lineterminator='\n')
    csv_tcp = csv.writer(tcp_f, delimiter=',', lineterminator='\n')

    for row in csv_reader:
        if row[2] == 'udp':
            csv_udp.writerow([row[1], row[0]])
        elif row[2] == 'tcp':
            csv_tcp.writerow([row[1], row[0]])