import argparse
import vobject
import os
from math import ceil
import datetime

def parse_files(files):
    birthday_dict = dict()

    for file in files:
        try:
            with open(file) as f:
                vcard = vobject.readOne(''.join(f.readlines()))
        except:
            print(f'Error reading {file} as vcard')

        if 'bday' in vcard.contents:
            year, mon, day = map(int, vcard.contents['bday'][0].value.split('-'))
            birthday = datetime.date(year, mon, day)

        if 'fn' in vcard.contents:
            name = vcard.contents['fn'][0].value

        if name and birthday:
            birthday_dict[name] = birthday

        name, birthday = None, None

    return birthday_dict

if __name__ == '__main__':
    ap = argparse.ArgumentParser(
            description='Output icalendar containing events for birthdays in vcf files',
            formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument('dir',
            help='Path to dir containing vcards')

    args = ap.parse_args()

    if not os.path.isdir(args.dir):
        ap.print_help()
        exit(1)

    files = [os.path.join(args.dir, f) for f in os.listdir(args.dir) if os.path.isfile(os.path.join(args.dir, f))]

    birthday_dict = parse_files(files)

    ical = vobject.iCalendar()
    ical.add('prodid').value = f'bday-remind'.upper()

    for k, v in birthday_dict.items():
        vevent = ical.add('vevent')
        vevent.add('summary').value = f'[BDAY] {k}'
        vevent.add('description').value = f'Born {v}'
        vevent.add('uid').value = f'bday-remind-{k.replace(" ", "-").lower()}-{v}'

        dtstart = vevent.add('dtstart')
        dtstart.value = v

        valarm = vevent.add('valarm')
        valarm.add('action').value = 'DISPLAY'
        valarm.add('trigger').value = datetime.timedelta(minutes=-30)

        rrule = vevent.add('rrule')
        rrule.value = 'FREQ=YEARLY'

    print(ical.serialize())

