#!/usr/bin/env python

from collections import defaultdict
import csv
import math

# "YEAR","DATANUM","SERIAL","HHWT","GQ","PERNUM","PERWT","BPL","BPLD","OCC"

OCCUPATIONS = {
    '3010': 'Dentists',
    '3040': 'Optometrists',
    '3050': 'Pharmacists',
    '3060': 'Physicians and Surgeons',
    '3110': 'Physicians Assistants',
    '3255': 'Registered Nurses'
}

POPULATION = {
    '2005': 136458810,
    '2010': 139033928,
    '2015': 150534773,
}

DESIGN_FACTOR = {
    '2005': 2.2,
    '2010': 2.0,
    '2015': 2.5
}


def standard_error(year, estimate):
    return DESIGN_FACTOR[year] * math.sqrt(99 * estimate * (1 - (estimate / POPULATION[year])))


BPL = {}

with open('../bpl_mapping.csv') as f:
    reader = csv.reader(f)
    header = next(reader)

    for row in reader:
        last_two = row[0][-2:]

        if last_two != '00' and last_two != '99':
            continue

        BPL[row[0][:-2]] = row[1]

output = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0)))

print('Reading data')

with open('usa_00011.csv') as f:
    reader = csv.DictReader(f)

    for i, row in enumerate(reader):
        if i % 100000 == 0:
            print(i)

        if row['OCC'] not in OCCUPATIONS:
            continue

        year = row['YEAR']
        occ = OCCUPATIONS[row['OCC']]
        bpl = BPL[row['BPL']]

        output[year][occ][bpl] += int(row['PERWT'])

print('Writing output')

with open('sum_occ_by_bpl.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['year', 'occ', 'bpl', 'count', 'pct', 'std_err'])

    for year, occs in output.items():
        for occ, bpls in occs.items():
            total = sum(bpls.values())

            for bpl, count in bpls.items():
                pct = count / total
                std_err = standard_error(year, count)

                writer.writerow([year, occ, bpl, count, pct, std_err])
