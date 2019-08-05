from datetime import datetime, timedelta


class EmailService:

    def __init__(self):
        self.current_date = datetime.now().date()
    def load_details(self):
        pass


def main():
    email_details = {   "host": "",
                        "port": "",
                        "host_user": "",
                        "host_password": "",
                        "sender": "",
                        "subject":"",
                        "message":"",
                        }

if __name__ == '__main__':
    main()