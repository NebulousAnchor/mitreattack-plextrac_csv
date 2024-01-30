#!/usr/bin/env python3

import requests
import sys
import argparse
import pandas as pd
import numpy as np
import mitreattack.attackToExcel.attackToExcel as attackToExcel
import mitreattack.attackToExcel.stixToDf as stixToDf


# Initialize parser
parser = argparse.ArgumentParser(description = "Convert MITRE ATT&CK Excel spreadsheet to PlexTrac CSV file")

# Adding optional argument
parser.add_argument("-d", "--domain", help = "MITRE ATT&CK Domain e.g: enterprise-attack, ics-attack, mobile-attack")
parser.add_argument("-l", "--list", action='store_true', help = "List all PlexTrac Repositories in Tenant")
parser.add_argument("-a", "--api", action='store_true', help = "PlexTrac API URL Non-MFA")
parser.add_argument("-t", "--tenant", action="store", type=str, help = "PlexTrac Tenant")   
parser.add_argument("-U", "--username", action="store", type=str, help = "PlexTrac Username")
parser.add_argument("-P", "--password", action="store", type=str, help = "PlexTrac Password")
parser.add_argument("-r", "--repository", action="store", type=str, help = "PlexTrac Repository ID")
parser.add_argument("-f", "--file", action="store", type=str, help = "If you want to use a local CSV file instead of generating one from MITRE ATT&CK")


# Read arguments from command line
args = parser.parse_args()

# Check for required arguments when using API
if args.api and not (args.tenant and args.username and args.password and args.repository):
    print("When Using PlexTrac API you must specify the following arguments: Tenant, Username, Password, Repository\n")
    parser.print_help()
    sys.exit(0)

if args.list and not (args.tenant and args.username and args.password):
    print("When Using PlexTrac API you must specify the following arguments: Tenant, Username, Password, Repository\n")
    parser.print_help()
    sys.exit(0)
elif args.list:
    # Define the API endpoint URL
    auth_url = "https://" + args.tenant + "/api/v1/authenticate"
    data = {'username': args.username, 'password': args.password}
    response = requests.post(auth_url, data=data)
    r = response.json()
    if response.status_code == 200:
        print("Authentication Successful")
    else:
        print("Authentication Failed")
        sys.exit(0)
    api_url = "https://" + args.tenant + "/api/v2/repositories/getAllWriteupsRepositories"
    headers = {'Authorization': 'Bearer ' + r['token']}
    json = {}
    response = requests.post(api_url, headers=headers, json=json)
    if response.status_code == 200:
        print("List Repositories Successful")
        repos = response.json()
        df = pd.DataFrame(repos["data"], columns=['abbreviation', 'created_at', 'created_by', 'description', 'is_deleted', 'name', 'repository_id', 'repository_type', 'repository_users', 'tenant_id', 'updated_at', 'writeups_count', 'doc_type'])
        output = df.loc[:, ['name','repository_id', 'writeups_count']]
        print(output)
        sys.exit(0)  

if args.file:
    input = open(args.file, 'rb')
    file = {"file": input }   
else:    
    # List of columns to be extracted into new dataframe
    extract_col = ['target name', 'description', 'mapping description', 'url', 'ID', 'name', 'detection', 'source ID', 'source name', 'tactics']

    # Column remapping list [FYI column names are case sensitive and must be lowercase in PlexTrac CSV file]
    rename_col = {'target name': 'title', 'mapping description': 'recommendations', 'url': 'references', 'ID': 'mitre_technique_id', 'name': 'mitre_technique_name', 'detection': 'mitre_technique_detection', 'source ID': 'mitre_mitigation_id', 'source name': 'mitre_mitigation_name', 'tactics': 'mitre_technique_tactics'}

    # Define the MITRE ATT&CK domain
    if not args.domain:
        print("Please specify a MITRE ATT&CK domain\n")
        parser.print_help()
        sys.exit(0)
    # Create an instance of the Att&ck dataset
    attackdata = attackToExcel.get_stix_data(args.domain)
    techniques_data = stixToDf.techniquesToDf(attackdata, args.domain)

    # Merge the techniques and associated mitigations dataframes
    data = pd.merge(techniques_data["techniques"], techniques_data["associated mitigations"], left_on='ID', right_on='target ID')

    # Extract columns from the merged dataframe
    data2 = data.loc[:, extract_col]

    # Rename columns and add new columns need by PlexTrac
    data2 = data2.rename(columns=rename_col)
    data2.insert(1, "severity", "medium", allow_duplicates=False)
    data2.insert(5, "tags", '', allow_duplicates=False)
    data2["tags"] = data2[["mitre_mitigation_id", "mitre_technique_id"]].agg(','.join, axis=1)

    # Add Identifier to 'Title' column if there are duplicate titles
    data2['title'] = np.where(data2['title'].duplicated(keep=False),data2['title'] + '-' + data2.groupby('title').cumcount().add(1).astype(str),data2['title'])

    csv_name = 'MITRE_to_PlexTrac_' + args.domain + '.csv'
    # Save the DataFrame to a CSV file
    data2.to_csv(csv_name, index=False)
    input = open(csv_name, 'rb')
    file = {"file":input}
    
if args.api:
    # Define the API endpoint URL
    auth_url = "https://" + args.tenant + "/api/v1/authenticate"
    data = {'username': args.username, 'password': args.password}
    response = requests.post(auth_url, data=data)
    r = response.json()
    if response.status_code == 200:
        print("Authentication Successful")
    else:
        print("Authentication Failed")
        sys.exit(0)
    api_url = "https://" + args.tenant + "/api/v2/writeups/import/csv"
    headers = {'Authorization': 'Bearer ' + r['token']}
    data = {'repositoryId': args.repository}
    response = requests.post(api_url, headers=headers, files=file, data=data)
    input.close()
    if response.status_code == 200:
        print("CSV Upload Successful")
    else:
        print("CSV Upload Failed")
        sys.exit(0)
