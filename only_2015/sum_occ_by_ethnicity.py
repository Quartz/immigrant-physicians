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

ETHNICITIES = {
    '416': 'Iranian',
    '429': 'Syrian',
    '553': 'Nigerian',
    '615': 'Indian',
    '706': 'Chinese'
}

POPULATION = 150534773
DESIGN_FACTOR = 2.0     # Ancestry


def standard_error(estimate):
    return DESIGN_FACTOR * math.sqrt(99 * estimate * (1 - (estimate / POPULATION)))


output = defaultdict(lambda: defaultdict(lambda: 0))

print('Reading data')

with open('usa_00015.csv') as f:
    reader = csv.DictReader(f)

    for i, row in enumerate(reader):
        if i % 100000 == 0:
            print(i)

        try:
            occ = OCCUPATIONS[row['OCC']]
        except KeyError:
            continue

        ethnicity = ETHNICITIES.get(row['ANCESTR1'], 'Other')

        output[occ][ethnicity] += int(row['PERWT'])

print('Writing output')

with open('sum_occ_by_ethnicity.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['occ', 'ethnicity', 'count', 'pct', 'std_err', 'moe'])

    for occ, ethnicities in output.items():
        total = sum(ethnicities.values())

        for ethnicity, count in ethnicities.items():
            pct = count / total
            std_err = standard_error(count)
            ninety_percent = std_err * 1.645
            moe = ninety_percent / count * 100

            writer.writerow([occ, ethnicity, count, pct, std_err, moe])
