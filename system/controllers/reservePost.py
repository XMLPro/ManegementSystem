from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from system.controllers.postFinishView import finish
from system.models import Reserved, Equipment
from system.controllers.utils import reverse_or_404


def reservePost(request):
    # リダイレクト先の受け取り
    backname = request.GET.get("backname")
    backtitle = request.GET.get("backtitle")

    if request.method == "POST":
        equipment = Equipment.objects.get(id=request.POST["equipment_id"])
        if not Reserved.objects.filter(
                equipment=equipment, user=request.user).exists():
            reserve = Reserved(equipment=equipment, user=request.user)
            reserve.save()
            return finish("reserve", backname, backtitle)
    return redirect(reverse_or_404("system:top", backname))


def cancelPost(request):
    # リダイレクト先の受け取り
    backname = request.GET.get("backname")
    backtitle = request.GET.get("backtitle")

    if request.method == "POST":
        reserved_id = request.POST.get("reserved_id")
        if reserved_id:
            reserved = Reserved.objects.get(id=reserved_id)
        else:
            equipment = Equipment.objects.get(id=request.POST["equipment_id"])
            reserved = Reserved.objects.get(
                equipment=equipment, user=request.user)
        if reserved:
            reserved.delete()
        return finish("cancel_reserve", backname, backtitle)
    return redirect(reverse_or_404("system:top", backname))
