from fileinput import filename
import json
import os
import requests


key = ""


def get_cms_name(domain):
    filename = "responses/" + domain+'.json'

    # if the file exists, read it
    if (os.path.isfile(filename)):
        with open(filename, 'r') as f:
            json_response = json.load(f)
    else:
        request = requests.get(
            'https://api.builtwith.com/v19/api.json?KEY='+key+'&LOOKUP=' + domain)
        json_response = request.json()

    with open(filename, 'w') as outfile:
        json.dump(json_response, outfile)

    technologies = json_response['Results'][0]['Result']['Paths'][0]['Technologies']

    cms_data = []
    shop_exists = False

    for tech in technologies:
        if tech['Tag'] == 'cms' or tech['Tag'] == 'shop':
            cms_data.append(tech)
            if tech['Tag'] == 'shop':
                shop_exists = True

    latest = 0
    latest_cms = ''

    for cms in cms_data:
        if shop_exists and cms['Tag'] != 'shop':
            continue

        if cms['LastDetected'] > latest:
            latest = cms['LastDetected']
            # if Parent key exists, use that instead of Name
            if 'Parent' in cms:
                latest_cms = cms['Parent']
            else:
                latest_cms = cms['Name']

    if latest_cms == '':
        latest_cms = 'Unknown'

    return latest_cms


# get domains from domains.txt file read line by line
domains = []
with open('domains.txt', 'r') as f:
    for line in f:
        domains.append(line.strip())

cms_names = []

for domain in domains:
    cms = get_cms_name(domain)
    cms_names.append(cms)

# print cms names and usages in percentage
total_cms_names = len(cms_names)

for cms in cms_names:
    print(cms, ':', (cms_names.count(cms) / total_cms_names) * 100)
