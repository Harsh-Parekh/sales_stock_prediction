from flask import render_template, jsonify, request, redirect, url_for

from base import app
from base.com.controller.login_controller import login_session, logout_session
from base.com.dao.area_dao import AreaDAO
from base.com.dao.city_dao import CityDAO
from base.com.dao.state_dao import StateDAO
from base.com.vo.area_vo import AreaVO
from base.com.vo.city_vo import CityVO
from base.com.vo.state_vo import StateVO


@app.route('/admin/ajax_city')
def admin_ajax_city():
    try:
        if login_session() == 'admin':
            area_dao = AreaDAO()
            city_vo = CityVO()
            city_vo.city_state_id = request.args.get('stateId')
            city_vo_list = area_dao.view_ajax_city_area(city_vo)
            data = [i.as_dict() for i in city_vo_list]
            return jsonify(data)
        else:
            return logout_session()
    except Exception as ex:
        print('admin_ajax_city route error occurred>>>>>>>>>>', ex)


@app.route('/admin/load_area', methods=["GET"])
def admin_load_area():
    try:
        if login_session() == 'admin':
            state_vo = StateDAO()
            state_vo_list = state_vo.search_state()
            return render_template('admin/add_files/addArea.html', state_data=state_vo_list)
        else:
            return logout_session()
    except Exception as ex:
        print('admin_load_area route exception occurred>>>>>>>>>>', ex)


@app.route('/admin/insert_area', methods=["POST"])
def admin_insert_area():
    try:
        if login_session() == 'admin':
            area_vo = AreaVO()
            area_dao = AreaDAO()
            area_vo.area_state_id = request.form.get('areastateId')
            area_vo.area_city_id = request.form.get('areacityId')
            area_vo.area_name = request.form.get('areaName')
            area_vo.area_pincode = request.form.get('areaPincode')
            area_dao.insert_area(area_vo)
            return redirect(url_for('admin_view_area'))
        else:
            return logout_session()
    except Exception as ex:
        print('admin_insert_area route exception occurred>>>>>>>>>>', ex)


@app.route('/admin/view_area', methods=["GET"])
def admin_view_area():
    try:
        if login_session() == 'admin':
            area_dao = AreaDAO()
            area_vo_list = area_dao.search_area()
            return render_template('admin/view_files/viewArea.html', area_data=area_vo_list)
        else:
            return logout_session()
    except Exception as ex:
        print('admin_view_area route exception occurred>>>>>>>>>>', ex)


@app.route('/admin/delete_area', methods=["GET"])
def admin_delete_area():
    try:
        if login_session() == 'admin':
            area_vo = AreaVO()
            area_dao = AreaDAO()
            area_vo.area_id = request.args.get('areaId')
            area_dao.delete_area(area_vo)
            return redirect(url_for('admin_view_area'))
        else:
            return logout_session()
    except Exception as ex:
        print('admin_delete_area route exception occurred>>>>>>>>>>', ex)


@app.route('/admin/edit_area', methods=['GET'])
def admin_edit_area():
    try:
        if login_session() == 'admin':
            area_vo = AreaVO()
            state_dao = StateDAO()
            state_vo = StateVO()
            city_dao = CityDAO()
            area_dao = AreaDAO()
            area_vo.area_id = request.args.get('areaId')
            state_city_area = area_dao.join_city_data(area_vo)
            state_vo_list = state_dao.search_state()
            state_vo.state_id = state_city_area[0][2].state_id
            city_vo_list = city_dao.get_city(state_vo)
            area_vo_list = area_dao.edit_area(area_vo)
            return render_template('admin/edit_files/editArea.html', area_data=area_vo_list, state_data=state_vo_list,
                                   city_data=city_vo_list, multi_record=state_city_area)
        else:
            return logout_session()
    except Exception as ex:
        print('admin_edit_area route exception occurred>>>>>>>>>>', ex)


@app.route('/admin/update_area', methods=["POST"])
def admin_update_area():
    try:
        if login_session() == 'admin':
            area_vo = AreaVO()
            area_dao = AreaDAO()
            area_vo.area_id = request.form.get('areaId')
            area_vo.area_name = request.form.get('areaName')
            area_vo.area_pincode = request.form.get('areaPincode')
            area_vo.area_state_id = request.form.get('areastateId')
            area_vo.area_city_id = request.form.get('areacityId')
            area_dao.update_area(area_vo)
            return redirect(url_for('admin_view_area'))
        else:
            return logout_session()
    except Exception as ex:
        print('admin_update_area exception occurred>>>>>>>>>>', ex)
