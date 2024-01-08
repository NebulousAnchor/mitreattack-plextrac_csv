#!/usr/bin/env python3

import requests
import sys
import argparse
import pandas as pd
import numpy as np
import mitreattack.attackToExcel.attackToExcel as attackToExcel
import mitreattack.attackToExcel.stixToDf as stixToDf

r = ''

# Initialize parser
parser = argparse.ArgumentParser(description = "Convert MITRE ATT&CK Excel spreadsheet to PlexTrac CSV file")

# Adding optional argument
parser.add_argument("-d", "--domain", help = "MITRE ATT&CK Domain e.g: enterprise-attack, ics-attack, mobile-attack", required=True)
parser.add_argument("-a", "--API", action='store_true', help = "PlexTrac API URL Non-MFA")
#parser.add_argument("-m", "--MFA", action='store_true', help = "PlexTrac API URL MFA")
parser.add_argument("-t", "--tenant", action="store", type=str, help = "PlexTrac Tenant")   
parser.add_argument("-U", "--username", help = "PlexTrac Username")
parser.add_argument("-P", "--password", help = "PlexTrac Password")
#parser.add_argument("-T", "--token", help = "PlexTrac Token")
parser.add_argument("-r", "--repository", help = "PlexTrac Repository ID")

# Read arguments from command line
args = parser.parse_args()

if args.domain: 
    domain = args.domain
else:
    parser.print_help()
    sys.exit(0)

if args.API and not args.tenant:
    parser.print_help()
    sys.exit(0)
#elif args.MFA and not args.tenant:
#    parser.print_help()
#    sys.exit(0)


# Define the API endpoint URL
# if args.MFA:
#     api_url = "https://" + args.tenant + "/api/v1/authenticate/mfa"
#     if args.token:
#         token = args.token
#     else:
#         parser.print_help()
#         sys.exit(0)
if args.API:
    if (args.username and args.password):
        api_url = "https://" + args.tenant + "/api/v1/authenticate"
        username = args.username
        password = args.password
    else:
        parser.print_help()
        sys.exit(0)

    
# List of columns to be extracted into new dataframe
extract_col = ['target name', 'description', 'mapping description', 'url', 'ID', 'name', 'detection', 'source ID', 'source name', 'tactics']

# Column remapping list
rename_col = {'target name': 'title', 'mapping description': 'recommendations', 'url': 'references', 'ID': 'MITRE Technique ID', 'name': 'MITRE Technique Name', 'detection': 'MITRE Technique Detection', 'source ID': 'MIRE Mitigation ID', 'source name': 'MITRE Mitigation Name', 'tactics': 'MITRE Technique Tactics'}

# Create an instance of the Att&ck dataset
attackdata = attackToExcel.get_stix_data(domain)
techniques_data = stixToDf.techniquesToDf(attackdata, domain)

# Merge the techniques and associated mitigations dataframes
data = pd.merge(techniques_data["techniques"], techniques_data["associated mitigations"], left_on='ID', right_on='target ID')

# Extract columns from the merged dataframe
data2 = data.loc[:, extract_col]

# Rename columns and add new columns need by PlexTrac
data2 = data2.rename(columns=rename_col)
data2.insert(1, "severity", "medium", allow_duplicates=False)
data2.insert(5, "tags", '', allow_duplicates=False)

# Add Identifier to 'Title' column if there are duplicate titles
data2['title'] = np.where(data2['title'].duplicated(keep=False),data2['title'] + '-' + data2.groupby('title').cumcount().add(1).astype(str),data2['title'])

csv_name = 'MITRE_to_PlexTrac_' + domain + '.csv'
# Save the DataFrame to a CSV file
data2.to_csv(csv_name, index=False)


# Authenticate to PlexTrac API
# if args.MFA:
#     headers = {'Authorization': 'Bearer ' + token}
#     response = requests.post(api_url, headers=headers)
#     if response.status_code == 200:
#         print("Authentication Successful")
#     else:
#         print("Authentication Failed")
#         sys.exit(0)
if args.API:
    if args.tenant:
        tenant = args.tenant
        api_url = "https://" + tenant + "/api/v1/authenticate"  
    else:
        parser.print_help()
        sys.exit(0)
    data = {'username': username, 'password': password}
    response = requests.post(api_url, data=data)
    r = response.json()
    if response.status_code == 200:
        print("Authentication Successful")
    else:
        print("Authentication Failed")
        sys.exit(0)

# Upload CSV to PlexTrac
if args.API or args.MFA:
    if args.repository:
        repository = args.repository
        tenant = args.tenant
    else:
        parser.print_help()
        sys.exit(0)
    api_url = "https://" + tenant + "/api/v2/writeups/import/csv"
    headers = {'Authorization': 'Bearer ' + r['token']}
    files = {'file': open(csv_name, 'rb')}
    data = {'repositoryId': repository}
    response = requests.post(api_url, headers=headers, files=files, data=data)
    if response.status_code == 200:
        print("CSV Upload Successful")
    else:
        print("CSV Upload Failed")
        sys.exit(0)
