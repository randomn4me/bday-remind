import argparse
import vobject
from math import ceil
from datetime import date

from os import listdir
from os.path import isfile, isdir


ap = argparse.ArgumentParser(
        description='Print birthdays of local vcard files',
        formatter_class=argparse.RawTextHelpFormatter)
ap.add_argument('dir', help='Path to dir containing vcards')

args = ap.parse_args()

if not isdir(args.dir):
    ap.print_help()
    exit(1)

files = [args.dir + '/' + f for f in listdir(args.dir) if isfile(args.dir + '/' + f)]

min_distance = 365
today = date.today()

for file in files:
    with open(file) as f:
        file_data = f.readlines()

    vcard = vobject.readOne(''.join(file_data))

    if 'bday' in vcard.contents:
        year, mon, day = map(int, vcard.contents['bday'][0].value.split('-'))
        bday = date(today.year, mon, day)

    if 'fn' in vcard.contents:
        name = vcard.contents['fn'][0].value

    if name and bday:
        if bday.replace(year=today.year) < today:
            bday = bday.replace(year=today.year+1)

        ttb = (bday - today).days

        if ttb < min_distance:
            min_distance = ttb
            next_name = name
            next_bday = bday.replace(year=year)

    name, bday, ttb = None, None, None

age = ceil(abs(today - next_bday).days / 365)
print(f'fn:{next_name}')
print(f'bday:{next_bday}')
print(f'age:{age}')
