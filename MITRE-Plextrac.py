import sys
import argparse
import pandas as pd
import numpy as np
import mitreattack.attackToExcel.attackToExcel as attackToExcel
import mitreattack.attackToExcel.stixToDf as stixToDf

# Initialize parser
parser = argparse.ArgumentParser(description = "Convert MITRE ATT&CK Excel spreadsheet to PlexTrac CSV file")

# Adding optional argument
parser.add_argument("-d", "--Domain", help = "MITRE ATT&CK Domain e.g: enterprise-attack, ics-attack, mobile-attack")

# Read arguments from command line
args = parser.parse_args()

if args.Domain: 
    domain = args.Domain
else:
    print("Domain not specified, using enterprise-attack")
    domain = "enterprise-attack"

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

# Save the DataFrame to a CSV file
data2.to_csv('MITRE_to_PlexTrac_' + domain + '.csv', index=False)

