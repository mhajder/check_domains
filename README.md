# check_domains

Check if the domain is free by checking if the SOA record exists.


## Installation

Install requirements using pip:

```shell script
pip install -r requirements.txt
```

## Generating a list of domains

The easiest way is to use the [crunch](https://sourceforge.net/projects/crunch-wordlist/).

### Examples:

To generate a list consisting of 2-character domains (numbers and letters) for the **.pl**. Just run the command:

```shell script
crunch 5 5 0123456789abcdefghijklmnopqrstuvwxyz -t @@.pl -o domains.txt
```

To generate a list consisting of 3-character domains (letters only) for the **.pl**. Just run the command:

```shell script
crunch 6 6 abcdefghijklmnopqrstuvwxyz -t @@@.pl -o domains.txt
```

## Usage

To view help:

```shell script
python check_domains.py
```

Help:

```shell script
usage: check_domains.py [-h] -p PROCESS [-o OUTPUT]

Checking if the domain has SOA records. If it doesn't, there is a good chance
that it can be free.

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Optional output file

required arguments:
  -p PROCESS, --process PROCESS
                        File to process
```

To start checking domains:

```shell script
python check_domains.py -p domains.txt
```
where `domains.txt` is your domains file to check

To start checking domains and saving the output:

```shell script
python check_domains.py -p domains.txt -o output.txt
```
where `domains.txt` is your domains file to check and `output.txt` is a file with domains that can be free