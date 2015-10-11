# scriptlog-malier

Runs a command line script and emails recipients with console contant when completed/failed.

Run python scriptLog-mailer.py -h for help.

Usage example:
```
cd /script_location/
python scriptLog-mailer.py \
	-s "python script.py" \
	-ho smtp.gmail.com -po 587 -e \
	-u sender@gmail.com -p passwd \
	-r "one@domain.com, two@domain.com" \
	-n "script name"
```
-----
For issues connecting to gmail, see  [this](http://stackoverflow.com/questions/10147455/trying-to-send-email-gmail-as-mail-provider-using-python) Stack Overflow thread.
