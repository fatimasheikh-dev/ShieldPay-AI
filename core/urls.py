from django.urls import path
from . import views


urlpatterns = [

    path(
        "",
        views.dashboard,
        name="dashboard"
    ),

    path(
        "transaction-checker/",
        views.transaction_checker,
        name="transaction_checker"
    ),

    path(
        "transaction-history/",
        views.transaction_history,
        name="transaction_history"
    ),

    path(
        "ai-fraud-detection/",
        views.ai_fraud_detection,
        name="ai_fraud_detection"
    ),

    path(
        "slip-scanner/",
        views.slip_scanner,
        name="slip_scanner"
    ),

    path(
        "scam-url-checker/",
        views.scam_url_checker,
        name="scam_url_checker"
    ),

    path(
        "recovery-center/",
        views.recovery_center,
        name="recovery_center"
    ),

    path(
        "recovery-case/<str:case_id>/",
        views.recovery_case,
        name="recovery_case"
    ),

]
