import argparse
import os
import sys

import idna
import requests


# To-do
# * checking if a given domain (extensions) exists/is correct
# * the ability to add entire links so that the script pulls the domain out by itself
# def get_domains():
#     domains_fetch = requests.get('https://data.iana.org/TLD/tlds-alpha-by-domain.txt')
#     domains_fetch = domains_fetch.text
#     domains = domains_fetch.strip().split('\n')
#     return domains[1:]


def check_domain(domain_name, errors):
    headers = {'Accept': 'application/dns-json'}
    domain_check = requests.get(f'https://cloudflare-dns.com/dns-query?type=SOA&name={domain_name}.', headers=headers)
    if domain_check.status_code == 200:
        response = domain_check.json()
        if errors is True:
            if 'Status' in response:
                if response['Status'] == 3:
                    return False
                else:
                    return True
            else:
                return True
        else:
            if 'Status' in response:
                if response['Status'] == 0:
                    return True
                else:
                    return False
            else:
                return False


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Checking if the domain has SOA records. If it doesn\'t, there is a '
                                                 'good chance that it can be free.')
    requiredParser = parser.add_argument_group('required arguments')
    requiredParser.add_argument('-p', '--process', action='store', type=str, required=True, help='File to process')
    parser.add_argument('-o', '--output', action='store', type=str, help='Output file')
    parser.add_argument('-e', '--errors', action='store_true', default=False, help='DNS errors as registered domains')

    if len(sys.argv) == 1:
        # display help message when no args are passed.
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    if not os.path.isfile(args.process):
        print('File path {} does not exist. Exiting...'.format(args.process))
        sys.exit()

    input_file = open(args.process, mode='r', newline='', encoding="utf-8")
    if args.output is not None:
        output_file = open(args.output, mode='a', newline='', encoding="utf-8")
        for row in input_file:
            domain = idna.encode(row.strip()).decode('utf-8')
            has_soa = check_domain(domain, args.errors)
            if has_soa is False:
                print(f'{domain}: {has_soa}')
                output_file.write(domain)
                output_file.write('\n')
        output_file.close()
    else:
        for row in input_file:
            domain = idna.encode(row.strip()).decode('utf-8')
            has_soa = check_domain(domain, args.errors)
            if has_soa is False:
                print(f'{domain}: {has_soa}')
    input_file.close()
