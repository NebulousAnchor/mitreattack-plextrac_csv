# mitreattack-plextrac_csv
Simple Python script to create findings database as CSV for import to PlexTrac


## install requirements first
``pip install -r requirements.txt``

## Run mitreattack-plextrac_csv
```
python3 mitreattack-plextrac_csv.py 

usage: MITRE-Plextrac.py [-h] [-d DOMAIN]

Convert MITRE ATT&CK Excel spreadsheet to PlexTrac CSV file

options:
  -h, --help            show this help message and exit
  -d DOMAIN, --Domain DOMAIN
                        MITRE ATT&CK Domain e.g: enterprise-attack, ics-attack, mobile-attack
```

## Specify a domain to use
```
python3 mitreattack-plextrac_csv.py -d enterprise-attack
2024-01-05 13:57:04.785 | INFO     | mitreattack.attackToExcel.attackToExcel:get_stix_data:69 - Downloading ATT&CK data from github.com/mitre/cti
parsing techniques: 100%|███████████████████████████| 625/625 [00:00<00:00, 2798.17it/s]
parsing relationships for type=technique: 100%|████████████████████████| 17202/17202 [00:00<00:00, 29649.17it/s]
```
## Example of the data
```
                                 title severity                                        description                                    recommendations                                 references tags MITRE Technique ID               MITRE Technique Name                          MITRE Technique Detection MIRE Mitigation ID                    MITRE Mitigation Name                MITRE Technique Tactics
0  Abuse Elevation Control Mechanism-1   medium  Adversaries may circumvent mechanisms designed...  Check for common UAC bypass weaknesses on Wind...  https://attack.mitre.org/techniques/T1548                   T1548  Abuse Elevation Control Mechanism  Monitor the file system for files that have th...              M1047                                    Audit  Defense Evasion, Privilege Escalation
1  Abuse Elevation Control Mechanism-2   medium  Adversaries may circumvent mechanisms designed...  System settings can prevent applications from ...  https://attack.mitre.org/techniques/T1548                   T1548  Abuse Elevation Control Mechanism  Monitor the file system for files that have th...              M1038                     Execution Prevention  Defense Evasion, Privilege Escalation
2  Abuse Elevation Control Mechanism-3   medium  Adversaries may circumvent mechanisms designed...  Applications with known vulnerabilities or kno...  https://attack.mitre.org/techniques/T1548                   T1548  Abuse Elevation Control Mechanism  Monitor the file system for files that have th...              M1028           Operating System Configuration  Defense Evasion, Privilege Escalation
3  Abuse Elevation Control Mechanism-4   medium  Adversaries may circumvent mechanisms designed...  Remove users from the local administrator grou...  https://attack.mitre.org/techniques/T1548                   T1548  Abuse Elevation Control Mechanism  Monitor the file system for files that have th...              M1026            Privileged Account Management  Defense Evasion, Privilege Escalation
4  Abuse Elevation Control Mechanism-5   medium  Adversaries may circumvent mechanisms designed...  The sudoers file should be strictly edited suc...  https://attack.mitre.org/techniques/T1548                   T1548  Abuse Elevation Control Mechanism  Monitor the file system for files that have th...              M1022  Restrict File and Directory Permissions  Defense Evasion, Privilege Escalation
```
