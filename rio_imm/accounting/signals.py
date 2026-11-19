from decimal import Decimal

from django.db.models.signals import post_save
from django.dispatch import receiver

from rio.models import Applicant


@receiver(post_save, sender=Applicant)
def create_initial_invoice_for_applicant(sender, instance: Applicant, created: bool, **kwargs):
    """
    Invoice creation is now handled directly inside add_applicant()
    to avoid duplicate invoice generation and UNIQUE constraint errors.
    """
    return