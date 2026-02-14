def seed_stages(sender, **kwargs):
    from .models import Stage

    defaults = ["Applied", "Shortlisted", "Interview", "Offer", "Rejected"]
    for i, name in enumerate(defaults, start=1):
        Stage.objects.get_or_create(name=name, defaults={"position": i})
