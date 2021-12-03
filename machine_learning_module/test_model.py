import pickle
import warnings

import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

with open('StockModel.pkl', 'rb') as fp:
    model_load = pickle.load(fp)

dfStock = pd.read_csv(r'dataset.csv')


def testData(dfStock):
    dfStock.drop(['Stock_Id'], axis=1, inplace=True)
    dfStock.apply(lambda x: sum(x.isnull()), axis=0)
    dfStock = dfStock[~pd.isnull(dfStock).any(axis=1)]
    y = dfStock.No_Stock_Sell
    X = dfStock.drop(['No_Stock_Sell'], axis=1)
    CategoryList = ['Stock_Type']
    for feature in X[CategoryList]:
        X[feature] = pd.Categorical(X[feature]).codes

    prediction = model_load.predict(X)
    print("MAE=%.2f" % mean_absolute_error(y, prediction))
    print("MSE=%.2f" % mean_squared_error(y, prediction))
    r2_score_value = r2_score(y, prediction)
    print("r2 score=", r2_score_value)
    fo = open("Prediction.txt", "w+")
    for i in prediction:
        fo.write(str(i) + "\n")


testData(dfStock)
