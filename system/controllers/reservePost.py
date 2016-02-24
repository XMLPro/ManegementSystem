from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from system.controllers.postFinishView import finish
from system.models import Reserved, Equipment
from django.http import Http404


def reverse_or_404(default_name, name=None):
    try:
        return reverse(name if name else default_name)
    except:
        raise Http404


def reservePost(request):
    backname = request.GET.get("backname")
    if request.method == "POST":
        equipment = Equipment.objects.get(id=request.POST["equipment_id"])
        if not Reserved.objects.filter(
                equipment=equipment, user=request.user).exists():
            reserve = Reserved(equipment=equipment, user=request.user)
            reserve.save()
            return finish("reserve")
    return redirect(reverse_or_404("system:top", backname))


def cancelPost(request):
    backname = request.GET.get("backname")
    if request.method == "POST":
        equipment = Equipment.objects.get(id=request.POST["equipment_id"])
        reserved = Reserved.objects.get(equipment=equipment, user=request.user)
        if reserved:
            reserved.delete()
        return finish("cancel_reserve")
    return redirect(reverse_or_404("system:top", backname))
