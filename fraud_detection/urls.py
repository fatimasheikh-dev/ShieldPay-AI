from django.urls import path
from .views import ai_fraud_detection


urlpatterns = [
    path(
        "",
        ai_fraud_detection,
        name="ai_fraud_detection"
    ),
]