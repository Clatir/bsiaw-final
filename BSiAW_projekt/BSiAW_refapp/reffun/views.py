from django.shortcuts import render, redirect, get_object_or_404
from authentication.forms import EdytujUser
from authentication.models import UserProfile, User
from django.db.models import Q
from game.models import Match, Klub, Zawodnik, Events
from .forms import EdytujMeczForm, DodajZawodnikaForm, DodajEventForm
from django.contrib.auth.decorators import login_required
from .decorators import role_required, referee_required, referees_required
# Create your views here.

@role_required('ref')
@login_required
def editusr(request):
    user = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = EdytujUser(request.POST, instance=user.user)
        if form.is_valid():
            form.save()
            return redirect('judge_dashboard')
    else:
        form = EdytujUser(instance=user.user)
    return render(request, 'reffun/userform.html', {'user': user, 'form': form})
    
@role_required('ref')
@login_required    
def listameczy(request):
    user = UserProfile.objects.get(user=request.user)
    warunek = Q(SedziaG = user.user) | Q(SedziaA1 = user.user) | Q(SedziaA2 = user.user)
    wszystkiemecze = Match.objects.filter(warunek)
    context = {
        'mecze': wszystkiemecze,
    }
    return render(request, "game/meczlist.html", context)
    
@role_required('ref')
@login_required
@referees_required
def szczegolymeczu(request, mecz_id):
    mecz = get_object_or_404(Match, pk=mecz_id)
    return render(request, 'game/szczegolymeczu.html', {'mecz': mecz})
    

@role_required('ref')
@login_required
@referee_required
def sprawozdanie(request, mecz_id):
    mecz = get_object_or_404(Match, pk=mecz_id)
    if request.method == 'POST':
        form = EdytujMeczForm(request.POST, instance=mecz)
        if form.is_valid():
            form.save()
            return render(request, 'reffun/sprawozdanie.html', {'mecz': mecz, 'form': form})
    else:
        form = EdytujMeczForm(instance=mecz)
    return render(request, 'reffun/sprawozdanie.html', {'mecz': mecz, 'form': form})
    

@role_required('ref')
@login_required  
@referee_required  
def sgosp(request, mecz_id):
    mecz = get_object_or_404(Match, pk=mecz_id)
    gospodarz = mecz.Gosp
    zawodnicy = Zawodnik.objects.filter(klub=gospodarz).order_by('nr')
    return render(request, 'reffun/sgosp.html', {'mecz': mecz, 'zawodnicy': zawodnicy})

@role_required('ref')
@login_required
@referee_required
def sgosc(request, mecz_id):
    mecz = get_object_or_404(Match, pk=mecz_id)
    gosc = mecz.Gosc
    zawodnicy = Zawodnik.objects.filter(klub=gosc).order_by('nr')
    return render(request, 'reffun/sgosc.html', {'mecz': mecz, 'zawodnicy': zawodnicy})
    
@role_required('ref')
@login_required  
@referee_required  
def event(request, mecz_id):
    mecz = get_object_or_404(Match, pk=mecz_id)
    wydarzenia = Events.objects.filter(mecz=mecz).order_by('minuta')
    return render(request, 'reffun/event.html', {'mecz': mecz, 'wydarzenia': wydarzenia})

@role_required('ref')
@login_required
@referee_required
def addevent(request, mecz_id):
    mecz = get_object_or_404(Match, pk=mecz_id)
    if request.method == 'POST':
        form = DodajEventForm(request.POST)
        if form.is_valid():
            form.instance.mecz = mecz
            form.save()
            return redirect('event', mecz.id)
    else:
        form = DodajEventForm
    return render(request, "reffun/addevent.html", {'form': form, 'mecz': mecz})    
    
@role_required('ref')
@login_required
@referee_required    
def addzawodnikh(request, mecz_id):
    mecz = get_object_or_404(Match, pk=mecz_id)
    if request.method == 'POST':
        form = DodajZawodnikaForm(request.POST)
        if form.is_valid():
            form.instance.klub = mecz.Gosp
            form.save()
            return redirect('sgosp', mecz.id)
    else:
        form = DodajZawodnikaForm
    return render(request, "reffun/addzaw.html", {'form': form, 'mecz': mecz})
    
@role_required('ref')
@login_required
@referee_required
def addzawodnika(request, mecz_id):
    mecz = get_object_or_404(Match, pk=mecz_id)
    if request.method == 'POST':
        form = DodajZawodnikaForm(request.POST)
        if form.is_valid():
            form.instance.klub = mecz.Gosc
            form.save()
            return redirect('sgosc', mecz.id)
    else:
        form = DodajZawodnikaForm
    return render(request, "reffun/addzawa.html", {'form': form, 'mecz': mecz})
    
