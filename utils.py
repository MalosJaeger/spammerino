import logging

from dns import resolver


def get_mx_records(domain: str) -> dict:
    # more checks to see if domain is root domain or not?
    try:
        mx_records = resolver.resolve(domain, 'MX')
        exchanges = [record.to_text().split()[1] for record in mx_records]
    except (resolver.NoAnswer, resolver.NXDOMAIN, resolver.NoNameservers) as err:
        exchanges = []
        logging.warning(f'DNS error while querying for MX records for {domain}. Error: {str(err)}')

    logging.debug(f'Found {len(exchanges)} MX records for {domain}')
    return {'domain': domain, 'mx_records': exchanges}