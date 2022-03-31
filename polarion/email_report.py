#!/usr/bin/env python

"""
Module to generate email report post extracting automation status from polarion.
"""
import os
import smtplib
import sys
import time
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import pytz
from jinja2 import Environment, FileSystemLoader, select_autoescape
from jinja_markdown import MarkdownExtension

import config as cf
from main import main

config = cf.Config()
config.load()
gmail_user = config.sender_user
mail_to = config.recipient_user
PRODUCT = "Red Hat Ceph Storage"
results = main()


def send_email(gmail_user, recipients, subject, body):
    """
    Function to send email from sender to receipients with the subject and message passed.
    """

    sent_from = gmail_user

    msg = MIMEMultipart("mixed")
    msg["Subject"] = subject
    msg["From"] = gmail_user
    msg["To"] = ", ".join(recipients)

    # create html template for email body
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print(project_dir)
    template_dir = os.path.join(project_dir, "polarion/html_template")
    jinja_env = Environment(
        extensions=[MarkdownExtension],
        loader=FileSystemLoader(template_dir),
        autoescape=select_autoescape(["html", "xml"]),
    )
    template = jinja_env.get_template("automation_status.html")
    automation_status = template.render(items=body[0])

    template = jinja_env.get_template("component_wise_data.html")
    # component_data = template.render(content=body[1])
    component_data = template.render(content=body)

    # Record the MIME types of both parts - text/plain and text/html.
    table1 = MIMEText(automation_status, "html")
    table2 = MIMEText(component_data, "html")

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(table1)
    msg.attach(table2)

    try:
        s = smtplib.SMTP("localhost")
        s.sendmail(sent_from, recipients, msg.as_string())
        s.quit()

        print("Email sent!")
    except:
        print("Something went wrong...{}", sys.exc_info()[0])


UTC = pytz.utc
IST = pytz.timezone("Asia/Kolkata")
datetime_ist = datetime.now(IST)
start_time = datetime_ist.strftime("%d %b %Y %H:%M")
send_email(
    gmail_user,
    [mail_to],
    f"{PRODUCT} Automation Status as on {start_time} [IST]",
    results,
)
