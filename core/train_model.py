import pandas as pd 
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
import json 

df=pd.read_csv("D:/Phishgaurd AI/data/dataset_phishing.csv")

features=['length_url','length_hostname','ip','nb_dots','nb_hyphens','nb_at','nb_qm','nb_and','nb_or','nb_eq','nb_underscore','nb_tilde',
          'nb_percent','nb_slash','nb_star','nb_colon','nb_comma','nb_semicolumn','nb_dollar','nb_space','nb_www','nb_com','nb_dslash',
          'https_token','ratio_digits_url','ratio_digits_host','punycode','port','tld_in_path','tld_in_subdomain','nb_subdomains','shortening_service',
          'path_extension']

X=df[features]
y=df['status']
X_train, X_test, y_train, y_test=train_test_split(X , y, test_size=0.2, random_state=42 )
print("Training Rows:",len(X_train))
print("Testing Rows :",len(X_test))
print("Training Model ")

model=RandomForestClassifier(n_estimators=100,random_state=42)
model.fit(X_train,y_train)

y_pred=model.predict(X_test)
print("\n Results ")
print(classification_report(y_test,y_pred))

joblib.dump(model , "D:/Phishgaurd AI/core/phishing_model.pkl")

with open("D:/Phishgaurd AI/core/features.json","w") as f:
    json.dump(features,f)

    print("Model and feature list saved ")