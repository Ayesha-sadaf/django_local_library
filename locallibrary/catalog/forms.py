import datetime
from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import BookInstance

class DueDateValidationMixin:
    def validate_due_date(self,date):
         #check of date is not in the past
        if date < datetime.date.today():
            raise ValidationError(_('Invalid date :%(value)s - date in past'),code='invalid',params={'value':date})
        #check if date is in allowed range 
        if date > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date :%(value)s - date more than 4 weeks ahead'),code='invalid',params={'value':date})
        return date



class RenewBookForm(forms.Form,DueDateValidationMixin):
    renewal_date=forms.DateField(help_text='Enter a date between now and 4 weeks(default)')
    def clean_renewal_date(self):
        return self.validate_due_date(self.cleaned_data['renewal_date'])
    

class BorrowBookForm(ModelForm,DueDateValidationMixin):
    
    def clean_due_back(self):
        return self.validate_due_date(self.cleaned_data['due_back'])
    
    class Meta:
        model=BookInstance
        fields=['borrower','due_back']
        help_texts = {'due_back': _('Enter a date between now and 4 weeks (default 3).')}