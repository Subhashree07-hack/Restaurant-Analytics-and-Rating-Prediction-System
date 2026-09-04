import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle

df = pd.read_csv("data/loan_approval.csv")

features = ["income", "credit_score", "loan_amount", "years_employed"]

X = df[features]
y = df["loan_approved"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier()
model.fit(X_train, y_train)

print("Accuracy:", model.score(X_test, y_test))

pickle.dump(model, open("model/loan_model.pkl", "wb"))
print("Model saved")