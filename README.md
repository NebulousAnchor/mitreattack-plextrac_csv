# mitreattack-plextrac_csv
Simple Python script to create findings database as CSV for import to PlexTrac

This script specifically maps MITRE Technique ID's (e.g, T1548) with associated MITRE Mitigation ID's (e.g, M1047, M1038, M1028, M1026, M1022) allowing the Technique ID to be usefully duplicated such that you can choose the exact mitigation needed for the finding instead of having all possible mitigations, causing the report recipient to guess what applies to them, or the report writer to remove extraneous information.


## install requirements first
``pip install -r requirements.txt``

## Run mitreattack-plextrac_csv
```
python3 mitreattack-plextrac_csv.py 

usage: MITRE-Plextrac.py [-h] [-d DOMAIN] [-l] [-a] [-t TENANT] [-U USERNAME] [-P PASSWORD] [-r REPOSITORY] [-f FILE]

Convert MITRE ATT&CK Excel spreadsheet to PlexTrac CSV file

options:
  -h, --help            show this help message and exit
  -d DOMAIN, --domain DOMAIN
                        MITRE ATT&CK Domain e.g: enterprise-attack, ics-attack, mobile-attack
  -l, --list            List all PlexTrac Repositories in Tenant
  -a, --api             PlexTrac API URL Non-MFA
  -t TENANT, --tenant TENANT
                        PlexTrac Tenant
  -U USERNAME, --username USERNAME
                        PlexTrac Username
  -P PASSWORD, --password PASSWORD
                        PlexTrac Password
  -r REPOSITORY, --repository REPOSITORY
                        PlexTrac Repository ID
  -f FILE, --file FILE  If you want to use a local CSV file instead of generating one from MITRE ATT&CK
```

## Specify a domain to use for local CSV copy only
```
python3 mitreattack-plextrac_csv.py -d enterprise-attack
2024-01-05 13:57:04.785 | INFO     | mitreattack.attackToExcel.attackToExcel:get_stix_data:69 - Downloading ATT&CK data from github.com/mitre/cti
parsing techniques: 100%|███████████████████████████| 625/625 [00:00<00:00, 2798.17it/s]
parsing relationships for type=technique: 100%|████████████████████████| 17202/17202 [00:00<00:00, 29649.17it/s]
```
## Specify a PlexTrac Tenant and Authentication Information to List Respositiories or Upload to a specific Repository
```
python3 MITRE-Plextrac.py -a -t 'example.plextrac.com' -U '{username}' -P '{password}' -r '{repositoryID}' -d 'enterprise-attack'
2024-01-20 15:22:29.555 | INFO     | mitreattack.attackToExcel.attackToExcel:get_stix_data:69 - Downloading ATT&CK data from github.com/mitre/cti
parsing techniques: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 625/625 [00:00<00:00, 2868.09it/s]
parsing relationships for type=technique: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 17202/17202 [00:00<00:00, 32335.19it/s]
Authentication Successful
CSV Upload Successful
```

## Example of the data
```
                                 title severity                                        description                                    recommendations                                 references         tags  MITRE Technique ID  MITRE Technique Name  MITRE Technique Detection  MIRE Mitigation ID  MITRE Mitigation Name  MITRE Technique Tactics
0  Abuse Elevation Control Mechanism-1   medium  Adversaries may circumvent mechanisms designed...  Check for common UAC bypass weaknesses on Wind...  https://attack.mitre.org/techniques/T1548  T1548,M1047  T1548  Abuse Elevation Control Mechanism  Monitor the file system for files that have th...              M1047                                    Audit  Defense Evasion, Privilege Escalation
1  Abuse Elevation Control Mechanism-2   medium  Adversaries may circumvent mechanisms designed...  System settings can prevent applications from ...  https://attack.mitre.org/techniques/T1548  T1548,M1038  T1548  Abuse Elevation Control Mechanism  Monitor the file system for files that have th...              M1038                     Execution Prevention  Defense Evasion, Privilege Escalation
2  Abuse Elevation Control Mechanism-3   medium  Adversaries may circumvent mechanisms designed...  Applications with known vulnerabilities or kno...  https://attack.mitre.org/techniques/T1548  T1548,M1028  T1548  Abuse Elevation Control Mechanism  Monitor the file system for files that have th...              M1028           Operating System Configuration  Defense Evasion, Privilege Escalation
3  Abuse Elevation Control Mechanism-4   medium  Adversaries may circumvent mechanisms designed...  Remove users from the local administrator grou...  https://attack.mitre.org/techniques/T1548  T1548,M1026  T1548  Abuse Elevation Control Mechanism  Monitor the file system for files that have th...              M1026            Privileged Account Management  Defense Evasion, Privilege Escalation
4  Abuse Elevation Control Mechanism-5   medium  Adversaries may circumvent mechanisms designed...  The sudoers file should be strictly edited suc...  https://attack.mitre.org/techniques/T1548  T1548,M1022  T1548  Abuse Elevation Control Mechanism  Monitor the file system for files that have th...              M1022  Restrict File and Directory Permissions  Defense Evasion, Privilege Escalation
=======
## Example of the data
```
                                 title severity                                        description                                    recommendations                                 references tags MITRE Technique ID               MITRE Technique Name                          MITRE Technique Detection MIRE Mitigation ID                    MITRE Mitigation Name                MITRE Technique Tactics
0  Abuse Elevation Control Mechanism-1   medium  Adversaries may circumvent mechanisms designed...  Check for common UAC bypass weaknesses on Wind...  https://attack.mitre.org/techniques/T1548                   T1548  Abuse Elevation Control Mechanism  Monitor the file system for files that have th...              M1047                                    Audit  Defense Evasion, Privilege Escalation
1  Abuse Elevation Control Mechanism-2   medium  Adversaries may circumvent mechanisms designed...  System settings can prevent applications from ...  https://attack.mitre.org/techniques/T1548                   T1548  Abuse Elevation Control Mechanism  Monitor the file system for files that have th...              M1038                     Execution Prevention  Defense Evasion, Privilege Escalation
2  Abuse Elevation Control Mechanism-3   medium  Adversaries may circumvent mechanisms designed...  Applications with known vulnerabilities or kno...  https://attack.mitre.org/techniques/T1548                   T1548  Abuse Elevation Control Mechanism  Monitor the file system for files that have th...              M1028           Operating System Configuration  Defense Evasion, Privilege Escalation
3  Abuse Elevation Control Mechanism-4   medium  Adversaries may circumvent mechanisms designed...  Remove users from the local administrator grou...  https://attack.mitre.org/techniques/T1548                   T1548  Abuse Elevation Control Mechanism  Monitor the file system for files that have th...              M1026            Privileged Account Management  Defense Evasion, Privilege Escalation
4  Abuse Elevation Control Mechanism-5   medium  Adversaries may circumvent mechanisms designed...  The sudoers file should be strictly edited suc...  https://attack.mitre.org/techniques/T1548                   T1548  Abuse Elevation Control Mechanism  Monitor the file system for files that have th...              M1022  Restrict File and Directory Permissions  Defense Evasion, Privilege Escalation
```
![image](https://github.com/NebulousAnchor/mitreattack-plextrac_csv/assets/40901091/084521b4-ec63-4d83-bee0-2193a4e612ae)
