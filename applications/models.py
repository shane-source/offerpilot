from django.db import models
from django.conf import settings

class Stage(models.Model):
    name = models.CharField(max_length=60, unique=True)
    position = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["position"]

    def __str__(self):
        return self.name

class Application(models.Model):
    STATUS = [("open", "Open"), ("closed", "Closed")]
    OUTCOME = [("none", "None"), ("interview", "Interview"), ("offer", "Offer"), ("rejected", "Rejected")]

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="job_apps")
    stage = models.ForeignKey(Stage, on_delete=models.PROTECT, related_name="apps")

    company = models.CharField(max_length=120)
    job_title = models.CharField(max_length=120)
    location = models.CharField(max_length=120, blank=True, default="")
    job_url = models.URLField(blank=True, default="")

    status = models.CharField(max_length=10, choices=STATUS, default="open")
    outcome = models.CharField(max_length=12, choices=OUTCOME, default="none")
    position = models.PositiveIntegerField(default=0)

    company_logo = models.ImageField(upload_to="logos/", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["stage__position", "position", "-updated_at"]

    def __str__(self):
        return f"{self.company} - {self.job_title}"

class Note(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name="notes")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

class Attachment(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name="attachments")
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    label = models.CharField(max_length=80, default="CV")
    file = models.FileField(upload_to="attachments/")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
