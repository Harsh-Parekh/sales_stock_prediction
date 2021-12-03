import secrets
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import render_template, request, redirect, url_for, flash

from base import app
from base.com.dao.login_dao import LoginDAO
from base.com.dao.password_otp_dao import PasswordotpDAO
from base.com.vo.login_vo import LoginVO
from base.com.vo.password_otp_vo import PasswordotpVO


@app.route('/forgot_password', methods=['GET'])
def forgot_password():
    try:
        return render_template('user/forgotpassword.html')
    except Exception as ex:
        print('forgot_password route error occurred>>>>>>>>>>', ex)


@app.route('/send_password_link', methods=['POST'])
def send_password_link():
    try:
        login_vo = LoginVO()
        login_dao = LoginDAO()
        login_vo.login_username = request.form.get('username')
        status = login_dao.is_exist(login_vo)
        if status is False:
            otp = secrets.token_hex(2)
            password_otp_vo = PasswordotpVO()
            password_otp_dao = PasswordotpDAO()
            password_otp_vo.login_id = login_dao.find_login_id(login_vo)
            password_otp_vo.otp = otp
            password_otp_vo.time_stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            password_otp_dao.insert_passwordotp(password_otp_vo)
            sender = "salesstockpredictiondonotreply@gmail.com"
            receiver = request.form.get('username')
            msg = MIMEMultipart()
            msg['From'] = sender
            msg['To'] = receiver
            msg['Subject'] = "Account Passwor Reset"
            message = """
            Password reset link :- http://localhost:1024/reset_password 
            Verify yourself with opt :- {} for verify your self.
            """.format(otp)
            msg.attach(MIMEText(message, 'plain'))

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender, "salesstockprediction")
            text = msg.as_string()
            server.sendmail(sender, receiver, text)
            server.quit()
            message = 'Successfully sent password reset link to register e-mail id kindly check!'
            category = 'link sent'
            flash(message, category)
            return redirect('/')
        else:
            error_message = 'Username you entered is not registered with us !!!'
            category = 'invalid credentials'
            flash(error_message, category)
            return redirect(url_for('forgot_password'))
    except Exception as ex:
        print('forgot_password route error occurred>>>>>>>>>>', ex)


@app.route('/reset_password', methods=['GET'])
def reset_password():
    try:
        return render_template('user/resetpassword.html')
    except Exception as ex:
        print('reset_password route error occurred>>>>>>>>>>', ex)


@app.route('/reset_user_password', methods=['POST'])
def reset_user_password():
    try:
        login_vo = LoginVO()
        login_dao = LoginDAO()

        password_otp_dao = PasswordotpDAO()
        password_otp_vo = PasswordotpVO()

        login_vo.login_username = request.form.get('username')

        password_otp_vo.login_id = login_dao.find_login_id(login_vo)
        password_otp_vo.otp = request.form.get('otp')

        result = password_otp_dao.validate(password_otp_vo)
        print(result)

        if result:
            login_vo.login_password = request.form.get('password')
            login_dao.update_password(login_vo)
            message = 'Password successfully changed !!!'
            category = 'credentials update'
            flash(message, category)
            return redirect('/')
        elif result is False:
            message = 'OTP time limit exceed! Request for new otp !!!'
            category = 'timelimit'
            flash(message, category)
            return redirect(url_for('forgot_password'))
        elif result == 'invalid credentials':
            error_message = 'Username or otp is not valid please try again !!!'
            category = 'invalid credentials'
            flash(error_message, category)
            return redirect(url_for('reset_password'))

    except Exception as ex:
        print('reset_user_password route error occurred>>>>>>>>>>', ex)
