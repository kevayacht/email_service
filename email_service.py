import os
from datetime import datetime
from email.utils import formatdate
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.nonmultipart import MIMENonMultipart
from email.mime.base import MIMEBase
from email import encoders
import smtplib


class EmailService:

    def __init__(self, data):
        self.current_date = datetime.now().date()

        self.host = data["host"]
        self.port = data["port"]
        self.host_user = data["host_user"]
        self.host_password = data["host_password"]
        self.sender = data["sender"]
        self.subject = data["subject"]
        self.message = data["message"]
        self.address_list = data["address_list"]

        self.cwd = os.path.dirname(__file__)

    def email(self):

        try:
            server = smtplib.SMTP(str(self.host) + ":" + str(self.port))
            server.starttls()
            server.login(self.host_user, self.host_password)

            msg = MIMEMultipart(
                From=self.sender + "<" + self.host_user + ">",
                To=self.address_list,     # TODO: this should be an iterative function
                Date=formatdate(localtime=True),
                Subject=self.subject + " @" + str(self.current_date)
            )

            # Setup backend email details
            msg['From'] = self.sender + "<" + self.host_user + ">"
            msg['Subject'] = self.subject
            msg['To'] = self.address_list    # TODO: this should be an iterative function
            msg.attach(MIMEText(self.message.replace('\\n', '\n')))

            # Loop to attach all files in the files array
            for f in self.address_list:
                if f.find(".pdf",):
                    attachment = MIMEBase("application", "octet-stream")
                    attachment.set_payload(open(f, "rb").read())
                    encoders.encode_base64(attachment)
                    attachment.add_header('Content-Disposition', 'attachment', filename=f)
                    msg.attach(attachment)
                else:
                    attachment = MIMENonMultipart('text', 'csv', charset='utf-8')
                    attachment.set_payload(open(f, "rb").read())
                    encoders.encode_base64(attachment)
                    attachment.add_header('Content-Disposition', 'attachment', filename=f)
                    msg.attach(attachment)

            server.sendmail(self.host_user, "to_address", msg.as_string())

        except smtplib.SMTPRecipientsRefused as refused:
            print("Invalid address - {to_address}".format(to_address=self.address_list))

        finally:
            print('Done Sending mail')
            if server:
                server.quit()


def main():
    address_list = []
    email_details = {   "host": "",
                        "port": "",
                        "host_user": "",
                        "host_password": "",
                        "sender": "",
                        "subject":"",
                        "message":"",
                        "address_list": address_list,
                        }


if __name__ == '__main__':
    main()