from flask import render_template, request, redirect, url_for

from base import app
from base.com.controller.login_controller import login_session, logout_session
from base.com.dao.state_dao import StateDAO
from base.com.vo.state_vo import StateVO


@app.route('/admin/load_state', methods=["GET"])
def admin_load_state():
    try:
        if login_session() == 'admin':
            return render_template('admin/addfiles/addState.html')
        else:
            return logout_session()

    except Exception as ex:
        print("admin_load_state route exception occurred>>>>>>>>>>", ex)


@app.route('/admin/insert_state', methods=["POST"])
def admin_insert_state():
    try:
        if login_session() == 'admin':
            state_vo = StateVO()
            state_dao = StateDAO()
            state_vo.state_name = request.form.get('stateName')
            state_vo.state_description = request.form.get('stateDescription')
            state_dao.insert_state(state_vo)
            return redirect(url_for('admin_view_state'))
        else:
            return logout_session()
    except Exception as ex:
        print("admin_insert_state route exception occurred>>>>>>>>>>", ex)


@app.route('/admin/view_state', methods=["GET"])
def admin_view_state():
    try:
        if login_session() == "admin":
            state_dao = StateDAO()
            state_vo_list = state_dao.search_state()
            return render_template('admin/viewfiles/viewState.html', state_data=state_vo_list)
        else:
            return logout_session()
    except Exception as ex:
        print("admin_view_state route exception occurred>>>>>>>>>>", ex)


@app.route('/admin/delete_state', methods=["GET"])
def admin_delete_state():
    try:
        if login_session() == 'admin':
            state_vo = StateVO()
            state_dao = StateDAO()
            state_id = request.args.get('stateId')
            state_vo.state_id = state_id
            state_dao.delete_state(state_vo)
            return redirect(url_for('admin_view_state'))
        else:
            return logout_session()
    except Exception as ex:
        print("admin_delete_state route exception occurred>>>>>>>>>>", ex)


@app.route('/admin/edit_state/', methods=["GET"])
def admin_edit_state():
    try:
        if login_session() == 'admin':
            state_vo = StateVO()
            state_dao = StateDAO()
            state_id = request.args.get('stateId')
            state_vo.state_id = state_id
            state_vo_list = state_dao.edit_state(state_vo)
            return render_template('admin/editfiles/editState.html', state_data=state_vo_list)
        else:
            return logout_session()
    except Exception as ex:
        print("admin_edit_state route exception occurred>>>>>>>>>>", ex)


@app.route('/admin/update_state', methods=["POST"])
def admin_update_state():
    try:
        if login_session() == 'admin':
            state_vo = StateVO()
            state_dao = StateDAO()
            state_vo.state_id = request.form.get('stateId')
            state_vo.state_name = request.form.get('stateName')
            state_vo.state_description = request.form.get('stateDescription')
            if state_vo.state_name and state_vo.state_description:
                state_dao.update_state(state_vo)
                return redirect(url_for('admin_view_state'))
            else:
                return redirect('/admin/edit_state/?stateId=' + str(state_vo.state_id))
        else:
            return logout_session()
    except Exception as ex:
        print("admin_update_state route exception occurred>>>>>>>>>>", ex)
