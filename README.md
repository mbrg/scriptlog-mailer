# scriptlog-malier
Runs a command line script, emails recipients when completed/errored with console contant

Run python scriptLog-mailer.py -h for help.

Example:
python scriptLog-mailer.py \
	-s "python script.py -m YAY" \
	-ho smtp.gmail.com -po 587 -e \
	-u sender@gmail.com -p passwd \
	-r "one@domain.com, two@domain.com" \
	-n "script name" \
