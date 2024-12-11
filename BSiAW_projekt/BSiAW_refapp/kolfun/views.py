from django.shortcuts import render, redirect, get_object_or_404
from authentication.forms import EdytujUser
from authentication.models import UserProfile, User
from game.models import Match, Zawodnik, Klub, Events
from django.core.mail import EmailMultiAlternatives
from .forms import DodajMeczForm
from django.contrib.auth.decorators import login_required
from .decorators import role_required, kol_required

# Create your views here.

@role_required('kol')
@login_required
def editusrk(request):
    user = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = EdytujUser(request.POST, instance=user.user)
        if form.is_valid():
            form.save()
            return redirect('committee_dashboard')
    else:
        form = EdytujUser(instance=user.user)
    return render(request, 'kolfun/userform.html', {'user': user, 'form': form})

@role_required('kol')
@login_required
def kolmecze(request):
    user = UserProfile.objects.get(user=request.user)
    wszystkiemecze = Match.objects.filter(Kolegium = user.user)
    context = {
        'mecze': wszystkiemecze,
    }
    return render(request, "kolfun/kolmecze.html", context)

@role_required('kol')
@login_required
@kol_required
def szczegolymeczuk(request, mecz_id):
    mecz = get_object_or_404(Match, pk=mecz_id)
    return render(request, 'kolfun/szczegolymeczuk.html', {'mecz': mecz})

@role_required('kol')
@login_required
@kol_required
def sprawozdaniek(request, mecz_id):
    mecz = get_object_or_404(Match, pk=mecz_id)
    if request.method == 'POST':
        mecz.status = "zaakceptowane"
        mecz.save()
        return render(request, 'kolfun/sprawozdaniek.html', {'mecz': mecz, })
    return render(request, 'kolfun/sprawozdaniek.html', {'mecz': mecz})
    
@role_required('kol')
@login_required
@kol_required
def sgospk(request, mecz_id):
    mecz = get_object_or_404(Match, pk=mecz_id)
    gospodarz = mecz.Gosp
    zawodnicy = Zawodnik.objects.filter(klub=gospodarz).order_by('nr')
    return render(request, 'kolfun/sgospk.html', {'mecz': mecz, 'zawodnicy': zawodnicy})


@role_required('kol')
@login_required
@kol_required
def sgosck(request, mecz_id):
    mecz = get_object_or_404(Match, pk=mecz_id)
    gosc = mecz.Gosc
    zawodnicy = Zawodnik.objects.filter(klub=gosc).order_by('nr')
    return render(request, 'kolfun/sgosck.html', {'mecz': mecz, 'zawodnicy': zawodnicy})
    
@role_required('kol')
@login_required
@kol_required
def eventk(request, mecz_id):
    mecz = get_object_or_404(Match, pk=mecz_id)
    wydarzenia = Events.objects.filter(mecz=mecz).order_by('minuta')
    return render(request, 'kolfun/eventk.html', {'mecz': mecz, 'wydarzenia': wydarzenia})

@role_required('kol')
@login_required
def addmecz(request):
    u1 = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = DodajMeczForm(request.POST)
        if form.is_valid():
            form.instance.Kolegium = u1.user
            #creator = u1.user
            mecz = form.save()
            sendinfoSG(mecz)
            sendinfoSA(mecz)
            sendinfoSAa(mecz)
            return redirect("kolmecze")
    else:
        form = DodajMeczForm
    return render(request, "kolfun/addmecz.html", {'form': form})

def sendinfoSG(mecz,):
    s1 = mecz.SedziaG
    #name = s1.username
    email = s1.email
    plain_message = f"Dostales nowa obsade na mecz: {mecz.Gosp} - {mecz.Gosc}\n " \
                    f"Data meczu: {mecz.data}, godzina {mecz.godzina}\n" \
                    f"W: {mecz.miejscowosc}\n" \
                    f"Ul: {mecz.ulica}\n" \
                    f"Kolejka: {mecz.kolejka}, {mecz.rozgrywki}\n" \
                    f"Kontakt do kolegium: {mecz.Kolegium.email}\n"
    message = EmailMultiAlternatives(
        subject="Nowa Obsada",
        body=plain_message,
        from_email=None,
        to=[email],
    )
    try:
        message.send()
    except:
        print("cos nie tak")

def sendinfoSA(mecz):
    if mecz.SedziaA1:
        s1 = mecz.SedziaA1
    #name = s1.username
        email = s1.email
        plain_message = f"Dostales nowa obsade na mecz: {mecz.Gosp} - {mecz.Gosc}\n " \
                        f"Data meczu: {mecz.data}\n " \
                        f"W: {mecz.miejscowosc}\n" \
                        f"Ul: {mecz.ulica}\n" \
                        f"Kolejka: {mecz.kolejka}, {mecz.rozgrywki}\n" \
                        f"Kontakt do kolegium: {mecz.Kolegium.email}\n"
        message = EmailMultiAlternatives(
            subject="Nowa Obsada",
            body=plain_message,
            from_email=None,
            to=[email],
        )
        try:
            message.send()
        except:
            print("cos nie tak")

def sendinfoSAa(mecz):
    if mecz.SedziaA2:
        s1 = mecz.SedziaA2
    #name = s1.username
        email = s1.email
        plain_message = f"Dostales nowa obsade na mecz: {mecz.Gosp} - {mecz.Gosc}\n " \
                        f"Data meczu: {mecz.data}\n " \
                        f"W: {mecz.miejscowosc}\n" \
                        f"Ul: {mecz.ulica}\n" \
                        f"Kolejka: {mecz.kolejka}, {mecz.rozgrywki}\n" \
                        f"Kontakt do kolegium: {mecz.Kolegium.email}\n"
        message = EmailMultiAlternatives(
            subject="Nowa Obsada",
            body=plain_message,
            from_email=None,
            to=[email],
        )
        try:
            message.send()
        except:
            print("cos nie tak")
    