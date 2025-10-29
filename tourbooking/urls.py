from django.contrib import admin
from django.urls import path,include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth.views import LoginView,LogoutView,PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from .import views

app_name='tourbooking'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('',views.home,name='home'),
    path('package/<int:id>/',views.package,name='package'),
    path('about',views.about,name='about'),
    path('trip',views.trip,name='trip'),
    path('contact',views.contact,name='contact'),
    path('signup',views.SignUpView.as_view(),name='signup'),
    path('accounts/login',views.login,name='accounts/login'),
    path('package/',views.PackageView.as_view(),name='package'),
    path('gallery/',views.gallery,name='gallery'),
    path("book/<int:id>",views.book,name="book"),
    path("rating/<int:id>",views.rating,name="rating"),
    path("delete/<int:id>",views.delete,name="delete"), 
]
urlpatterns += staticfiles_urlpatterns()