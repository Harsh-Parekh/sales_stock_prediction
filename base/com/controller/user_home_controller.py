import secrets
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import render_template, request, redirect, flash, jsonify, url_for

from base import app
from base.com.controller.login_controller import login_session, logout_session
from base.com.dao.area_dao import AreaDAO
from base.com.dao.city_dao import CityDAO
from base.com.dao.login_dao import LoginDAO
from base.com.dao.state_dao import StateDAO
from base.com.dao.user_dao import UserDAO
from base.com.vo.area_vo import AreaVO
from base.com.vo.city_vo import CityVO
from base.com.vo.login_vo import LoginVO
from base.com.vo.user_vo import UserVO


@app.route('/user/ajax_city', methods=['GET'])
def user_ajax_city():
    try:
        user_dao = UserDAO()
        city_vo = CityVO()
        city_vo.city_state_id = request.args.get('stateId')
        city_vo_list = user_dao.view_ajax_city(city_vo)
        data = [i.as_dict() for i in city_vo_list]
        return jsonify(data)
    except Exception as ex:
        print('user_ajax_city route error occurred>>>>>>>>>>', ex)


@app.route('/user/ajax_area', methods=['GET'])
def user_ajax_area():
    try:
        user_dao = UserDAO()
        area_vo = AreaVO()
        area_vo.area_city_id = request.args.get('cityId')
        area_vo_list = user_dao.view_ajax_area(area_vo)
        data = [i.as_dict() for i in area_vo_list]
        return jsonify(data)
    except Exception as ex:
        print('user_ajax_area route error occurred>>>>>>>>>>', ex)


@app.route('/load_register', methods=['GET'])
def user_load_register():
    try:
        state_dao = StateDAO()
        state_list = state_dao.search_state()
        return render_template('user/register.html', state_data=state_list)
    except Exception as ex:
        print('user_load_register route error occurred>>>>>>>>>>', ex)


@app.route('/insert_user', methods=["POST"])
def user_insert_user():
    try:
        login_vo = LoginVO()
        user_vo = UserVO()
        login_dao = LoginDAO()
        user_dao = UserDAO()

        login_vo.login_username = request.form.get('username')
        is_exist = login_dao.is_exist(login_vo)
        if is_exist == True:

            login_password = secrets.token_hex(8)

            login_vo.login_username = request.form.get('username')
            login_vo.login_password = login_password
            login_vo.login_role = 'user'
            login_vo.login_status = 'active'
            login_vo.login_secretkey = secrets.token_hex(32)
            login_dao.insert_login(login_vo)

            user_vo.user_organization_name = request.form.get('organizationName')
            user_vo.user_contact = request.form.get('contact')
            user_vo.user_state_id = request.form.get('stateId')
            user_vo.user_city_id = request.form.get('cityId')
            user_vo.user_area_id = request.form.get('areaId')
            user_vo.user_address = request.form.get('address')
            user_vo.user_fullname = request.form.get('ownerName')
            user_vo.user_login_id = login_vo.login_id
            user_dao.insert_user(user_vo)

            sender = "salesstockpredictiondonotreply@gmail.com"
            receiver = request.form.get('username')
            msg = MIMEMultipart()
            msg['From'] = sender
            msg['To'] = receiver
            msg['Subject'] = "Sales Stock Prediction Password"
            message = """
            Welcome to Sales Stock Prediction !!!

            Bring the power of data analytics to your organization to
            Grow up your Sales with the power of MachineLearning.

            Your Registration is completed
            Your temporary Password for login to your account is: {}

            After login you can change your Password from Edit Profile.
                """.format(login_password)

            msg.attach(MIMEText(message, 'plain'))

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender, "salesstockprediction")
            text = msg.as_string()
            server.sendmail(sender, receiver, text)
            server.quit()

            flash('Register Successfully!!! U will receive an password mail shortly in your register email.', 'success')
            return redirect('/')
        else:
            flash('Email id already register!!!', 'exist')
            return redirect(url_for('user_load_register'))
    except Exception as ex:
        print('user_insert_user route error occurred>>>>>>>>>>', ex)


@app.route('/user/change_password', methods=['GET'])
def user_change_password():
    try:
        if login_session() == 'user':
            login_dao = LoginDAO()
            login_secretkey = request.cookies.get('login_secretkey')
            login_vo_list = login_dao.get_login_data(login_secretkey)
            return render_template('user/changePassword.html', data=login_vo_list)
        else:
            return logout_session()
    except Exception as ex:
        print('user_change_password route error occurred>>>>>>>>>>', ex)


@app.route('/user/update_profile_password', methods=['POST'])
def user_update_profile_password():
    try:
        if login_session() == 'user':
            login_dao = LoginDAO()
            login_vo = LoginVO()
            login_vo.login_id = request.form.get('loginId')
            login_username = login_dao.find_login_username(login_vo)
            login_vo.login_username = login_username
            login_vo.login_password = request.form.get('password1')
            login_dao.update_password(login_vo)
            return redirect(url_for('user_load_edit_profile'))

        else:
            return logout_session()
    except Exception as ex:
        print('user_update_profile_password route error occurred>>>>>>>>>>', ex)


@app.route('/user/load_edit_profile')
def user_load_edit_profile():
    try:
        if login_session() == 'user':
            login_dao = LoginDAO()
            user_dao = UserDAO()
            state_dao = StateDAO()
            city_dao = CityDAO()
            area_dao = AreaDAO()

            state_vo_list = state_dao.search_state()
            city_vo_list = city_dao.search_city()
            area_vo_list = area_dao.search_area()

            login_secretkey = request.cookies.get('login_secretkey')

            login_vo_list = login_dao.get_login_data(login_secretkey)
            user_vo = user_dao.get_user(login_vo_list.login_id)

            return render_template('user/editProfile.html', user_data=user_vo, statedata=state_vo_list,
                                   citydata=city_vo_list, areadata=area_vo_list)
        else:
            return logout_session()
    except Exception as ex:
        print('user_load_edit_profile route error occurred>>>>>>>>>>', ex)


@app.route('/user/update_profile', methods=['POST'])
def user_update_profile():
    try:
        if login_session() == 'user':
            user_vo = UserVO()
            login_vo = LoginVO()
            user_dao = UserDAO()

            user_vo.user_login_id = request.form.get('loginId')
            user_vo.user_id = request.form.get('userId')
            user_vo.user_state_id = request.form.get('stateId')
            user_vo.user_city_id = request.form.get('cityId')
            user_vo.user_area_id = request.form.get('areaId')
            user_vo.user_address = request.form.get('address')
            user_vo.user_organization_name = request.form.get('organizationName')
            user_vo.user_fullname = request.form.get('ownerName')
            user_vo.user_contact = request.form.get('contact')

            login_vo.login_id = request.form.get('loginId')
            login_vo.login_username = request.form.get('username')
            login_vo.login_password = request.form.get('password')

            user_dao.update_login_profile(login_vo)
            user_dao.update_user_profile(user_vo)

            return redirect(url_for('user_load_edit_profile'))
        else:
            return logout_session()
    except Exception as ex:
        print('user_update_profile route error occurred>>>>>>>>>>', ex)
