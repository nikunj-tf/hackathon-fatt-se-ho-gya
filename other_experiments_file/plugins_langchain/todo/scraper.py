import os

import dns
import dns.resolver
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
import tldextract

OUTPUT_DIR = 'scraped_data'


def get_subdomains(domain):
    subdomains = set()
    ext = tldextract.extract(domain)
    url = ext.domain + '.' + ext.suffix
    for r in dns.resolver.resolve(url, 'CNAME'):
        subdomains.add(str(r.target).rstrip('.'))
    print(subdomains)
    return subdomains


# def get_subdomains(domain):
#     subdomains = []
#     # get the root domain
#     root_domain = urlparse(domain).hostname
#     print(root_domain)
#     if root_domain is not None:
#         # check for www subdomain
#         subdomains.append('www')
#         # get all other subdomains
#         for i in range(len(root_domain.split('.'))):
#             subdomain = '.'.join(root_domain.split('.')[i:])
#             subdomains.append(subdomain)
#     else:
#         print("Root domain None:")
#     return subdomains


def scrape_subdomain(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        # extract the webpage content here
        content = soup.get_text()
        # write content to a file
        parsed_url = urlparse(url)
        output_file = f'{OUTPUT_DIR}/{parsed_url.hostname}{parsed_url.path.replace("/", "-")}.txt'
        with open(output_file, 'w') as f:
            f.write(content)
        print(f'Successfully scraped {url} and wrote data to {output_file}')
    else:
        print(f'Error scraping {url}: status code {response.status_code}')


def scrape_domain(domain):
    subdomains = get_subdomains(domain)
    # os.makedirs(OUTPUT_DIR, exist_ok=True)
    # for subdomain in subdomains:
    #     url = f'https://{subdomain}.{domain}'
    #     scrape_subdomain(url)

if __name__ == '__main__':
    domain = 'https://www.truefoundry.com/'
    scrape_domain(domain)

