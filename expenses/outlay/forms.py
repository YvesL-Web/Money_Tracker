from django import forms

class FilterDate(forms.Form):
    start = forms.DateField( widget=forms.DateInput(attrs={'type':'date'}))
    end = forms.DateField( widget=forms.DateInput(attrs={'type':'date'}))