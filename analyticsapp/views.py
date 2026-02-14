from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from applications.models import Application

@login_required
def analytics_page(request):
    qs = Application.objects.filter(owner=request.user)

    total = qs.count()
    offers = qs.filter(outcome="offer").count()
    rejected = qs.filter(outcome="rejected").count()
    interviews = qs.filter(outcome="interview").count()
    success = int((offers / total) * 100) if total else 0

    start = timezone.now() - timedelta(weeks=10)
    weekly = (
        qs.filter(created_at__gte=start)
          .extra(select={"week": "strftime('%%Y-%%W', created_at)"})
          .values("week")
          .annotate(count=Count("id"))
          .order_by("week")
    )

    return render(request, "analytics.html", {
        "summary": {"total": total, "offers": offers, "rejected": rejected, "interviews": interviews, "success": success},
        "weekly": list(weekly),
    })
