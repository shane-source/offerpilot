from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.contrib import messages

from .models import Stage, Application, Note, Attachment
from .seed import ensure_default_stages

@login_required
def board(request):
    ensure_default_stages()
    q = request.GET.get("q", "").strip()

    stages = Stage.objects.all()
    apps = Application.objects.filter(owner=request.user).select_related("stage")

    if q:
        apps = apps.filter(company__icontains=q) | apps.filter(job_title__icontains=q) | apps.filter(location__icontains=q)

    apps = apps.order_by("position", "-updated_at")

    cards_by_stage = {s.id: [] for s in stages}
    for a in apps:
        cards_by_stage[a.stage_id].append(a)

    return render(request, "board.html", {"stages": stages, "cards_by_stage": cards_by_stage, "q": q})

@login_required
@require_POST
def create_application(request):
    stage = get_object_or_404(Stage, id=request.POST.get("stage"))
    app = Application.objects.create(
        owner=request.user,
        stage=stage,
        company=request.POST.get("company", "").strip(),
        job_title=request.POST.get("job_title", "").strip(),
        location=request.POST.get("location", "").strip(),
        job_url=request.POST.get("job_url", "").strip(),
        position=0,
    )
    logo = request.FILES.get("company_logo")
    if logo:
        app.company_logo = logo
        app.save()
    return redirect("/board/")

@login_required
@require_POST
def move_card(request):
    app = get_object_or_404(Application, id=request.POST.get("app_id"), owner=request.user)
    stage = get_object_or_404(Stage, id=request.POST.get("stage_id"))
    app.stage = stage
    app.position = int(request.POST.get("position", 0))
    app.save()
    return JsonResponse({"ok": True})

@login_required
def notes(request, app_id):
    app = get_object_or_404(Application, id=app_id, owner=request.user)
    if request.method == "POST":
        body = request.POST.get("body", "").strip()
        if body:
            Note.objects.create(application=app, author=request.user, body=body)
            return redirect(f"/app/{app.id}/notes/")
    return render(request, "notes.html", {"app": app, "notes": app.notes.all()})

@login_required
def attachments(request, app_id):
    app = get_object_or_404(Application, id=app_id, owner=request.user)
    if request.method == "POST":
        f = request.FILES.get("file")
        if not f:
            messages.error(request, "Select a file first.")
            return redirect(f"/app/{app.id}/attachments/")
        Attachment.objects.create(
            application=app,
            uploaded_by=request.user,
            label=request.POST.get("label", "CV"),
            file=f
        )
        return redirect(f"/app/{app.id}/attachments/")
    return render(request, "attachments.html", {"app": app, "items": app.attachments.all()})
