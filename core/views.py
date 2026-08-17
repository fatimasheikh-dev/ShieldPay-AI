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

        try:
            amount_value = float(amount)
        except (TypeError, ValueError):
            amount_value = 0

        risk_score = 15

        if amount_value >= 100000:
            risk_score += 50
        elif amount_value >= 50000:
            risk_score += 30
        elif amount_value >= 20000:
            risk_score += 15

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

        uploaded_file = request.FILES.get("slip")

        if uploaded_file:
            result = (
                "Payment slip uploaded successfully. "
                "Further verification is required."
            )
        else:
            result = "Please upload a payment slip."

    return render(
        request,
        "slip_scanner.html",
        {
            "result": result
        }
    )


def scam_url_checker(request):

    result = None

    if request.method == "POST":

        url = request.POST.get(
            "url",
            ""
        ).strip()

        if not url:
            result = "Please enter a URL."

        elif (
            url.startswith("https://")
            and "." in url
        ):
            result = (
                "URL appears safe for basic checks."
            )

        else:
            result = (
                "Suspicious URL. "
                "Please verify before opening."
            )

    return render(
        request,
        "scam_url_checker.html",
        {
            "result": result
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

    search_query = request.GET.get(
        "search",
        ""
    ).strip()

    status_filter = request.GET.get(
        "status",
        "ALL"
    ).strip()

    incidents = (
        RecoveryIncident.objects
        .all()
        .order_by("-created_at")
    )

    if search_query:

        incidents = incidents.filter(

            case_id__icontains=search_query

        ) | incidents.filter(

            transaction_id__icontains=search_query

        ) | incidents.filter(

            incident_type__icontains=search_query

        ) | incidents.filter(

            bank__icontains=search_query

        )

    if status_filter in [
        "PENDING",
        "IN_PROGRESS",
        "RESOLVED"
    ]:

        incidents = incidents.filter(
            status=status_filter
        )

    incidents = incidents.distinct().order_by(
        "-created_at"
    )

    all_incidents = RecoveryIncident.objects.all()

    total_cases = all_incidents.count()

    pending_cases = all_incidents.filter(
        status="PENDING"
    ).count()

    in_progress_cases = all_incidents.filter(
        status="IN_PROGRESS"
    ).count()

    resolved_cases = all_incidents.filter(
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
            "resolved_cases": resolved_cases,
            "search_query": search_query,
            "status_filter": status_filter
        }
    )


def recovery_case(request, case_id):

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

            uploaded_file = request.FILES.get(
                "evidence_file"
            )

            if uploaded_file:

                incident.evidence_file = uploaded_file
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
