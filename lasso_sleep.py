"""
Preston Stover 06.10.2026 - BERN02 - Kaggle Competition
Sleep_Duration with Lasso regression 
penalty strength (lambda, called `alpha` in scikit-learn)
"""
import pandas as pd
from sklearn.linear_model import LassoCV
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

# load data
train = pd.read_csv("train.csv")
test = pd.read_csv("test.csv")

# separate response (y) from predictors (x)
y = train["Sleep_Duration"]
X_train = train.drop(columns=["ID", "Sleep_Duration"]) # removes ID and y leaving only predictor vals
X_test = test.drop(columns=["ID"])

# turn categorical columns (Gender, Occupation, BMI, Sleep_Disorder) into 0/1 values for regression.
# ex: Occupation_Doctor,Occupation_Nurse,Occupation_Teacher all set to 0 value except for actual occupation of individual (1).
X_all = pd.get_dummies(pd.concat([X_train, X_test]), drop_first=True) # stack train and test first so both get exactly the same columns
X_train = X_all.iloc[:len(X_train)] # first set of rows = train
X_test = X_all.iloc[len(X_train):] # remaining rows = test

# Lasso model:
# Lasso needs predictors on the same scale, otherwise the penalty is unfair
model = make_pipeline(StandardScaler(), LassoCV(cv=10, random_state=1)) # fits Lasso and picks lambda by 10-fold covariance
model.fit(X_train, y)

# results
lasso = model[-1] # get last term of fitted Lasso covar
print("Chosen lambda:", round(lasso.alpha_, 4)) # alpha_ is learned from data
coefs = pd.Series(lasso.coef_, index=X_train.columns)
print("Kept variables:\n", coefs[coefs != 0].sort_values(key=abs, ascending=False).round(3))
print("Dropped variables:", list(coefs[coefs == 0].index))

# predict test set and save as csv
submission = pd.DataFrame({"ID": test["ID"], "Sleep_Duration": model.predict(X_test)})
submission.to_csv("submission.csv", index=False)
print(submission.head())
