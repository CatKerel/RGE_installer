import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import pandas as pd

url = 'https://www.qualit-enr.org/annuaire/?type=installateurs-photovoltaique&ville=01'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
ua = UserAgent().random
header = {'user-agent': ua}

table = soup.find('div', class_='results-list')
rows = table.find_all('a')
hrefs = [row.get('href') for row in rows]
print(len(hrefs))
columns = ['Name', 'Address', 'Postcode', 'City', 'Telephone number', 'Out skills', 'Certificates']
data = pd.DataFrame(columns=columns)

for ref in hrefs:
    ref_soup = BeautifulSoup(requests.get(ref, headers=header).text, 'html.parser')
    name = ref_soup.find('h1').text
    address = '\n'.join([add.strip() for add in ref_soup.find('div', class_='fs-lg lh-md').text.strip().split(sep='\n')[:-1]]).strip()
    postcode = ref_soup.find('div', class_='fs-lg lh-md').text.strip().split(sep='\n')[-1].strip()
    city = postcode[postcode.find(' ') + 1:]
    postcode = postcode[:postcode.find(' ')]
    certificates = [a.get('href') for a in ref_soup.find_all('a', class_='link-download')]
    certificates_str = '\n'.join(certificates)
    skills = [skill.text for skill in
              ref_soup.find('div', class_='col-lg-6 md-down-mb-lg').find_all('div', class_='cms')]
    skills_str = '\n'.join(skills)
    phone = ref_soup.find('div', class_='phone-container').text.strip()
    data = pd.concat([data, pd.DataFrame(data=[[name, address, postcode, city, phone, skills_str, certificates_str]],
                                         columns=columns)],
                     axis=0, ignore_index=True)
    print(name)

data.to_excel('result.xlsx', index=False)