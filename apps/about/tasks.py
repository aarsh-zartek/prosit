from prosit.celery import app

from apps.about.models import ContactForm

from lib.utils import last_month_from_today


@app.task
def delete_old_contact_forms() -> str:

    contact_forms = ContactForm.objects.filter(created__date__lt=last_month_from_today())
    deleted, _ = contact_forms.delete()

    return f"Successfully Deleted {deleted} Contact Forms"
