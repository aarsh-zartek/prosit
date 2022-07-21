from prosit.celery import app

from apps.about.models import ContactForm

from lib.utils import last_month_from_today


@app.task
def delete_old_contact_forms() -> str:
    """Deletes all Contact Form queries older than 30 days"""

    deleted, _ = ContactForm.objects.filter(
        created__date__lt=last_month_from_today()
    ).delete()

    return f"Successfully Deleted {deleted} Contact Forms"
