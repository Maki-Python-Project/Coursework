from django import forms
from django.forms import fields

from movies import views

from .models import Reviews, Rating, RatingStar, Movie

class ReviewForm(forms.ModelForm):
    
    class Meta:
        model = Reviews
        fields = ("name", "email", "text")

class RatingForm(forms.ModelForm):

    star = forms.ModelChoiceField(
        queryset = RatingStar.objects.all(), widget = forms.RadioSelect(), empty_label = None
    )

    class Meta:
        model = Rating
        fields = ('star',)

class PopularForm(forms.ModelForm):

  
    class Meta:
        model = Movie
        fields = ('views',)