#!/usr/bin/env python

from collections import defaultdict
import csv

# "YEAR","DATANUM","SERIAL","HHWT","GQ","PERNUM","PERWT","BPL","BPLD","OCC"

OCCUPATIONS = {
    '3010': 'Dentists',
    '3040': 'Optometrists',
    '3050': 'Pharmacists',
    '3060': 'Physicians and Surgeons',
    '3110': 'Physicians Assistants',
    '3255': 'Registered Nurses'
}

BPL = {}

with open('bpl_mapping.csv') as f:
    reader = csv.reader(f)
    header = next(reader)

    for row in reader:
        last_two = row[0][-2:]

        if last_two != '00' and last_two != '99':
            continue

        BPL[row[0][:-2]] = row[1]

output = defaultdict(lambda: defaultdict(lambda: 0))

print('Reading data')

with open('usa_00006.csv') as f:
    reader = csv.DictReader(f)

    for i, row in enumerate(reader):
        if i % 100000 == 0:
            print(i)

        if row['OCC'] not in OCCUPATIONS:
            continue

        occ = OCCUPATIONS[row['OCC']]
        bpl = BPL[row['BPL']]

        output[occ][bpl] += int(row['PERWT'])

print('Writing output')

with open('sum_occ_by_bpl.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['occ', 'bpl', 'count'])

    for occ, bpls in output.items():
        for bpl, count in bpls.items():
            writer.writerow([occ, bpl, count])
