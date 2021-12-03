from flask import render_template, request, redirect, url_for

from base import app
from base.com.controller.login_controller import login_session, logout_session
from base.com.dao.city_dao import CityDAO
from base.com.dao.state_dao import StateDAO
from base.com.vo.city_vo import CityVO


@app.route('/admin/load_city', methods=["GET"])
def admin_load_city():
    try:
        if login_session() == 'admin':
            state_dao = StateDAO()
            state_vo_list = state_dao.search_state()
            return render_template('admin/addfiles/addCity.html', state_data=state_vo_list)
        else:
            return logout_session()

    except Exception as ex:
        print("admin_load_city route exception occured>>>>>>>>>", ex)


@app.route('/admin/insert_city', methods=["POST"])
def admin_insert_city():
    try:
        if login_session() == 'admin':
            city_vo = CityVO()
            city_dao = CityDAO()
            city_vo.city_state_id = request.form.get('citystateId')
            city_vo.city_name = request.form.get('cityName')
            city_vo.city_description = request.form.get('cityDescription')
            if city_vo.city_name and city_vo.city_description:
                city_dao.insert_city(city_vo)
                return redirect(url_for('admin_view_city'))
            else:
                return redirect(url_for('admin_load_city'))
        else:
            return logout_session()
    except Exception as ex:
        print("admin_insert_city route exception occured>>>>>>>>>>", ex)


@app.route('/admin/view_city', methods=["GET"])
def admin_view_city():
    try:
        if login_session() == 'admin':
            city_dao = CityDAO()
            city_dao_list = city_dao.search_city()
            return render_template('admin/viewfiles/viewCity.html', city_data=city_dao_list)
        else:
            return logout_session()
    except Exception as ex:
        print("admin_view_city route exception occured>>>>>>>>>", ex)


@app.route('/admin/delete_city', methods=["GET"])
def admin_delete_city():
    try:
        if login_session() == 'admin':
            city_vo = CityVO()
            city_dao = CityDAO()
            city_id = request.args.get('cityId')
            city_vo.city_id = city_id
            city_dao.delete_city(city_vo)
            return redirect(url_for('admin_view_city'))
        else:
            return logout_session()
    except Exception as ex:
        print("admin_delete_state route exception occured>>>>>>>>>>", ex)


@app.route('/admin/edit_city/', methods=["GET"])
def admin_edit_city():
    try:
        if login_session() == 'admin':
            state_dao = StateDAO()
            city_vo = CityVO()
            city_dao = CityDAO()
            state_dao_list = state_dao.search_state()
            city_id = request.args.get('cityId')
            city_vo.city_id = city_id
            city_vo_list = city_dao.edit_city(city_vo)
            return render_template('admin/editfiles/editCity.html', city_data=city_vo_list, state_data=state_dao_list)
        else:
            return logout_session()
    except Exception as ex:
        print("admin_edit_city route exception occured>>>>>>>>>>", ex)


@app.route('/admin/update_city', methods=["POST"])
def admin_update_city():
    try:
        if login_session() == 'admin':
            city_vo = CityVO()
            city_dao = CityDAO()
            city_vo.city_id = request.form.get('cityId')
            city_vo.city_state_id = request.form.get('citystateId')
            city_vo.city_name = request.form.get('cityName')
            city_vo.city_description = request.form.get('cityDescription')
            city_dao.update_city(city_vo)
            return redirect(url_for('admin_view_city'))
        else:
            return logout_session()
    except Exception as ex:
        print("admin_update_city route exception occured>>>>>>>>>>", ex)
