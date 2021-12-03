from flask import render_template, request, redirect, url_for

from base import app
from base.com.controller.login_controller import login_session, logout_session
from base.com.dao.user_dao import UserDAO
from base.com.vo.login_vo import LoginVO


@app.route('/admin/view_user_organization', methods=['GET'])
def admin_view_user_organization():
    try:
        if login_session() == 'admin':
            user_dao = UserDAO()
            user_vo_list = user_dao.search_user()
            print(user_vo_list)
            return render_template('admin/viewfiles/viewUserOrganization.html', user_list=user_vo_list)
        else:
            return logout_session()
    except Exception as ex:
        print('admin_view_organization route error occured>>>>>>>>>>', ex)


@app.route('/admin/user_block_unblock', methods=['GET'])
def admin_user_block_unblock():
    try:
        if login_session() == 'admin':
            login_vo = LoginVO()
            user_dao = UserDAO()
            login_vo.login_id = request.args.get('loginId')
            user_dao.user_block_unblock(login_vo)
            return redirect(url_for('admin_view_user_organization'))
        else:
            return logout_session()
    except Exception as ex:
        print('admin_user_block route error occured>>>>>>>>>', ex)
