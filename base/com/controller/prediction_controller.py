from flask import render_template, request, redirect, url_for

from base import app
from base.com.controller.login_controller import login_session, logout_session
from base.com.vo.prediction_vo import PredictionVO
from base.com.dao.prediction_dao import PredictionDAO
from base.com.vo.login_vo import LoginVO
from base.com.dao.login_dao import LoginDAO
import pickle
import pandas as pd
from datetime import datetime

stock_type_dic = {'Pain Relievers': 34, 'Hair Oil': 20, 'Noodles': 33, 'Cartidges': 6, 'Soft Drink': 42, 'Razors': 39,
                  'Women Trouser': 51, 'Dishwashes': 13, 'Sanitary Care': 40, 'Pasta': 35, 'Canned Foods': 5,
                  'Coffee': 11, 'Men Jeans': 25, 'Energy Drink': 15, "Men's Deo": 29, 'Pooja Needs': 38,
                  'ToothPaste': 47, 'Cleaners': 10, 'Ketchups': 22, 'Girls Shirt': 19, 'Men Shirt': 26,
                  'Tissues & Disposables': 45, 'Milk Drink': 30, 'Tea': 44, 'Breads Grains': 3, 'Dog Supplies': 14,
                  'Biscuits': 0, 'ToothBrush': 46, 'Conditioner': 12, 'Women Shirt': 49, 'Pickels': 37,
                  'Women T-Shirt': 50, 'Lip Care': 24, 'Candy': 4, 'Shampoo': 41, 'Sweets': 43, 'Perfumes': 36,
                  'Chips': 8, "Women's Deo": 52, 'Laundry Detergents': 23, 'Frozen Foods': 18, 'Face Wash': 17,
                  'Boys Shirt': 2, 'Namkeen': 32, 'Men Trouser': 28, 'Face Cream': 16, 'Women Jeans': 48,
                  'Body Lotion': 1, 'Men T-Shirt': 27, 'MouthWash': 31, 'Chocklate': 9, 'Cat Supplies': 7,
                  'Hand Wash': 21}


@app.route('/admin/view_prediction', methods=['GET'])
def admin_view_prediction():
    try:
        if login_session() == 'admin':
            prediction_dao = PredictionDAO()
            prediction_vo_list = prediction_dao.search_prediction()
            return render_template('admin/viewfiles/viewPredictions.html', prediction_vo_list=prediction_vo_list)
        else:
            return logout_session()
    except Exception as ex:
        print('admin_view_prediction route error occurred>>>>>>>>>>', ex)


@app.route('/user/add_prediction', methods=['GET'])
def user_add_prediction():
    try:
        if login_session() == 'user':
            return render_template("user/addPrediction.html", stock_type_dic=stock_type_dic)
        else:
            return logout_session()
    except Exception as ex:
        print('user_add_prediction route error occurred>>>>>>>>>>', ex)


@app.route('/user/perform_prediction', methods=['POST'])
def user_perform_prediction():
    try:
        if login_session() == 'user':

            login_vo = LoginVO()
            login_dao = LoginDAO()
            login_username = request.cookies.get('login_username')
            login_vo.login_username = login_username
            user_login_id = login_dao.find_login_id(login_vo)

            prediction_vo = PredictionVO()
            prediction_stock_type = request.form.get("stock_type")
            prediction_stock_purchased_season = int(request.form.get("season_purchase_season"))
            prediction_stock_sell_season = int(request.form.get("stock_sell_season"))
            prediction_stock_purchased_month = int(request.form.get("stock_purchase_month"))
            prediction_no_stock_purchased = int(request.form.get("no_stock_purchased"))

            prediction_no_stock_returned = 0
            prediction_no_stock_remains = (int(request.form.get("no_stock_purchased")) * 5) // 100

            prediction_stock_sell_duration_months = int(request.form.get("stock_sell_duration_month"))
            prediction_year = int(request.form.get("year"))

            file = open('/home/spy/projectworkspace/salesstockprediction/machine_learning_module/StockModel.pkl', 'rb')
            model = pickle.load(file)
            df = pd.DataFrame([[prediction_no_stock_purchased, prediction_no_stock_returned,
                                prediction_no_stock_remains, prediction_stock_type, prediction_stock_purchased_season,
                                prediction_stock_sell_season, prediction_stock_purchased_month,
                                prediction_stock_sell_duration_months, prediction_year]])
            df.columns = ["No_Stock_Purchased", "No_Stock_Returned", "No_Stock_Remains", "Stock_Type",
                          "Stock_Purchased_Season", "Stock_Sell_Season", "Stock_Purchased_Month",
                          "Stock_Sell_Duration_Months", "Year"]
            df["Stock_Type"] = stock_type_dic[prediction_stock_type]
            print(df)
            prediction_no_stock_sell = int(round(model.predict(df)[0]))

            season = {1: "summer", 2: "winter", 3: "monsoon"}
            month = {1: "january", 2: "february", 3: "march", 4: "april", 5: "may", 6: "june", 7: "july", 8: "august",
                     9: "suptember", 10: "octomber", 11: "november", 12: "december"}

            prediction_stock_purchased_month = month[prediction_stock_purchased_month]
            prediction_stock_sell_season = season[prediction_stock_sell_season]
            prediction_stock_purchased_season = season[prediction_stock_purchased_season]

            prediction_vo.prediction_login_id = user_login_id
            prediction_vo.prediction_stock_type = prediction_stock_type
            prediction_vo.prediction_stock_purchased_season = prediction_stock_purchased_season
            prediction_vo.prediction_stock_sell_season = prediction_stock_sell_season
            prediction_vo.prediction_stock_purchased_month = prediction_stock_purchased_month
            prediction_vo.prediction_no_stock_purchased = prediction_no_stock_purchased
            prediction_vo.prediction_no_stock_returned = prediction_no_stock_returned
            prediction_vo.prediction_no_stock_remains = prediction_no_stock_remains
            prediction_vo.prediction_stock_sell_duration_months = prediction_stock_sell_duration_months
            prediction_vo.prediction_year = prediction_year
            prediction_vo.prediction_no_stock_sell = prediction_no_stock_sell
            prediction_vo.prediction_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            prediction_dao = PredictionDAO()
            prediction_dao.insert_prediction(prediction_vo)

            return redirect(url_for("user_view_prediction"))
        else:
            return logout_session()
    except Exception as ex:
        print('user_perform_prediction route error occuerd>>>>>>>>>>', ex)


@app.route('/user/view_prediction', methods=['GET'])
def user_view_prediction():
    try:
        if login_session() == 'user':
            login_vo = LoginVO()
            login_dao = LoginDAO()
            prediction_dao = PredictionDAO()

            login_username = request.cookies.get('login_username')
            login_vo.login_username = login_username

            user_login_id = login_dao.find_login_id(login_vo)

            prediction_vo_list = prediction_dao.user_prediction(user_login_id)
            return render_template("user/viewPredictions.html", prediction_vo_list=prediction_vo_list)
        else:
            return logout_session()
    except Exception as ex:
        print('user_view_prediction route error occurred>>>>>>>>>>', ex)


@app.route('/user/view_previous_prediction', methods=['GET'])
def user_view_previous_prediction():
    try:
        if login_session() == 'user':
            prediction_vo = PredictionVO()
            prediction_dao = PredictionDAO()
            predictionId = request.args.get('predictionId')
            prediction_vo.prediction_id = predictionId
            prediction_vo_list = prediction_dao.previous_prediction(prediction_vo)
            return render_template("user/viewpredictionData.html", prediction_vo_list=prediction_vo_list)
        else:
            return logout_session()
    except Exception as ex:
        print('user_view_prediction route error occurred>>>>>>>>>>', ex)


@app.route('/admin/view_prediction_data_user', methods=['GET'])
def admin_view_prediction_data_user():
    try:
        if login_session() == 'admin':
            prediction_vo = PredictionVO()
            prediction_dao = PredictionDAO()
            predictionId = request.args.get('predictionId')
            prediction_vo.prediction_id = predictionId
            prediction_vo_list = prediction_dao.previous_prediction(prediction_vo)
            return render_template("admin/viewfiles/viewpredictionData.html", prediction_vo_list=prediction_vo_list)
        else:
            return logout_session()
    except Exception as ex:
        print('admin_view_prediction_data_user route error occurred>>>>>>>>>>', ex)


@app.route('/user/view_prediction_data', methods=['GET'])
def user_view_prediction_data():
    try:
        if login_session() == 'user':
            prediction_vo = PredictionVO()
            prediction_dao = PredictionDAO()
            predictionId = request.args.get('predictionId')
            prediction_vo.prediction_id = predictionId
            prediction_vo_list = prediction_dao.previous_prediction(prediction_vo)
            return render_template("user/viewpredictionData.html", prediction_vo_list=prediction_vo_list)
        else:
            return logout_session()
    except Exception as ex:
        print('admin_view_prediction_data_user route error occurred>>>>>>>>>>', ex)
