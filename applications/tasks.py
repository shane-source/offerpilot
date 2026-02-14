from celery import shared_task
from django.utils import timezone
from django.core.mail import send_mail
from .models import Reminder, Notification

@shared_task
def send_due_reminders():
    now = timezone.now()
    due = Reminder.objects.filter(status="pending", remind_at__lte=now).select_related("created_by", "application")

    count = 0
    for r in due:
        user = r.created_by
        app = r.application
        msg = r.message or f"Reminder: {app.company} - {app.job_title}"

        if r.channel == "email" and user.email:
            send_mail(
                subject=f"OfferPilot Reminder: {app.company}",
                message=msg,
                from_email=None,
                recipient_list=[user.email],
                fail_silently=False,
            )

        if r.channel == "in_app":
            Notification.objects.create(user=user, title=f"Reminder: {app.company}", body=msg)

        r.status = "sent"
        r.sent_at = now
        r.save(update_fields=["status", "sent_at"])
        count += 1

    return count


