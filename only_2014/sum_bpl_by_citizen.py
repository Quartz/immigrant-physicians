#!/usr/bin/env python

from collections import defaultdict
import csv
import math

CITIZEN = {
    '0': 'N/A',
    '1': 'Born abroad of American parents',
    '2': 'Naturalized citizen',
    '3': 'Not a citizen',
    '4': 'Not a citizen, but has received first papers',
    '5': 'Foreign born, citizenship status not reported'
}

# TKTK: NOT UPDATED FOR 2014 dataset
POPULATION = 150534773
DESIGN_FACTOR = 2.0     # Ancestry


BPL = {}

with open('../bpl_mapping.csv') as f:
    reader = csv.reader(f)
    header = next(reader)

    for row in reader:
        last_two = row[0][-2:]

        if last_two != '00' and last_two != '99':
            continue

        BPL[row[0][:-2]] = row[1]


def standard_error(estimate):
    return DESIGN_FACTOR * math.sqrt(99 * estimate * (1 - (estimate / POPULATION)))


output = defaultdict(lambda: defaultdict(lambda: 0))

print('Reading data')

with open('usa_00016.csv') as f:
    reader = csv.DictReader(f)

    for i, row in enumerate(reader):
        if i % 100000 == 0:
            print(i)

        bpl = BPL.get(row['BPL'], 'Other')
        citizen = CITIZEN[row['CITIZEN']]

        output[bpl][citizen] += int(row['PERWT'])

print('Writing output')

with open('sum_bpl_by_citizen.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['bpl', 'citizen', 'count', 'pct', 'std_err', 'moe'])

    for bpl, citizens in output.items():
        total = sum(citizens.values())

        for citizen, count in citizens.items():
            pct = count / total
            std_err = standard_error(count)
            ninety_percent = std_err * 1.645
            moe = ninety_percent / count * 100

            writer.writerow([bpl, citizen, count, pct, std_err, moe])
