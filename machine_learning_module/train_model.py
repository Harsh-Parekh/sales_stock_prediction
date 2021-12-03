import pickle

import pandas as pd
import scipy.stats as st
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from xgboost.sklearn import XGBRegressor

dfStock = pd.read_csv(r'dataset.csv')

dfStock.drop(['Stock_Id'], axis=1, inplace=True)
dfStock.apply(lambda x: sum(x.isnull()), axis=0)
dfStock = dfStock[~pd.isnull(dfStock).any(axis=1)]
y = dfStock.No_Stock_Sell

X = dfStock.drop(['No_Stock_Sell'], axis=1)

CategoryList = ['Stock_Type']  # Categorical features

for feature in X[CategoryList]:  # Loop through all columns in the dataframe
    X[feature] = pd.Categorical(X[feature]).codes  # Convert to categorical features

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.35, random_state=123)
X_train.fillna(X_train.mean())
y_train.fillna(y_train.mean())
X_test.fillna(X_test.mean())
y_test.fillna(y_test.mean())

one_to_left = st.beta(10, 1)
from_zero_positive = st.expon(0, 50)
params = {
    "n_estimators": st.randint(3, 40),
    "max_depth": st.randint(3, 40),
    "learning_rate": st.uniform(0.05, 0.4),
    "colsample_bytree": one_to_left,
    "subsample": one_to_left,
    "gamma": st.uniform(0, 10),
    'reg_alpha': from_zero_positive,
    "min_child_weight": from_zero_positive
}

xgbreg = XGBRegressor(nthread=-1)
rsCV = RandomizedSearchCV(xgbreg, params, n_jobs=1)
rsCV.fit(X_train, y_train)
clf = XGBRegressor(**rsCV.best_params_)
clf.fit(X_train, y_train)

prediction = clf.predict(X_test)
print(prediction)
predict_dict = {'prediction': prediction}
with open(r"StockModel.pkl", 'wb') as fp:
    pickle.dump(clf, fp)
accuracy = clf.score(X_test, y_test)
print("Model Accuracy=%.2f" % (accuracy * 100.0))
print("MAE=%.2f" % mean_absolute_error(y_test, prediction))
print("MSE=%.2f" % mean_squared_error(y_test, prediction))
r2_score_value = r2_score(y_test, prediction)
print("r2 score=", r2_score_value)
