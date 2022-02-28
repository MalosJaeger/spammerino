import logging
import itertools

from dns import resolver


def get_mx_records(domain: str) -> dict:
    # more checks to see if domain is root domain or not?
    try:
        mx_records = resolver.resolve(domain, 'MX', lifetime=30)
        exchanges = [record.to_text().split()[1] for record in mx_records]
    except (resolver.NoAnswer, resolver.NXDOMAIN, resolver.NoNameservers) as err:
        exchanges = []
        logging.warning(f'DNS error while querying for MX records for {domain}. Error: {str(err)}')

    logging.debug(f'Found {len(exchanges)} MX records for {domain}')
    return {'domain': domain, 'mx_records': exchanges}


def verify_email_address(email_address: str, mail_server: str) -> bool:
    try:
        with smtplib.SMTP('localhost', 2525) as smtp:
            smtp.helo()
            resp = smtp.rcpt(email_address)

            if resp[0] == 550:
                return False

    except smtplib.SMTPException as err:
        logging.warning(f'SMTPLib error {str(err)}')

    return False


def merge_common_emails_with_domains(emails_file: str, domains_file: str) -> list:
    with open(emails_file, 'r') as emails_fd:
        common_emails = emails_fd.readlines()
        common_emails = [email.strip() for email in common_emails]
    
    with open(domains_file, 'r') as domains_fd:
        domains = domains_fd.readlines()
        domains = [domain.strip() for domain in domains]
    
    emails_as_tuples = list(itertools.product(common_emails, domains))
    return [email + '@' + domain for email, domain in emails_as_tuples]

if __name__ == '__main__':
    possible_emails = merge_common_emails_with_domains('lists/common_groups.txt', 'lists/domains.txt')
    print(len(possible_emails))
    with open('lists/possible_email_combinations.txt', 'w') as emails_fd:
        emails_fd.write('\n'.join(possible_emails) + '\n')