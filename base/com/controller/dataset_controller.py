import os
from datetime import datetime

from flask import render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

from base import app, UPLOAD_FOLDER
from base.com.controller.login_controller import login_session, logout_session
from base.com.dao.dataset_dao import DatasetDAO
from base.com.vo.dataset_vo import DatasetVO
from base.com.dao.login_dao import LoginDAO
from base.com.vo.login_vo import LoginVO

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


@app.route('/admin/load_dataset', methods=['GET'])
def admin_load_dataset():
    try:
        if login_session() == 'admin':
            return render_template('admin/addfiles/addDataset.html')
        else:
            return logout_session()
    except Exception as ex:
        print('admin_load_dataset exception occurred>>>>>>>>>>', ex)


@app.route('/user/load_dataset', methods=['GET'])
def user_load_dataset():
    try:
        if login_session() == 'user':
            return render_template('user/addDataset.html')
        else:
            return logout_session()
    except Exception as ex:
        print('user_load_dataset exception occurred>>>>>>>>>>', ex)


@app.route('/admin/view_dataset', methods=['GET'])
def admin_view_dataset():
    try:
        if login_session() == 'admin':
            dataset_vo = DatasetDAO()
            dataset_vo_list = dataset_vo.search_datatset()
            return render_template('admin/viewfiles/viewDataset.html', dataset_data=dataset_vo_list)
        else:
            return logout_session()
    except Exception as ex:
        print('admin_view_dataset exception occurred>>>>>>>>>>', ex)


@app.route('/user/view_dataset', methods=['GET'])
def user_view_dataset():
    try:
        if login_session() == 'user':
            dataset_vo = DatasetDAO()

            login_dao = LoginDAO()
            login_vo = LoginVO()
            login_username = request.cookies.get('login_username')
            login_vo.login_username = login_username
            user_login_id = login_dao.find_login_id(login_vo)

            dataset_vo_list = dataset_vo.search_dataset_user(user_login_id)
            return render_template('user/viewDataset.html', dataset_data=dataset_vo_list)
        else:
            return logout_session()
    except Exception as ex:
        print('user_view_dataset exception occurred>>>>>>>>>>', ex)


@app.route('/admin/insert_dataset', methods=['POST'])
def admin_insert_dataset():
    try:
        if login_session() == 'admin':
            dataset_vo = DatasetVO()
            dataset_dao = DatasetDAO()

            login_dao = LoginDAO()
            login_vo = LoginVO()
            login_username = request.cookies.get('login_username')
            login_vo.login_username = login_username
            user_login_id = login_dao.find_login_id(login_vo)

            dataset_fileobject = request.files.get('datasetFilename')
            dataset_vo.dataset_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            dataset_vo.dataset_filename = secure_filename(dataset_fileobject.filename)
            dataset_vo.dataset_description = request.form.get('datasetDescription')
            dataset_vo.dataset_filepath = UPLOAD_FOLDER.replace('base', '..')
            dataset_vo.dataset_by = user_login_id
            dataset_fileobject.save(os.path.join(UPLOAD_FOLDER, dataset_fileobject.filename))
            dataset_dao.insert_dataset(dataset_vo)

            return redirect(url_for('admin_view_dataset'))
        else:
            return logout_session()
    except Exception as ex:
        print('admin_insert_dataset exception occurred>>>>>>>>>>', ex)


@app.route('/user/insert_dataset', methods=['POST'])
def user_insert_dataset():
    try:
        if login_session() == 'user':
            dataset_vo = DatasetVO()
            dataset_dao = DatasetDAO()

            login_dao = LoginDAO()
            login_vo = LoginVO()
            login_username = request.cookies.get('login_username')
            login_vo.login_username = login_username
            user_login_id = login_dao.find_login_id(login_vo)

            dataset_fileobject = request.files.get('datasetFilename')
            dataset_vo.dataset_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            dataset_vo.dataset_filename = secure_filename(dataset_fileobject.filename)
            dataset_vo.dataset_description = request.form.get('datasetDescription')
            dataset_vo.dataset_filepath = UPLOAD_FOLDER.replace('base', '..')
            dataset_vo.dataset_by = user_login_id
            dataset_fileobject.save(os.path.join(UPLOAD_FOLDER, dataset_fileobject.filename))
            dataset_dao.insert_dataset(dataset_vo)

            sender = "salesstockpredictiondonotreply@gmail.com"
            receiver = login_username
            msg = MIMEMultipart()
            msg['From'] = sender
            msg['To'] = receiver
            msg['Subject'] = "Your dataset is uploaded"
            message = """
            Hello {},
            We are glad to know you that your dataset {},
            is successfully received by the admin.
            As per our term after uploading own dataset you have to wait for 48 hours,
            so our team can easily analyze your dataset.
            After completion of work from our side,our admin will contact you and explain you that how
            you can predict your sales for upcomming period,month or year according to your dataset.
            So please keep patience.
            
            Thank you for joining us,
            have a great day.
            """.format(login_username, request.files.get('datasetFilename'))

            msg.attach(MIMEText(message, 'plain'))

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender, "salesstockprediction")
            text = msg.as_string()
            server.sendmail(sender, receiver, text)
            server.quit()

            sender = "salesstockpredictiondonotreply@gmail.com"
            receiver = "salesstockpredictiondonotreply@gmail.com"
            msg = MIMEMultipart()
            msg['From'] = sender
            msg['To'] = receiver
            msg['Subject'] = "New dataset is uploaded by user"
            message = """
            Our SSP user :{} has uploaded a new dataset kindly contact him,
            after viewing.
            """.format(login_username)
            msg.attach(MIMEText(message, 'plain'))

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender, "salesstockprediction")
            text = msg.as_string()
            server.sendmail(sender, receiver, text)
            server.quit()

            return redirect(url_for('user_view_dataset'))
        else:
            return logout_session()
    except Exception as ex:
        print('user_insert_dataset exception occurred>>>>>>>>>>', ex)


@app.route('/admin/delete_dataset')
def admin_delete_dataset():
    try:
        if login_session() == 'admin':
            dataset_dao = DatasetDAO()
            dataset_vo = DatasetVO()
            dataset_vo.dataset_id = request.args.get('datasetId')
            dataset_dao.delete_dataset(dataset_vo)
            return redirect(url_for('admin_view_dataset'))
        else:
            return logout_session()
    except Exception as ex:
        print('admin_delete_dataset exception occurred>>>>>>>>>>', ex)
