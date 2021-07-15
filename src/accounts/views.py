from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Profile


@login_required
def profile(request):
    data = None
    try:
        profile = Profile.objects.get(user=request.user)
        data = profile
    except Profile.DoesNotExist:
        pass
    return render(request, 'accounts/profile.html', {'data':data})

@login_required
def create_profile(request):
    if request.method == 'GET':
        return render(request, 'accounts/create_profile.html')
    data = request.POST
    profile = Profile()
    profile.user = request.user
    profile.name = data.get('name',None)
    profile.firstname = data.get('firstname',None)
    profile.lastname = data.get('lastname',None)
    profile.phone = data.get('phone',None)
    profile.address = data.get('address',None)
    profile.website = data.get('website',None)
    profile.save()
    return redirect('profile')


@login_required
def update_profile(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'GET':
        return render(request, 'accounts/update_profile.html',{'data':profile})
    data = request.POST
    profile.name = data.get('name',None)
    profile.firstname = data.get('firstname',None)
    profile.lastname = data.get('lastname',None)
    profile.phone = data.get('phone',None)
    profile.address = data.get('address',None)
    profile.website = data.get('website',None)
    profile.save()
    return redirect('profile')
    



