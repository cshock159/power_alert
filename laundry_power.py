import os
import smtplib
from time import sleep
from email.mime.text import MIMEText

subject = "Power is out."
body = "Breaker is most likely tripped in laundry room."
sender = "EMAIL"
recipients = ["7028167158@vtext.com"]
password = "PASSWORD"
count = 0

def main():
    global count

    def send_email(subject, body, sender, recipients, password):
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = ', '.join(recipients)
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
           smtp_server.login(sender, password)
           smtp_server.sendmail(sender, recipients, msg.as_string())
        print("Message sent!")

    def pingtest():
        global count
        print("Trying to reach Dryer.")
        pingresult = os.system(f"ping -c 4 192.168.2.136 >/dev/null 2>&1")
        if pingresult != 0:
           print("Dryer didn't respond. Trying to reach Washer.")
           pingresult2 = os.system(f"ping -c 4 192.168.2.12 >/dev/null 2>&1")
           if pingresult2 != 0 and count == 0:
                print("Couldn't reach Washer or Dryer. Power may be out.")
                send_email(subject, body, sender, recipients, password)
                count = 1
                return count
           elif pingresult2 == 0 and count == 1:
                print("Reseting now that they're back online.")
                count = 0
                return count
           elif pingresult2 != 0 and count == 1:
                print("Already Sent Text. Waiting for washer/dryer to come back online to reset.")
           else:
                print("Appears online!")
        elif pingresult == 0 and count == 1:
                print("Reseting now that they're back online.")
                count = 0
                return count
        else:
           print("Appears Online!")
           count = 0
           return count
    while True:
        pingtest()
        sleep(1800)

if __name__ == "__main__":
    main()
