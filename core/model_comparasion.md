# Phishgaurd AI -Model Comparson Report 
## Objective 
Compare Three Models  to select  the best one  for url  Phishing Detection
## Model Tested 
-Logistic Regression 
-Random Forest(100 treees)
-XGBoost (100 estimators)
## Dataset 
-Source: Kaggle web page  phishing Detection  Dataset 
-Total Rows:11,430(Balanced :5715 phishing , 5715 Legitimate )
-feature Used : 33 URL-extractable  features 
-Train/ Test split : 80/20

## Evaluation Method 
-Single train/test split (80/20)
-5-fold cross validation for  reliable comparision 
-primary metric F1 Score (macro Average )
# Results 
| Model               | CV F1  | Variance  | Test Accuracy |
|---------------------|--------|-----------|---------------|
| Logistic Regression | 0.8063 | ±0.0066   | 0.82          |
| Random Forest       | 0.8807 | ±0.0051   | 0.88          |
| XGBoost             | 0.8766 | ±0.0090   | 0.90          |

## Winner: Random Forest

## Reasoning
Random Forest was selected for the following reasons:

1. Highest CV F1 score (0.8807) — best average performance across all 5 folds
2. Lowest variance (±0.0051) — most consistent model, least likely to perform 
   poorly on unseen data
3. Logistic Regression scored 0.8063 — confirms the problem is too complex 
   for a simple linear model
4. XGBoost scored higher on single test accuracy (0.90) but lower CV score 
   and higher variance — less reliable for a security tool where consistency matters
5. For a security tool, consistency is more important than peak accuracy

## Limitations
- Only 33 of 87 available features used (URL-extractable only)
- No webpage content features — limits detection of clean-URL phishing
- Model may miss phishing sites with simple, clean URLs (false negatives)
- Dataset is balanced 50/50 — real world phishing ratio is different