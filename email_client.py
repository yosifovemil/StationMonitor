import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config import Config
import pandas as pd


def error_message_admins(error: str, config: Config):
    send_email(
        subject="StationMonitor error",
        body="Encountered the following error: \n{error}".format(error=error),
        email_user=config.get_email_user(),
        email_password=config.get_email_password(),
        recipients=config.get_admins()
    )


def notify_users(single_exposures: dict[str, pd.DataFrame], daily_averages: dict[str, float], config: Config):
    subject = "Линамар превишени стойности"

    body_text = """
Здравейте,
    
Засечени са превишени стойности на следните химични съединения от станцията на Линамар:
    """

    body_html = ""

    if len(single_exposures) > 0:
        body_html += format_single_exposures(single_exposures)

    if len(daily_averages) > 0:
        body_html += format_averages(daily_averages)

    send_email(
        subject=subject,
        body=body_text,
        email_user=config.get_email_user(),
        email_password=config.get_email_password(),
        recipients=config.get_users(),
        body_html=body_html
    )


def format_single_exposures(single_exposures: dict[str, pd.DataFrame]):
    html = "<h2>Еднократни стойности над лимита</h2>"
    for compound in single_exposures.keys():
        html += "<h3>{compound}</h3>".format(compound=compound)
        html += single_exposures[compound].to_html(index=False)
        html += "<br />"

    return html


def format_averages(daily_averages: dict[str, float]):
    html = "<h2>Средни денонощни стойности над лимита</h2>"
    html += "<table border=\"1\">"
    html += "<tr><th>Съединение</th><th>Средна денонощна концентрация</th></tr>"
    for compound in daily_averages.keys():
        html += "<tr>"
        html += "<td>{compound}</td>".format(compound=compound)
        html += "<td>{:.2f}</td>".format(daily_averages[compound])
        html += "</tr>"

    html += "</table>"

    return html


def send_email(subject, body, email_user, email_password, recipients, body_html=""):
    msg = MIMEMultipart("alternative")
    msg['Subject'] = subject
    msg['From'] = email_user
    msg['To'] = ', '.join(recipients)
    msg.attach(MIMEText(body, "plain"))

    if body_html != "":
        msg.attach(MIMEText(body_html, "html"))

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
        smtp_server.login(email_user, email_password)
        smtp_server.sendmail(email_user, recipients, msg.as_string())
