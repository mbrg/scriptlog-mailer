"""
mibarg 2015
"""
import argparse
import subprocess
import sys, os
import datetime
import tempfile
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate

def send_mail(user, passwd, send_to, subject, content, attachments=None, host="smtp.gmail.com", port=587, force_tls=False):
    """
    Send stmp email
    """
    msg = MIMEMultipart(
        From=user,
        To=COMMASPACE.join(send_to),
        Date=formatdate(localtime=True),
        Subject=subject
    )
    msg.attach(MIMEText(content))

    for a in attachments or []:
        with open(a, "rb") as fil:
            msg.attach(MIMEApplication(
                fil.read(),
                Content_Disposition='attachment; filename="%s.txt"' % os.path.basename(a),
                Name=os.path.basename(a)
            ))
    smtp = smtplib.SMTP(host, port)
    if force_tls: smtp.starttls()
    smtp.login(user, passwd)
    smtp.sendmail(user, send_to, msg.as_string())
    smtp.close()


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', "--script", required=True, help='Command line script to run, between "" signs')
    parser.add_argument('-ho', "--email_host", required=True, help='For example: smtp.gmail.com')
    parser.add_argument('-po', "--email_port", default=False)
    parser.add_argument('-u', "--email_user", required=True, help='Sender email address')
    parser.add_argument('-p', "--email_passwd", required=True)
    parser.add_argument('-r', "--recipients", required=True, help='A list of email recipients, between "" signs seperated by commas')
    parser.add_argument('-n', "--script_name", help='Short script name for the message subject')
    parser.add_argument('-l', "--logs_in_message", action='store_true', default=False, help='Send logs as email conent, not as a attachment')
    parser.add_argument('-e', "--encrypt", action='store_true', default=False, help='Force using TLS')
    args = parser.parse_args()

    # Assetions
    short_name = args.script_name if args.script_name else args.script
    args.recipients = args.recipients.split(',')
    try: assert isinstance(args.recipients, list)
    except AssertionError: print 'Recipients should be a list of email, for examle: "one@mail.com, two@mail.com"'

    # Run script
    start_time = datetime.datetime.now()
    p = subprocess.Popen(args.script.split(' '),
                     stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE,
                     )
    end_time = datetime.datetime.now()
    out, err = p.communicate()

    # Mail results
    if err=='':
        text_subject = 'Scriptlog-Mailer: Your script "%s" completed successfully on %s (after running %s minutes)' % (
            short_name,
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            (end_time-start_time).seconds/60)
        text_content = '%s\n' % text_subject
        #html_content = '<html><body><p><u>%s</u></p><br></body></html>' % text_subject
    else:
        text_subject = 'Scriptlog-Mailer: Your script "%s" raised an error on %s (after running %s minutes)' % (
            short_name,
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            (end_time-start_time).seconds/60)
        text_content = '%s\nError message:%s\n' % (text_subject, err)
        #html_content = '<html><body><p><u>%s</u></p><br><p>%s</p><br></body></html>' % (text_subject, err)

    if args.logs_in_message:
        text_content = '%s\n%s' % (text_content, out)
        #html_content = html_content.replace('</body></html>','<p>%s</p></body></html>' % out)
        fname = None
    else:
        f = tempfile.NamedTemporaryFile(delete=False)
        f.write(out)
        fname = [f.name]
        f.close()
    send_mail(user=args.email_user,
              passwd=args.email_passwd,
              send_to=args.recipients, 
              subject=text_subject, 
              content=text_content, 
              attachments=fname, 
              host=args.email_host, 
              force_tls=args.encrypt)
    if fname: os.remove(fname)  # Delete tmp file

if __name__ == '__main__':
    main(sys.argv)
