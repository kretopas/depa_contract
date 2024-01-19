# app/odoo/user.py
from app.helpers.odoo import Odoo
from app.odoo.certificate import generate_password

from decouple import config
from email.utils import make_msgid
from email.header import decode_header
from email.mime.text import MIMEText
from typing import Union
import smtplib
import xmlrpc.client

SMTP_SSL_HOST = "smtp.office365.com"
SMTP_SSL_PORT = 587
EMAIL_ADDRESS = config("SARABAN_EMAIL_ADDRESS")
EMAIL_PASSWORD = config("SARABAN_EMAIL_PASSWORD")

odoo = Odoo()
db = config("ODOO_DB")
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(config("ODOO_URL")))

def check_authenticate(login_username: str, login_password: str) -> tuple:
    try:
        login_uid = common.authenticate(db, login_username, login_password, {})
        if login_uid:
            res_user = odoo.search_read('res.users', [
                ['id', '=', login_uid]
            ], {
                'fields': ['sel_groups_1_9_10']
            })[0]
            data = (login_uid, res_user['sel_groups_1_9_10'])
        else:
            data = (False, False)
        return data
    except Exception as e:
        print(e)
        return (False, False)
    
def get_employee_data(user_id: int) -> Union[dict, bool]:
    employee = odoo.search_read('hr.employee', [
        ['user_id', '=', user_id]
    ], {
        'fields': ['id', 'name', 'emp_code']
    })
    return employee[0] if employee else False

def check_duplicate_user(user: str) -> bool:
    user = odoo.search('res.users', [
        ['login', '=', user]
    ])
    return False if user else True

def get_user(user: str) -> Union[int, bool]:
    employee = odoo.search_read('res.users', [
        ['login', '=', user]
    ], {
        'fields': ['partner_id']
    })
    return employee[0]['partner_id'][0] if employee else False

def get_user_partner(user: str) -> dict:
    employee = odoo.search_read('res.users', [
        ['login', '=', user]
    ], {
        'fields': ['partner_id']
    })
    return employee[0] if employee else False

def get_partner_detail(partner_id: int) -> dict:
    partner = odoo.search_read('res.partner', [
        ['id', '=', partner_id]
    ], {
        'fields': ['email']
    })
    return partner[0]['email'] if partner else False

def change_user_password(user_id: int, new_password: str) -> None:
    update = odoo.write('res.users', user_id, {
        'new_password': new_password
    })
    return update if update else False

def send_email(destination: str, new_password: str = None, otp_message: dict = None) -> None:
    if new_password is not None:
        reply = f"""
            <html>
                <head></head>
                <body>
                    <p>
                    รหัสผ่านใหม่สำหรับเข้าใช้งานระบบ depa Contract ของคุณคือ<br/><br/>
                    {new_password}<br/>
                    </p>
                </body>
            </html>
        """
        subject = "depa Contract - รหัสผ่านใหม่"
        action = "password"
    elif otp_message is not None:
        reply = f"""
            <html>
                <head></head>
                <body>
                    <p>
                    OTP - {otp_message['otp']} (ref: {otp_message['ref']})<br/>
                    สำหรับเข้าสู่ระบบ depa Contract 
                    </p>
                </body>
            </html>
        """
        subject = "depa Contract - OTP"
        action = "otp"
    msg = MIMEText(reply, 'html')
    msg["Message-ID"] = make_msgid()
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = destination
    with smtplib.SMTP(SMTP_SSL_HOST, SMTP_SSL_PORT) as server:
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD, initial_response_ok=True)
        server.ehlo()
        server.sendmail(EMAIL_ADDRESS, destination, msg.as_string())
        print(f"Email ({action}) Sent to {destination}!")
        server.close()

def get_censor_email(user_email: str) -> str:
    email = user_email.split("@")
    email_name = email[0]
    email_domain = email[1]
    change_amount = (len(email_name) - 3)
    censor_email = ("x"*change_amount)+email_name[change_amount:len(email_name)]+"@"+email_domain
    return censor_email

def reset_user_password(user_name: str) -> Union[str, bool]:
    res_user = get_user_partner(user_name)
    partner_id = res_user['partner_id'][0]
    user_id = res_user['id']
    user_email = get_partner_detail(partner_id)
    if not user_email:
        return False
    censor_email = get_censor_email(user_email)
    new_password = generate_password(12)
    if change_user_password(user_id, new_password):
        send_email(destination=user_email, new_password=new_password)
        return censor_email
    return False

def email_otp(user_name: str, otp: str, ref: str) -> Union[dict, bool]:
    partner_id = get_user(user_name)
    user_email = get_partner_detail(partner_id)
    if not user_email:
        return False
    censor_email = get_censor_email(user_email)
    send_email(destination=user_email, otp_message={'otp': otp, 'ref': ref})
    return {'email': censor_email, 'ref': ref}