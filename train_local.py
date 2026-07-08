import joblib
import lightgbm as lgb
import pandas as pd
import boto3
from imblearn.combine import SMOTETomek

bucket = "customer-satisfaction-with-deploy"
key_train = "data/train_final.csv"
key_test="data/test_final.csv"

s3=boto3.client('s3')

obj_train=s3.get_object(Bucket=bucket,Key=key_train)
obj_test=s3.get_object(Bucket=bucket,Key=key_test)



train_df = pd.read_csv(obj_train["Body"])
test_df = pd.read_csv(obj_test["Body"])

test_df.drop('Unnamed: 0',axis=1,inplace=True)

X_train = train_df.drop(columns=["satisfaction"])
y_train = train_df["satisfaction"]
X_test = test_df.drop(columns=["satisfaction"])
y_test = test_df["satisfaction"]

tomek=SMOTETomek(random_state=42)
X_train_resampled,y_train_resampled=tomek.fit_resample(X_train,y_train)

model = lgb.LGBMClassifier(
    num_leaves=35,
    max_depth=6,
    learning_rate=0.1,
    n_estimators=250,
)
model.fit(X_train_resampled, y_train_resampled, eval_set=[(X_test, y_test)])

print("Test accuracy:", model.score(X_test, y_test))
joblib.dump(model, "model.joblib")
print("Saved model.joblib")