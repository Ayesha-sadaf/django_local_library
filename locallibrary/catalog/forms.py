import datetime
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class RenewBookForm(forms.Form):
    renewal_date=forms.DateField(help_text='Enter a date between now and 4 weeks(default)')
    def clean_renewal_date(self):
        date=self.cleaned_data['renewal_date']
        #check of date is not in the past
        if date < datetime.date.today():
            raise ValidationError(_('Invalid date :%(value)s - date in past'),code='invalid',params={'value':date})
        #check if date is in allowed range 
        if date > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date :%(value)s - date more than 4 weeks ahead'),code='invalid',params={'value':date})
        
        return date