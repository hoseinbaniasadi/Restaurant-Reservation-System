from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.contrib import messages
from django.urls import reverse

from .models import Review, Table
from .forms import ReservationForm, ReviewForm

# class ReserveTable(generic.ListView):
#     model = Table
#     template_name = 'restaurant/reserve_table.html'
#     context_object_name = 'tables'

class TableList(generic.ListView):
    queryset = Table.objects.filter(is_available=True)
    template_name = 'restaurant/table_list.html'
    context_object_name = 'tables'


def reserve_table(request, pk):
    table = get_object_or_404(Table, pk=pk)
    table_review = table.review.all()
    review_form = ReviewForm()
    
    if request.method == 'POST':
        form = ReservationForm(request.POST, initial={'table_id': pk})
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.table = table
            reservation.is_confirmed = True
            reservation.save()
            messages.success(request, 'Your reservation has been successfully submited')
            return redirect('home')
    else:   
        form = ReservationForm(initial={'table_id': pk})
        review_form = ReviewForm()
    return render(request, 'restaurant/reserve_table.html', context={
        'form': form,
        'table': table,
        'table_review': table_review, 
        'review_form': review_form,
        })


def table_review(request, pk):
    table = get_object_or_404(Table, pk=pk)
    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            form = review_form.save(commit=False)
            form.table = table
            form.user = request.user
            form.save()
            return redirect(reverse('reserve_table', args=[pk]))




