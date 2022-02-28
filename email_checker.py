import json
import logging
import src.utils

from multiprocessing import Queue, Pool

# INITIAL BASE CONFIGS
#logging.basicConfig(level=logging.DEBUG)


# METHODS
def parse_email_servers(domains: list[str]) -> dict:
    mail_servers = {}

    with Pool(3) as p:
        mail_servers = p.map(utils.get_mx_records, domains)
        return mail_servers
    

def dump_email_servers(domains_file: str, output_file: str):
    with open(domains_file, 'r') as domains_fd:
        malicious_domains = domains_fd.readlines()
        malicious_domains = [domain.strip() for domain in malicious_domains]

        mail_servers = parse_email_servers(malicious_domains)
        with open(output_file, 'w') as output_fd:
            output_fd.write(json.dumps(mail_servers))


if __name__ == '__main__':
    dump_email_servers('lists/domains.txt', 'lists/mail_servers.json')