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

POPULATION = 150534773
DESIGN_FACTOR = 1.9


def standard_error(year, estimate):
    return DESIGN_FACTOR * math.sqrt(99 * estimate * (1 - (estimate / POPULATION)))



output = defaultdict(lambda: defaultdict(lambda: 0))

print('Reading data')

with open('usa_00012.csv') as f:
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
    writer.writerow(['occ', 'year', 'count', 'pct', 'std_err', 'moe'])

    for occ, years in output.items():
        total = sum(years.values())

        for year, count in years.items():
            pct = count / total
            std_err = standard_error(year, count)
            ninety_percent = std_err * 1.645
            moe = ninety_percent / count * 100

            writer.writerow([occ, year, count, pct, std_err, moe])
