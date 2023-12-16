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


def notify_users(single_exposures: list[dict], daily_averages: list[dict], config: Config):
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

    body_html += "<p>Можете да видите малко повече информация за средните и максимални стойности на " \
                 "<a href=\"http://ec2-16-171-116-250.eu-north-1.compute.amazonaws.com:3000/\">този уебсайт</a> " \
                 "(разработва се активно и е възможно представените данни да са некоректни). " \
                 "За повече информация или подвърждение на данните, моля свържете се с " \
                 "<a href=\"mailto:yosifovemil@gmail.com\">yosifovemil@gmail.com</a></p>"

    send_email(
        subject=subject,
        body=body_text,
        email_user=config.get_email_user(),
        email_password=config.get_email_password(),
        recipients=config.get_users(),
        body_html=body_html
    )


def format_single_exposures(single_exposures: list[dict]):
    html = "<h2>Еднократни стойности над лимита</h2>"
    for compound in single_exposures:
        html += "<h3>{compound} - лимит {limit} µg/m3</h3>".format(compound=compound['name'], limit=compound['limit'])
        html += compound['data'].to_html(index=False)
        html += "<br />"

    return html


def format_averages(daily_averages: list[dict]):
    html = "<h2>Средни денонощни стойности над лимита</h2>"
    html += "<table border=\"1\">"
    html += "<tr><th>Съединение</th><th>Средна денонощна концентрация</th><th>Лимит</th></tr>"
    for compound in daily_averages:
        html += "<tr>"
        html += "<td>{compound}</td>".format(compound=compound['name'])
        html += "<td>{:.2f}</td>".format(compound['average'])
        html += "<td>{:.2f}</td>".format(compound['limit'])
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
