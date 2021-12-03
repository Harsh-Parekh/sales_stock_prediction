from datetime import timedelta

from flask import render_template, redirect, request, url_for, make_response, flash

from base import app
from base.com.dao.complaint_dao import ComplaintDAO
from base.com.dao.feedback_dao import FeedbackDAO
from base.com.dao.login_dao import LoginDAO
from base.com.dao.prediction_dao import PredictionDAO
from base.com.vo.login_vo import LoginVO
from scripts.donut import make_donut_chart

global_loginvo_list = []
global_login_secretkey_set = {0}
print(global_loginvo_list, global_login_secretkey_set)


@app.route('/', methods=['GET'])
def load_login():
    try:
        return render_template('login.html')
    except Exception as ex:
        print("load_login route exception occurred>>>>>>>>>>", ex)


@app.route("/validate_login", methods=['POST'])
def validate_login():
    try:

        global global_loginvo_list
        global global_login_secretkey_set

        login_vo = LoginVO()
        login_dao = LoginDAO()

        login_vo.login_username = request.form.get('username')
        login_vo.login_password = request.form.get('password')

        login_vo_list = login_dao.validate_login(login_vo)
        login_list = [i.as_dict() for i in login_vo_list]
        print("in validate_login login_list>>>>>>>>>>>", login_list)

        len_login_list = len(login_list)

        if len_login_list == 0:
            error_message = 'Username or password is incorrect !!!'
            category = 'invalid credentials'
            flash(error_message, category)
            return redirect(url_for('load_login'))

        elif login_list[0]['login_status'] == 'inactive':
            error_message = 'You have been temporarily blocked by website admin !!!'
            category = 'inactive user'
            flash(error_message, category)
            return redirect(url_for('load_login'))

        else:
            for row_entry in login_list:
                login_id = row_entry['login_id']
                login_username = row_entry['login_username']
                login_role = row_entry['login_role']
                login_secretkey = row_entry['login_secretkey']
                login_vo_dict = {
                    login_secretkey:
                        {'login_username': login_username, 'login_role': login_role, 'login_id': login_id}
                }

                if len(global_loginvo_list) != 0:

                    for i in global_loginvo_list:
                        tempList = list(i.keys())
                        global_login_secretkey_set.add(tempList[0])
                    login_secretkey_list = list(global_login_secretkey_set)

                    if login_secretkey not in login_secretkey_list:
                        global_loginvo_list.append(login_vo_dict)
                else:

                    global_loginvo_list.append(login_vo_dict)

                if login_role == 'admin':
                    response = make_response(redirect(url_for('load_dashboard')))
                    response.set_cookie('login_secretkey', value=login_secretkey, max_age=timedelta(minutes=30))
                    response.set_cookie('login_username', value=login_username, max_age=timedelta(minutes=30))
                    login_secretkey = request.cookies.get('login_secretkey')
                    login_username = request.cookies.get('login_username')

                    print("in validate_login login_secretkey>>>>>>>>>>>>>>>", login_secretkey)
                    print("in validate_login login_username>>>>>>>>>>>>>>>", login_username)
                    return response

                elif login_role == 'user':
                    response = make_response(redirect(url_for('load_dashboard')))
                    response.set_cookie('login_secretkey', value=login_secretkey, max_age=timedelta(minutes=30))
                    response.set_cookie('login_username', value=login_username, max_age=timedelta(minutes=30))
                    login_secretkey = request.cookies.get('login_secretkey')
                    login_username = request.cookies.get('login_username')

                    print("in validate_login login_secretkey>>>>>>>>>>>>>>>", login_secretkey)
                    print("in validate_login login_username>>>>>>>>>>>>>>>", login_username)
                    return response

                else:
                    return redirect(url_for('logout_session'))
    except Exception as ex:
        print("validate_login route exception occurred>>>>>>>>>>", ex)


@app.route('/load_dashboard', methods=['GET'])
def load_dashboard():
    try:

        if login_session() == 'admin':

            login_dao = LoginDAO()
            feedback_dao = FeedbackDAO()
            complaint_dao = ComplaintDAO()
            prediction_dao = PredictionDAO()

            userdata = login_dao.users()
            complain_pending_data = complaint_dao.complaint_pending()

            feedback = feedback_dao.feedback_data()
            prediction = prediction_dao.total_prediction()

            if userdata[1] != 0:
                percentage = round((prediction * 100) / userdata[1], 2)
                prediction = {'percentage': percentage, 'prediction': prediction}

            else:
                percentage = 0.0
                prediction = {'percentage': percentage, 'prediction': prediction}

            make_donut_chart(feedback)

            return render_template('admin/index.html', feedback=feedback,
                                   complainpending={'percentage': complain_pending_data[0],
                                                    'complaint': complain_pending_data[1]},
                                   user={'percentage': userdata[0], 'total': userdata[1]}
                                   , prediction=prediction, activeuser=userdata[2], blockuser=userdata[3])

        elif login_session() == 'user':
            return render_template('user/index.html')

        else:
            return redirect(url_for('logout_session'))
    except Exception as ex:
        print("load_dashboard route exception occurred>>>>>>>>>>", ex)


@app.route('/login_session')
def login_session():
    try:

        global global_loginvo_list
        login_role_flag = ""

        print("before login_role_flag=", login_role_flag)
        print("before len(login_role_flag)>>>>>>>>>>", len(login_role_flag))

        login_secretkey = request.cookies.get('login_secretkey')
        print("in login_session login_secretkey>>>>>>>>>", login_secretkey)

        if login_secretkey is None:
            return redirect('/')

        for i in global_loginvo_list:
            if login_secretkey in i.keys():
                if i[login_secretkey]['login_role'] == 'admin':
                    login_role_flag = "admin"
                elif i[login_secretkey]['login_role'] == 'user':
                    login_role_flag = "user"

        print("after login_role_flag>>>>>>>>>>", login_role_flag)
        print("after len(login_role_flag)>>>>>>>>>>", len(login_role_flag))

        if len(login_role_flag) != 0:
            print("<<<<<<<<<<<<<<<<True>>>>>>>>>>>>>>>>>>>>")
        return login_role_flag
    except Exception as ex:
        print("login_session route exception occurred>>>>>>>>>>", ex)


@app.route("/logout_session", methods=['GET'])
def logout_session():
    try:

        global global_loginvo_list

        login_secretkey = request.cookies.get('login_secretkey')
        login_username = request.cookies.get('login_username')

        print("in logout_session login_secretkey>>>>>>>>>", login_secretkey)
        print("in logout_session login_username>>>>>>>>>", login_username)
        print("in logout_session type of login_secretkey>>>>>>>>>", type(login_secretkey))
        print("in logout_session type of login_username>>>>>>>>>", type(login_username))

        response = make_response(redirect('/'))

        if login_secretkey is not None and login_username is not None:
            response.set_cookie('login_secretkey', login_secretkey, max_age=0)
            response.set_cookie('login_username', login_username, max_age=0)

            for i in global_loginvo_list:

                if login_secretkey in i.keys():  # line 138 core logic
                    global_loginvo_list.remove(i)
                    print("in logout_session global_loginvo_list>>>>>>>>>>>>>>>", global_loginvo_list)
                    break
        return response
    except Exception as ex:
        print("logout_session route exception occurred>>>>>>>>>>", ex)
