#!/usr/bin/env python

from collections import defaultdict
import csv
import math

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

output = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0)))


def standard_error(year, estimate):
    return DESIGN_FACTOR[year] * math.sqrt(99 * estimate * (1 - (estimate / POPULATION[year])))


print('Reading data')

with open('usa_00010.csv') as f:
    reader = csv.DictReader(f)

    for i, row in enumerate(reader):
        if i % 100000 == 0:
            print(i)

        if row['OCC'] not in OCCUPATIONS:
            continue

        year = row['YEAR']
        occ = OCCUPATIONS[row['OCC']]
        citizen = CITIZEN[row['CITIZEN']]

        output[year][occ][citizen] += int(row['PERWT'])

print('Writing output')

with open('sum_occ_by_citizen.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['year', 'occ', 'citizen', 'count', 'pct', 'std_err', 'moe'])

    for year, occs in output.items():
        for occ, citizens in occs.items():
            total = sum(citizens.values())

            for citizen, count in citizens.items():
                pct = count / total
                std_err = standard_error(year, count)
                ninety_percent = std_err * 1.645
                moe = ninety_percent / count * 100

                writer.writerow([year, occ, citizen, count, pct, std_err, moe])
