from django.urls import path
from . import views

urlpatterns = [
    path('', views.home,name="home"),
    path('add-packages/', views.add_packages,name="add-packages"),
    path('packages/', views.all_packages,name="packages"),
    path('packages/<int:id>/', views.package_details,name="package-details"),
    path('packages/org/<int:org>/', views.org_packages,name="org-packages"),
    path('packages/org/<int:package>/edit/', views.org_package_edit,name="org-package-edit"),
    path('packages/org/<int:package>/delete/', views.org_package_delete,name="org-package-delete"),



]   