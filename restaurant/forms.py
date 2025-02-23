from django import forms
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
import datetime

from .models import Reservation, Table, Review

class ReservationForm(forms.ModelForm):
    table_id = forms.IntegerField(widget=forms.HiddenInput)

    class Meta:
        model = Reservation
        fields = ['table_id', 'date', 'time', 'number_of_pepole']

    # def __init__(self, *args, **kwargs):
    #     self.table = kwargs.pop('table', None)
    #     super().__init__(*args, **kwargs)

    def clean(self):
         cleaned_data = super().clean()
         table_id = cleaned_data.get('table_id')
         date = cleaned_data.get('date')
         time = cleaned_data.get('time')
         number_of_pepole = cleaned_data.get('number_of_pepole')

         if not table_id:
            raise ValidationError('The Table id is not specified')

         if Reservation.objects.filter(table=table_id, date=date, time=time).exists():
            raise ValidationError('This table is already reserved at the selected time.')

         if table_id:
            table = get_object_or_404(Table, pk=table_id)
            if number_of_pepole > table.capacity:
                raise ValidationError(f"This table can obly accommodate {table.capacity} pepole")
         
         
         if date < datetime.date.today():
             raise ValidationError('You cannot reserve a table for a past date.')
         
         
         return cleaned_data
             

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']