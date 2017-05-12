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

output = defaultdict(lambda: defaultdict(lambda: 0))

print('Reading data')

with open('usa_00009.csv') as f:
    reader = csv.DictReader(f)

    for i, row in enumerate(reader):
        if i % 100000 == 0:
            print(i)

        if row['OCC'] not in OCCUPATIONS:
            continue

        occ = OCCUPATIONS[row['OCC']]
        year = row['YRIMMIG']

        output[occ][year] += int(row['PERWT'])

print('Writing output')

with open('sum_occ_by_year.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['occ', 'year', 'count'])

    for occ, years in output.items():
        for year, count in years.items():
            writer.writerow([occ, year, count])
