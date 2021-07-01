import argparse
import os
import sys

import idna
import requests


def check_domain(domain_name):
    post_data = {
        'domain_browser[domain]': domain_name,
        'domain_browser[lang]': 'en',
    }
    domain_check = requests.post('https://www.dns.pl/api/domain-browser', post_data)

    if domain_check.status_code == 200:
        response = domain_check.json()
        if not response['apiResponse']['errors'] and response['apiResponse']['results']:
            if list(response['apiResponse']['results'].values())[0] == 0:
                return {
                    'domain': list(response['apiResponse']['results'].keys())[0],
                    'results': True,  # Probably not registered
                }
            else:
                return {
                    'domain': list(response['apiResponse']['results'].keys())[0],
                    'results': False,  # Probably registered
                }
        else:
            return {
                'domain': list(response['apiResponse']['errors'].keys())[0],
                'results': False,  # Error, probably wrong domain
            }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Checking if the domain is registered using dns.pl API. If it '
                                                 'doesn\'t, there is a good chance that it can be free.')
    requiredParser = parser.add_argument_group('required arguments')
    requiredParser.add_argument('-p', '--process', action='store', type=str, required=True, help='File to process')
    parser.add_argument('-o', '--output', action='store', type=str, help='Output file')

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
            check_domain_results = check_domain(domain)
            if check_domain_results['results'] is True:
                print(f'{check_domain_results["domain"]}: {check_domain_results["results"]}')
                output_file.write(domain)
                output_file.write('\n')
        output_file.close()
    else:
        for row in input_file:
            domain = idna.encode(row.strip()).decode('utf-8')
            check_domain_results = check_domain(domain)
            if check_domain_results['results'] is True:
                print(f'{check_domain_results["domain"]}: {check_domain_results["results"]}')
    input_file.close()
