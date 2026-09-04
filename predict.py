import pandas as pd

def predict_loan(model, income, credit, loan, years):

    data = pd.DataFrame(
        [[income, credit, loan, years]],
        columns=[
            "income",
            "credit_score",
            "loan_amount",
            "years_employed"
        ]
    )

    prediction = model.predict(data)[0]
    probability = model.predict_proba(data)[0][1] * 100

    return prediction, probability