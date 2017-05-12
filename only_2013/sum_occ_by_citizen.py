#!/usr/bin/env python

from collections import defaultdict
import csv

OCCUPATIONS = {
    '3010': 'Dentists',
    '3040': 'Optometrists',
    '3050': 'Pharmacists',
    '3060': 'Physicians and Surgeons',
    '3110': 'Physicians Assistants',
    '3255': 'Registered Nurses'
}

CITIZEN = {
    '0': 'N/A',
    '1': 'Born abroad of American parents',
    '2': 'Naturalized citizen',
    '3': 'Not a citizen',
    '4': 'Not a citizen, but has received first papers',
    '5': 'Foreign born, citizenship status not reported'
}

output = defaultdict(lambda: defaultdict(lambda: 0))

print('Reading data')

with open('usa_00008.csv') as f:
    reader = csv.DictReader(f)

    for i, row in enumerate(reader):
        if i % 100000 == 0:
            print(i)

        if row['OCC'] not in OCCUPATIONS:
            continue

        occ = OCCUPATIONS[row['OCC']]
        citizen = CITIZEN[row['CITIZEN']]

        output[occ][citizen] += int(row['PERWT'])

print('Writing output')

with open('sum_occ_by_citizen.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['occ', 'citizen', 'count'])

    for occ, citizens in output.items():
        for citizen, count in citizens.items():
            writer.writerow([occ, citizen, count])
