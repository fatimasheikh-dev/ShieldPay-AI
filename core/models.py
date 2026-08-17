from django.db import models


class Transaction(models.Model):

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    receiver_name = models.CharField(
        max_length=150
    )

    receiver_account = models.CharField(
        max_length=150
    )

    bank = models.CharField(
        max_length=150
    )

    transaction_type = models.CharField(
        max_length=50
    )

    purpose = models.CharField(
        max_length=255
    )

    risk_score = models.IntegerField()

    result = models.CharField(
        max_length=30
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.receiver_name} - {self.result}"


class RecoveryIncident(models.Model):

    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("IN_PROGRESS", "In Progress"),
        ("RESOLVED", "Resolved"),
    ]

    incident_type = models.CharField(
        max_length=100
    )

    transaction_id = models.CharField(
        max_length=150,
        blank=True
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    bank = models.CharField(
        max_length=150,
        blank=True
    )

    description = models.TextField()

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="PENDING"
    )

    case_id = models.CharField(
        max_length=30,
        unique=True,
        blank=True
    )

    bank_reported = models.BooleanField(
        default=False
    )

    account_secured = models.BooleanField(
        default=False
    )

    evidence_saved = models.BooleanField(
        default=False
    )

    evidence_file = models.FileField(
        upload_to="recovery_evidence/",
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def save(self, *args, **kwargs):

        if not self.case_id:

            last_case = (
                RecoveryIncident.objects
                .order_by("-id")
                .first()
            )

            if last_case:
                next_number = last_case.id + 1
            else:
                next_number = 1

            self.case_id = f"SP-REC-{next_number:05d}"

        super().save(*args, **kwargs)

    def __str__(self):

        return (
            f"{self.case_id} - "
            f"{self.incident_type}"
        )