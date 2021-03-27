import os
import requests, wyre.settings

class Mailer:

    @staticmethod
    def send_simple_message( sender, title, message, receievers):

        """
            SEND SIMPLE MAIL REQUIRES :
            - SENDER - NUMERIC CODE
            - TITLE -> STRING
            - MESSAGE -> STRING
            - RECEIVERS -> LIST

            POSSIBLE SENDERS:
                1. WYRE-MONITOR
                2. WYRE-ALERTS
        """
        api_key = os.environ.get("api_key")
        mailgun_url = os.environ.get("mailgun_url")
        response = requests.post(
            mailgun_url,
            auth=("api", api_key),
            data={"from": f"{wyre.settings.POSSIBLE_SENDERS[sender]} <mailer@wyreng.com>",
                "to": receievers,
                "subject": title,
                "text": message})
        
        if response.ok:
            print("Sending successful ")
            open("maillogs.txt", "a").write("Sending Successful")
            return {
                "status": True,
                "message": "E-mail successfully sent"
            }

        else:
            print("Sending failed ")
            open("maillogs.txt", "a").write(f"Sending failed ({response.content})")

            return {
                "status": True,
                "message": response.content
            }

    @staticmethod
    def send_simple_message_with_attachment( sender, title, message, receievers, attachment: str):

        """
            SEND SIMPLE MAIL REQUIRES :
            - SENDER - NUMERIC CODE
            - TITLE -> STRING
            - MESSAGE -> STRING
            - RECEIVERS -> LIST

            POSSIBLE SENDERS:
                1. WYRE-MONITOR
                2. WYRE-ALERTS
                3. WYRE-GENIUS
        """
        api_key = os.environ.get("api_key")
        mailgun_url = os.environ.get("mailgun_url")
        response = requests.post(
            mailgun_url,
            auth=("api", api_key),
            files=[("attachment",("Report.pdf", open(attachment, "rb").read())) ],
            data={"from": f"{wyre.settings.POSSIBLE_SENDERS[sender]} <mailer@wyreng.com>",
                "to": receievers,
                "subject": title,
                "text": message})
        
        if response.ok:
            print("Sending successful ")
            open("maillogs.txt", "a").write("Sending Successful")
            return {
                "status": True,
                "message": "E-mail successfully sent"
            }

        else:
            print("Sending failed ")
            open("maillogs.txt", "a").write(f"Sending failed ({response.content})")

            return {
                "status": False,
                "message": response.content
            }