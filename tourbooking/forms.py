from django import forms
from .models import Package , Image , Itinerary
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class FeedbackForm(forms.Form):
    feedback = forms.CharField(label='Your Feedback', max_length=1000)


class CreatePackageForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = ['user','title','description','duration','price','date','itinerary','image']
        title = forms.CharField()
        description = forms.CharField()
        duration = forms.CharField()
        price = forms.CharField()
        date = forms.DateInput()

    itinerary = forms.ModelMultipleChoiceField(
        queryset=Itinerary.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
    image = forms.ModelMultipleChoiceField(
        queryset=Image.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username","email","password1","password2"]