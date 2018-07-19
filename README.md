# BDay-Remind

Output ical calendar containing events for birthdays based on local
vcard files. The dir to these files must be given.

Depends on the python module
[vobject](https://github.com/eventable/vobject).

Example output for a `vcard` file with the following data in ./test/:

	BEGIN:VCARD
	VERSION:3.0
	UID:db2092b7d8b2e11ba6c06f3cb01ded62
	FN:Max Mustermann
	BDAY;VALUE=date:1970-03-15
	END:VCARD


	$ python bday-remind.py ./test
	BEGIN:VCALENDAR
	VERSION:2.0
	PRODID:BDAY-REMIND
	BEGIN:VEVENT
	UID:bday-remind-max-mustermann-1970-03-15
	DTSTART;VALUE=DATE:19700315
	DESCRIPTION:Born 1970-03-15
	DTSTAMP:20180719T120219Z
	RRULE:FREQ=YEARLY
	SUMMARY:[BDAY] Max Mustermann
	BEGIN:VALARM
	ACTION:DISPLAY
	TRIGGER:-PT30M
	END:VALARM
	END:VEVENT
	END:VCALENDAR

The `uid` field of the distinct *vevents* are chosen in a
deterministic and easy to replicate way, so that if the output ics
string can easily be imported into the calendar again and the events
are overwritten if they are contained as well. This is useful, if only
one vcards with another birthday is added. If the `uids` are random,
	the calendar software might not get a duplicate insertion and the
	user would end up with duplicate events.
