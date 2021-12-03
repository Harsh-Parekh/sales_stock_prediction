from datetime import datetime

from flask import render_template, request, redirect, url_for

from base import app
from base.com.controller.login_controller import login_session, logout_session
from base.com.dao.complaint_dao import ComplaintDAO
from base.com.dao.login_dao import LoginDAO
from base.com.vo.complaint_vo import ComplaintVO
from base.com.vo.login_vo import LoginVO


@app.route('/user/load_post_complaint', methods=['GET'])
def user_load_post_complaint():
    try:
        if login_session() == 'user':

            login_dao = LoginDAO()
            login_vo = LoginVO()
            complaint_dao = ComplaintDAO()

            login_username = request.cookies.get('login_username')
            login_vo.login_username = login_username

            user_login_id = login_dao.find_login_id(login_vo)
            complaints = complaint_dao.user_complaint_list(user_login_id)

            if len(complaints) != 0:
                admin_login_id = complaints[0][0].complaint_to_login_id
                admin_login_vo = LoginVO()
                admin_login_vo.login_id = admin_login_id
                admin_login_username = login_dao.find_login_username(admin_login_vo)
                return render_template('user/complaint.html', complaints=complaints,
                                       admin_username=admin_login_username)
            else:
                return render_template('user/complaint.html', complaints=complaints)

        else:
            return logout_session()
    except Exception as ex:
        print('user_load_post_complaint route error occurred>>>>>>>>>>', ex)


@app.route('/user/post_complaint', methods=['POST'])
def user_post_complaint():
    try:
        if login_session() == 'user':

            login_dao = LoginDAO()
            login_vo = LoginVO()
            complain_dao = ComplaintDAO()
            complaint_vo = ComplaintVO()

            login_username = request.cookies.get('login_username')
            login_vo.login_username = login_username
            user_login_id = login_dao.find_login_id(login_vo)

            complaint_vo.complaint_subject = request.form.get('complaintSubject')
            complaint_vo.complaint_description = request.form.get('complaintDescription')
            complaint_vo.complaint_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            complaint_vo.complaint_status = 'pending'
            complaint_vo.complaint_from_login_id = user_login_id
            complaint_vo.complaint_to_login_id = 1
            complain_dao.insert_complaint(complaint_vo)
            return redirect('/user/load_post_complaint')
        else:
            return logout_session()
    except Exception as ex:
        print('user_post_compaint route error occurred>>>>>>>>>>', ex)


@app.route('/admin/delete_complaint', methods=["GET"])
def admin_delete_complaint():
    try:
        if login_session() == "admin":
            complaint_vo = ComplaintVO()
            complaint_dao = ComplaintDAO()
            complaint_vo.complaint_id = request.args.get('complaintId')
            complaint_dao.delete_complaint(complaint_vo)
            return redirect(url_for('admin_view_complaint'))
        else:
            return logout_session()
    except Exception as ex:
        print('admin_delete_complaint route error occurred>>>>>>>>>>', ex)


@app.route('/admin/view_complaint', methods=["GET"])
def admin_view_complaint():
    try:
        if login_session() == 'admin':
            complaint_dao = ComplaintDAO()
            complaint_vo_list = complaint_dao.admin_complaint_list()
            return render_template('admin/view_files/viewComplaint.html', complaintdata=complaint_vo_list)
        else:
            return logout_session()
    except Exception as ex:
        print('admin_view_complaint route error occurred>>>>>>>>>>', ex)


@app.route('/admin/reply_complaint', methods=["GET"])
def admin_reply_complaint():
    try:
        if login_session() == 'admin':
            complaint_vo = ComplaintVO()
            complain_dao = ComplaintDAO()
            complaint_vo.complaint_id = request.args.get('complaintId')
            complaint_vo_list = complain_dao.get_complaint(complaint_vo)
            return render_template('admin/add_files/addReply.html', complaint_data=complaint_vo_list)
        else:
            return logout_session()
    except Exception as ex:
        print('admin_reply_complaint route error occurred>>>>>>>>>>', ex)


@app.route('/admin/replied_complaint', methods=["POST"])
def admin_replied_complaint():
    try:
        if login_session() == 'admin':

            login_vo = LoginVO()
            login_dao = LoginDAO()
            complaint_vo = ComplaintVO()
            complaint_dao = ComplaintDAO()

            login_username = request.cookies.get('login_username')
            login_vo.login_username = login_username

            user_login_id = login_dao.find_login_id(login_vo)

            complaint_vo.complaint_id = request.form.get('complaintId')
            complaint_vo.complaint_status = 'replied'
            complaint_vo.complaint_reply_description = request.form.get('replyDescription')
            complaint_vo.complaint_reply_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            complaint_vo.complaint_to_login_id = user_login_id
            complaint_dao.insert_replied_complaint(complaint_vo)

            return redirect(url_for('admin_view_complaint'))
        else:
            return logout_session()
    except Exception as ex:
        print('admin_replied_complaint route error occurred>>>>>>>>>>', ex)
