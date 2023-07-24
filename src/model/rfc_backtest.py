from sklearn.ensemble import RandomForestClassifier
from tqdm import tqdm

import sys
sys.path.append('./src/misc')
import tools
import sql_tools

#import trailing dataset and create new column indicating O/U result. This will be the classification set.
path_to_data = "./src/sql/"

ntrail = int(input('Trail dataset (enter int): '))

data = sql_tools.read_database(path_to_data+"trailing_database.db", f"{ntrail}_game_trailing")
data = data[data['O/U_line']!='']
data['O/U_result'] = data.apply(lambda row: tools.OU(row['O/U_line'],float(row['total'])),axis=1)

X,y = tools.model_preprocessing(data,("2016-01-10","2023-12-12"))

#backtesting 
n = 15
n_estimators = 50
n_trials = 10
OU_results = list(y[-n:])

acc_vals = []

print(f"Backtesting for {n} games with {n_estimators} estimators with {n_trials} trials.\n")
for trial in tqdm(range(0,n_trials)):
    pred = []
    for i in range(0,n):
        rf_model = RandomForestClassifier(n_estimators=n_estimators)
        
        X_train = X[n+1-i:]
        y_train = y[n+1-i:]
        
        X_test = X[n-i]
        y_test = y[n-i]
        
        rf_model.fit(X_train,y_train)
        yhat = rf_model.predict(X_test.reshape(1, -1))
        
        pred.append(yhat[0])

    acc = tools.score_results(OU_results,pred)
    
    acc_vals.append(acc)
    
overall_acc = sum(acc_vals)/len(acc_vals)
print(f"\nRandom Forest Classifier achieved {overall_acc*100}% overall accruacy for the past {n} games. Accuracy is calculated from {n_trials} trials.")
    
