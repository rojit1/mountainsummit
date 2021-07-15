from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from .models import Package, Book

"""
Default home page
"""
def home(request):
    return render(request, 'dashboard/home.html')


"""
Package section
"""

@login_required
def add_packages(request):
    if request.method == "GET":
        if request.user.type == 'ORGANIZATION':
            return render(request, 'dashboard/add_packages.html')
        return redirect('/')

    if request.method == 'POST':
        data = request.POST
        file = request.FILES.get('image','')
        Package.objects.create(title=data['title'],location=data['location'], seats=data['seats'],image=file,date=data.get('date',''),description=data['description'],org_id = request.user.pk)
        return redirect('org-packages',org=request.user.pk)

def all_packages(request):
    data = Package.objects.all();
    return render(request, 'dashboard/packages.html',{'data':data})

def package_details(request, id):
    data = get_object_or_404(Package,pk=id)
    user_packages = [ item.package.pk for item in Book.objects.filter(user=request.user,package_id=id)]
    return render(request, 'dashboard/package_details.html',{'package':data,'user_packages':user_packages})

@login_required
def org_packages(request, org):
    if request.user.type == 'ORGANIZATION':
        data = Package.objects.filter(org_id=org)
        return render(request, 'dashboard/org_packages.html',{'data':data})
    return redirect('/')

@login_required
def org_package_edit(request, package):
    if request.user.type == 'ORGANIZATION':
        package = get_object_or_404(Package,pk=package)
        if request.user.pk != package.org_id:
            return redirect('/')
        if request.method == 'GET':
            return render(request, 'dashboard/edit_package.html',{'data':package})
        if request.method == "POST":
            pkg = get_object_or_404(Package,pk=request.POST['id'])
            pkg.title = request.POST.get('title',package.title)
            pkg.location = request.POST.get('location',package.location)
            pkg.seats = request.POST.get('seats',package.seats)
            pkg.image = request.FILES.get('image','')
            if request.POST['date'] == '':
                pkg.date=None
            else:
                pkg.date = request.POST['date']
            pkg.description = request.POST.get('description',package.description)
            pkg.save()

            return redirect('org-packages',org=request.user.pk)
    return redirect('/')

@login_required
def org_package_delete(request, package):
    pkg = get_object_or_404(Package,pk=package)
    if request.user.pk == pkg.org_id:
        pkg.delete()
        return redirect('org-packages',org=request.user.pk)
    return redirect('/')



"""
Booking section
"""
@login_required
def book_package(request, package_id):
    if request.user.type == 'USER':
        package = get_object_or_404(Package,pk=package_id)
        Book.objects.create(user=request.user, package=package)
        return redirect('package-details',id=package_id)
    return redirect('/')

@login_required
def cancel_package(request, package_id):
    if request.user.type == 'USER':
        package = get_object_or_404(Package,pk=package_id)
        Book.objects.filter(user=request.user, package=package).delete()
        return redirect('package-details',id=package_id)
    return redirect('/')

@login_required
def booked_packages(request):
    packages = Book.objects.filter(user=request.user)
    return render(request,'dashboard/booked_packages.html',{'packages':packages})
