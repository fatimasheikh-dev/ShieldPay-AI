from django.shortcuts import render
from pathlib import Path
import joblib


# Project folder
BASE_DIR = Path(__file__).resolve().parent.parent


# Load trained ML model
model = joblib.load(
    BASE_DIR / "ml" / "fraud_model.pkl"
)

# Load transaction type encoder
encoder = joblib.load(
    BASE_DIR / "ml" / "transaction_type_encoder.pkl"
)


def ai_fraud_detection(request):

    result = None
    risk_score = None
    message = None

    if request.method == "POST":

        amount = request.POST.get("amount")
        receiver_name = request.POST.get("receiver_name")
        receiver_account = request.POST.get("receiver_account")
        transaction_type = request.POST.get("transaction_type")
        purpose = request.POST.get("purpose")

        if (
            not amount
            or not receiver_name
            or not receiver_account
            or not transaction_type
            or not purpose
        ):

            message = "Please provide all transaction details."

        else:

            try:

                amount = float(amount)

                receiver_length = len(
                    receiver_name.strip()
                )

                account_length = len(
                    receiver_account.strip()
                )

                purpose_length = len(
                    purpose.strip()
                )

                # Convert transaction type to number
                encoded_type = encoder.transform(
                    [transaction_type]
                )[0]

                # Prepare data for ML model
                transaction_data = [[
                    amount,
                    receiver_length,
                    account_length,
                    encoded_type,
                    purpose_length
                ]]

                # Get fraud probability
                probabilities = model.predict_proba(
                    transaction_data
                )[0]

                fraud_probability = probabilities[1]

                risk_score = round(
                    fraud_probability * 100
                )

                # Classification
                if risk_score >= 70:

                    result = "FRAUDULENT"

                    message = (
                        "AI detected a high probability "
                        "of fraud."
                    )

                elif risk_score >= 40:

                    result = "SUSPICIOUS"

                    message = (
                        "AI detected suspicious "
                        "transaction patterns."
                    )

                else:

                    result = "SAFE"

                    message = (
                        "AI detected a low probability "
                        "of fraud."
                    )

            except Exception as e:

                message = (
                    f"Analysis error: {str(e)}"
                )

    return render(
        request,
        "ai_fraud_detection.html",
        {
            "result": result,
            "risk_score": risk_score,
            "message": message,
        }
    )