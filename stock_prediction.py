# from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np
from sklearn import linear_model
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import PolynomialFeatures

def create_polynomial_regression_model(company, day, max_degree, x_train, x_test, y_train, y_test):
    rmse_train = []
    rmse_test = []
    r2_train = []
    r2_test = []
    
    for i in range(1,max_degree):
        poly_features = PolynomialFeatures(degree=i)

        x_train_poly = poly_features.fit_transform(x_train)

        poly_model = linear_model.LinearRegression()
        poly_model.fit(x_train_poly, y_train)

        y_pred = poly_model.predict(x_train_poly)
        y_test_pred = poly_model.predict(poly_features.fit_transform(x_test))

        rmse_train.append(np.sqrt(mean_squared_error(y_train, y_pred)))
        r2_train.append(r2_score(y_train, y_pred))

        rmse_test.append(np.sqrt(mean_squared_error(y_test, y_test_pred)))
        r2_test.append(r2_score(y_test, y_test_pred))

    ind = np.argmin(rmse_test)
    print(company, day, "Degree: ", ind+1)    
    print("The model performance for the test set")
    print("-------------------------------------------")
    print("RMSE of test set is {}".format(rmse_test[ind]))
    print("R2 score of test set is {}".format(r2_test[ind]))

    print("\n")

cleaned_data = "clean-twitter-data.csv"
data = pd.read_csv(cleaned_data).to_numpy()
data_dict = {}

for i in data:
    if i[0] in data_dict.keys():
        data_dict[i[0]].append(i[2:])
    else:
        data_dict[i[0]] = [i[2:]]

for company in data_dict.keys():
    comp_data = np.array(data_dict[company])
    x = comp_data[:,:-4]
    for i in range(-4,0):
        y = comp_data[:,i]
        x_train, x_test, y_train, y_test = train_test_split(x,y,test_size=.2)
        create_polynomial_regression_model(company, i, 5, x_train, x_test, y_train, y_test)