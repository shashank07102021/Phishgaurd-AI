import pandas as pd 
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score   
from sklearn.metrics import classification_report
from xgboost import XGBClassifier
import json

df=pd.read_csv("D:/Phishgaurd AI/data/dataset_phishing.csv")

with open("D:/Phishgaurd AI/core/features.json","r") as f:
    features=json.load(f)
    X=df[features]
    y=(df['status']=='phishing').astype(int)


    X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2, random_state=42) 

    models={"Logistic Regression ": LogisticRegression(max_iter=1000),
    "Random Forest Classifier ": RandomForestClassifier(n_estimators=100,random_state=42),
    "XGBoost": XGBClassifier(n_estimators =100,random_state=42,eval_metric='logloss')}
     
    results={}

    for name , models in models.items():
        print(f"\n --{name}--")

        models.fit(X_train, y_train)

        y_pred=models.predict(X_test)
        print(classification_report(y_test,y_pred))

        cv_scores=cross_val_score(models,X,y,cv=5, scoring='f1_macro')
        print(f"5-fold CV F1:{cv_scores.mean():.4f}(+/-{cv_scores.std():.4f})")
        
        results[name]=cv_scores.mean()

print("\n--Summary ---")
for name,score in results.items():
    print(f"{name}: {score:.4f}")

winner=max(results,key=results.get)
print(f"\nBest Model: {winner}" ) 