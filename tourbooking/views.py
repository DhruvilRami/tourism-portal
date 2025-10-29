from django.shortcuts import render,redirect,resolve_url
from django.http import HttpResponse,Http404,HttpResponseRedirect
from urllib import response
from django.urls import reverse,reverse_lazy
from django.views import generic 
from django.contrib.auth.forms import (UserCreationForm, AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm,)
from .models import  Registration, Feedback, Review, Image, Itinerary,Package,Contact
from .forms import FeedbackForm , CreatePackageForm , CreateUserForm
from django.contrib import messages
from datetime import date
from django.core.mail import EmailMessage,EmailMultiAlternatives
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.template.loader import render_to_string

# Create your views here. 

def home(request):
    data = Package.objects.all()
    return render(request,'tourbooking/home.html',{"data":data}) 

class PackageView(generic.ListView):
    model = Package
    template_name='tourbooking/package.html'

@login_required
def book(request, id):
    package_data = Package.objects.get(id=id)
    image_data = package_data.image.all()
    itinerary_data = package_data.itinerary.all()
    current_user = request.user
    registration_data = Registration.objects.filter(
        user=current_user, package=package_data)
    today=date.today()
    if registration_data.exists():
        message = "You already booked this trip"

    else:   
        message = ""
        registration = Registration(user=current_user, package=package_data)
        image_data = package_data.image.all()
        registration.save()
        registration_data = Registration.objects.filter(user=current_user)    
        
        template = render_to_string('tourbooking/email.html', {'name':request.user.username,'package':package_data,'image': image_data})
        email = EmailMultiAlternatives(
            'Tour Booking Information',
            template,   
            'tourmania01@gmail.com',
            [request.user.email],
        )
        email.fail_silently=False
        email.content_subtype="html"
       # email.attach(image_data)
        
        email.send()

    return render(request, 'tourbooking/book.html', {"package_data": package_data, "registration_data": registration_data, "message": message,"today":today,"image_data": image_data})

def gallery(request):
    data = Package.objects.all()
    return render(request, 'tourbooking/package.html', {"data": data})

def package(request, id):
    form = FeedbackForm()
    package_data = Package.objects.get(id=id)
    itinerary_data = package_data.itinerary.all()
    image_data = package_data.image.all()
    review_data = Review.objects.filter(
        registration__package=Package.objects.get(id=id))
    RATING = 0
    COUNTER = 1
    for i in review_data:
        RATING += int(i.stars)
        COUNTER += 1
    RATING = RATING/COUNTER
    #RATING = RATING
    feedback_data = Feedback.objects.filter(package=id)
    return render(request, 'tourbooking/tourpackage.html', {"package_data": package_data,
                                            "itinerary_data": itinerary_data, "image_data": image_data, 'form': form,"review_data":review_data,'rating':round(RATING,2) ,'counter':COUNTER , 'feedback_data': feedback_data})

def about(request): 
    return render(request,'tourbooking/about.html')

def delete(request, id):
    template1 = render_to_string('tourbooking/email_cancel.html', {'name':request.user.username })
    email = EmailMessage(
            'Tour Cancellation',
            template1,
            'tourmania01@gmail.com',
            [request.user.email],
    )

    email.fail_silently=False
    email.send()
    registration = Registration.objects.get(id=id)
    registration.delete()
    return redirect("/")

@login_required
def trip(request):
    current_user = request.user
    registration_data = Registration.objects.filter(user=current_user)
    today = date.today()
    return render(request, 'tourbooking/trip.html', {"registration_data": registration_data, "today": today})


@login_required
def rating(request, id):
    registration = Registration.objects.get(id=id)
    print(request)
    if request.method == 'POST':
        if request.POST.get('star5') == 'on':
            review = 5
        elif request.POST.get('star4'):
            review = 4
        elif request.POST.get('star3'):
            review = 3
        elif request.POST.get('star2'):
            review = 2
        elif request.POST.get('star1'):
            review = 1
        else:
            review = 0
        review_field = request.POST.get('review')
        print(review_field)
        data = Review(registration=registration,stars=review, review=review_field)
        data.save()
        return redirect('/trip')
    return render(request, 'tourbooking/rating.html', {'package': registration.package})

def contact(request):   
    if request.method=='POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']
        print(name,email,phone,content)
        if len(name)<3 or len(email)<12 or len(phone)<10 or len(content)<10:
            messages.error(request,"Please fill the form correctly")
        else:
            contact = Contact(name=name , email=email , phone=phone , content=content)
            contact.save()
            messages.success(request,"Your message has been sent successfully")

    return render(request,'tourbooking/contact.html')

class SignUpView(generic.CreateView):
    form_class = CreateUserForm
    success_url = reverse_lazy('tourbooking:login')
    template_name = 'registration/signup.html'

def login(request):
    template2 = render_to_string('tourbooking/email_profile.html',{'name':request.user.username})
    email = EmailMessage(
            'Account Created',
            template2,
            'tourmania01@gmail.com',
            [request.user.email],
    )
    return render(request,'registration/login.html')

