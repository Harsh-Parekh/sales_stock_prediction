from datetime import datetime

from flask import render_template, request, redirect, url_for

from base import app
from base.com.controller.login_controller import logout_session, login_session
from base.com.dao.feedback_dao import FeedbackDAO
from base.com.dao.login_dao import LoginDAO
from base.com.vo.feedback_vo import FeedbackVO
from base.com.vo.login_vo import LoginVO


@app.route('/user/load_post_feedback', methods=['GET'])
def user_load_post_feedback():
    try:
        if login_session() == 'user':

            login_dao = LoginDAO()
            login_vo = LoginVO()
            feedback_dao = FeedbackDAO()

            login_username = request.cookies.get('login_username')
            login_vo.login_username = login_username
            user_login_id = login_dao.find_login_id(login_vo)

            feedbacks = feedback_dao.user_feedback_list(user_login_id)

            return render_template('user/feedback.html', feedbacks=feedbacks, username=login_username)
        else:
            return logout_session()
    except Exception as ex:
        print('user_load_post_feedback route error occurred>>>>>>>>>>', ex)


@app.route('/user/post_feedback', methods=['POST'])
def user_post_feedback():
    try:
        if login_session() == 'user':
            feedback_vo = FeedbackVO()
            feedback_dao = FeedbackDAO()
            login_dao = LoginDAO()
            login_vo = LoginVO()

            login_username = request.cookies.get('login_username')
            login_vo.login_username = login_username
            user_login_id = login_dao.find_login_id(login_vo)

            feedback_vo.feedback_rating = request.form.get('rate')
            feedback_vo.feedback_description = request.form.get('feedbackDescription')
            feedback_vo.feedback_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            feedback_vo.feedback_login_id = user_login_id
            feedback_dao.insert_feedback(feedback_vo)
            return redirect('/user/load_post_feedback')
        else:
            return logout_session()
    except Exception as ex:
        print('user_post_feedback route error occurred>>>>>>>>>>', ex)


@app.route('/admin/delete_feedback', methods=['GET'])
def admin_delete_feedback():
    try:
        if login_session() == 'admin':
            feedback_dao = FeedbackDAO()
            feedback_vo = FeedbackVO()
            feedback_vo.feedback_id = request.args.get('feedbackId')
            feedback_dao.delete_feedback(feedback_vo)
            return redirect(url_for('admin_view_feedback'))
        else:
            return logout_session()
    except Exception as ex:
        print('admin_delete_feedback route error occurred>>>>>>>>>>', ex)


@app.route('/admin/view_feedback', methods=['GET'])
def admin_view_feedback():
    try:
        if login_session() == 'admin':
            feedback_dao = FeedbackDAO()
            feedback_vo_list = feedback_dao.admin_feeback_list()
            return render_template('admin/view_files/viewFeedback.html', feedbackdata=feedback_vo_list)
        else:
            return logout_session()
    except Exception as ex:
        print('admin_view_feedback route error occurred>>>>>>>>>>', ex)
