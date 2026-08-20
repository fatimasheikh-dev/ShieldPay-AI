
from django.shortcuts import render
from .models import Transaction, RecoveryIncident


def dashboard(request):
    return render(
        request,
        "dashboard.html"
    )


def transaction_checker(request):

    result = None
    risk_score = None

    if request.method == "POST":

        amount = request.POST.get("amount")
        receiver = request.POST.get("receiver")
        bank = request.POST.get("bank")

        try:
            amount_value = float(amount)
        except (TypeError, ValueError):
            amount_value = 0

        risk_score = 20

        if amount_value >= 100000:
            risk_score += 40
        elif amount_value >= 50000:
            risk_score += 25
        elif amount_value >= 20000:
            risk_score += 15

        if not receiver:
            risk_score += 20

        if not bank:
            risk_score += 20

        risk_score = min(risk_score, 100)

        if risk_score >= 70:
            result = "FRAUD"
        elif risk_score >= 40:
            result = "SUSPICIOUS"
        else:
            result = "SAFE"

        try:
            Transaction.objects.create(
                amount=amount_value,
                receiver_name=receiver or "Unknown",
                receiver_account="Not provided",
                bank=bank or "Unknown",
                transaction_type="Online",
                purpose="Transaction Check",
                risk_score=risk_score,
                result=result
            )
        except Exception:
            pass

    return render(
        request,
        "transaction_checker.html",
        {
            "result": result,
            "risk_score": risk_score
        }
    )


def transaction_history(request):

    transactions = Transaction.objects.all().order_by(
        "-created_at"
    )

    return render(
        request,
        "transaction_history.html",
        {
            "transactions": transactions
        }
    )


def ai_fraud_detection(request):

    result = None
    risk_score = None

    if request.method == "POST":

        amount = request.POST.get("amount")

        transaction_type = request.POST.get(
            "transaction_type",
            "Online"
        )

        receiver = request.POST.get(
            "receiver",
            ""
        ).strip()

        try:
            amount_value = float(amount)
        except (TypeError, ValueError):
            amount_value = 0

        risk_score = 10

        # Amount risk
        if amount_value >= 100000:
            risk_score += 50

        elif amount_value >= 50000:
            risk_score += 35

        elif amount_value >= 20000:
            risk_score += 20

        elif amount_value >= 10000:
            risk_score += 10

        # Transaction type risk
        if transaction_type == "Mobile Wallet":
            risk_score += 10

        elif transaction_type == "Online":
            risk_score += 5

        # Receiver check
        if not receiver:
            risk_score += 20

        # Keep score between 0 and 100
        risk_score = min(
            risk_score,
            100
        )

        # Final result
        if risk_score >= 70:
            result = "HIGH RISK"

        elif risk_score >= 40:
            result = "MEDIUM RISK"

        else:
            result = "LOW RISK"

    return render(
        request,
        "ai_fraud_detection.html",
        {
            "result": result,
            "risk_score": risk_score
        }
    )


def slip_scanner(request):

    result = None

    if request.method == "POST":

        uploaded_file = request.FILES.get(
            "slip"
        )

        if uploaded_file:

            result = (
                "Payment slip uploaded successfully. "
                "Further verification is required."
            )

        else:

            result = (
                "Please upload a payment slip."
            )

    return render(
        request,
        "slip_scanner.html",
        {
            "result": result
        }
    )


def scam_url_checker(request):

    result = None
    risk_score = None
    warnings = []

    if request.method == "POST":

        url = request.POST.get(
            "url",
            ""
        ).strip().lower()

        if not url:

            result = "Please enter a URL."

        else:

            risk_score = 0

            # =========================
            # CHECK 1 — HTTPS
            # =========================

            if url.startswith("http://"):

                risk_score += 15

                warnings.append(
                    "Website is using HTTP instead of HTTPS."
                )

            elif not url.startswith("https://"):

                risk_score += 10

                warnings.append(
                    "URL does not use a standard HTTPS format."
                )


            # =========================
            # CHECK 2 — IP ADDRESS
            # =========================

            import re

            ip_pattern = (
                r"https?://"
                r"(?:\d{1,3}\.){3}\d{1,3}"
            )

            if re.match(
                ip_pattern,
                url
            ):

                risk_score += 30

                warnings.append(
                    "URL uses an IP address instead of a domain name."
                )


            # =========================
            # CHECK 3 — @ SYMBOL
            # =========================

            if "@" in url:

                risk_score += 25

                warnings.append(
                    "URL contains an @ symbol, which can hide the real destination."
                )


            # =========================
            # CHECK 4 — DOMAIN HYPHENS
            # =========================

            domain_part = url

            if "://" in domain_part:

                domain_part = domain_part.split(
                    "://",
                    1
                )[1]

            domain_part = domain_part.split(
                "/",
                1
            )[0]

            if domain_part.count("-") >= 3:

                risk_score += 15

                warnings.append(
                    "Domain contains an unusually high number of hyphens."
                )


            # =========================
            # CHECK 5 — SUSPICIOUS WORDS
            # =========================

            suspicious_words = [

                "login",
                "verify",
                "verification",
                "secure",
                "account",
                "update",
                "password",
                "wallet",
                "payment",
                "bank",
                "confirm",
                "claim",
                "reward",
                "free",
                "gift",
                "bonus"

            ]

            found_words = []

            for word in suspicious_words:

                if word in url:

                    found_words.append(
                        word
                    )


            if len(found_words) >= 3:

                risk_score += 25

                warnings.append(
                    "URL contains multiple security-sensitive keywords."
                )

            elif len(found_words) >= 1:

                risk_score += 10

                warnings.append(
                    "URL contains potentially sensitive keywords."
                )


            # =========================
            # CHECK 6 — URL LENGTH
            # =========================

            if len(url) > 100:

                risk_score += 10

                warnings.append(
                    "URL is unusually long."
                )


            # =========================
            # CHECK 7 — DOUBLE SLASH
            # =========================

            if "//" in url[8:]:

                risk_score += 15

                warnings.append(
                    "URL contains an unusual double-slash pattern."
                )


            # =========================
            # LIMIT SCORE
            # =========================

            risk_score = min(
                risk_score,
                100
            )


            # =========================
            # FINAL RESULT
            # =========================

            if risk_score >= 60:

                result = "SUSPICIOUS"

            elif risk_score >= 30:

                result = "SUSPICIOUS"

            else:

                result = "SAFE"


            # =========================
            # NO WARNING
            # =========================

            if not warnings:

                warnings.append(
                    "No obvious suspicious patterns were detected by the basic URL checks."
                )


    return render(
        request,
        "scam_url_checker.html",
        {
            "result": result,
            "risk_score": risk_score,
            "warnings": warnings
        }
    )


def recovery_center(request):

    if request.method == "POST":

        incident_type = request.POST.get(
            "incident_type",
            "Fraud Incident"
        )

        transaction_id = request.POST.get(
            "transaction_id",
            ""
        )

        amount = request.POST.get(
            "amount"
        )

        bank = request.POST.get(
            "bank",
            ""
        )

        description = request.POST.get(
            "description",
            ""
        )

        if not amount:
            amount = None

        RecoveryIncident.objects.create(
            incident_type=incident_type,
            transaction_id=transaction_id,
            amount=amount,
            bank=bank,
            description=description,
            status="PENDING"
        )

    incidents = (
        RecoveryIncident.objects
        .all()
        .order_by("-created_at")
    )

    total_cases = incidents.count()

    pending_cases = incidents.filter(
        status="PENDING"
    ).count()

    in_progress_cases = incidents.filter(
        status="IN_PROGRESS"
    ).count()

    resolved_cases = incidents.filter(
        status="RESOLVED"
    ).count()

    return render(
        request,
        "recovery_center.html",
        {
            "incidents": incidents,
            "total_cases": total_cases,
            "pending_cases": pending_cases,
            "in_progress_cases": in_progress_cases,
            "resolved_cases": resolved_cases
        }
    )


def recovery_case(
    request,
    case_id
):

    try:

        incident = RecoveryIncident.objects.get(
            case_id=case_id
        )

    except RecoveryIncident.DoesNotExist:

        return render(
            request,
            "recovery_case_not_found.html"
        )

    if request.method == "POST":

        action = request.POST.get(
            "action"
        )

        if action == "bank_reported":

            incident.bank_reported = True

        elif action == "account_secured":

            incident.account_secured = True

        elif action == "evidence_saved":

            incident.evidence_saved = True

        elif action == "status":

            new_status = request.POST.get(
                "status"
            )

            valid_statuses = [
                "PENDING",
                "IN_PROGRESS",
                "RESOLVED"
            ]

            if new_status in valid_statuses:

                incident.status = new_status

        if (
            incident.bank_reported
            and incident.account_secured
            and incident.evidence_saved
            and incident.status == "PENDING"
        ):

            incident.status = "IN_PROGRESS"

        incident.save()

    completed_actions = 0

    if incident.bank_reported:
        completed_actions += 1

    if incident.account_secured:
        completed_actions += 1

    if incident.evidence_saved:
        completed_actions += 1

    progress = completed_actions * 33

    if completed_actions == 3:
        progress = 100

    return render(
        request,
        "recovery_case.html",
        {
            "incident": incident,
            "completed_actions": completed_actions,
            "progress": progress
        }
    )
