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
