import smtplib

from bson import ObjectId
from email.mime.multipart import MIMEMultipart
from email.mime.audio import MIMEAudio

from configs import SENDER_ADDRESS, GMAIL_PWD


def send_email_ns(message, db_mp3):
    # try:
    mp3_fid = message["mp3_fid"]
    sender_address = SENDER_ADDRESS
    sender_password = GMAIL_PWD
    receiver_address = message["username"]

    msg = MIMEMultipart()

    msg["Subject"] = "MP3 file download is now ready! "
    msg["From"] = sender_address
    msg["To"] = receiver_address
    msg["Text"] = f"mp3 file_id: {mp3_fid} is now ready!"

    file_data = db_mp3.get(file_id=ObjectId(mp3_fid))
    msg.attach(MIMEAudio(file_data.read(), _subtype="mp3"))

    session = smtplib.SMTP("smtp.gmail.com", 587)
    session.starttls()
    session.login(sender_address, sender_password)
    session.send_message(msg, sender_address, receiver_address)
    session.quit()
    return
