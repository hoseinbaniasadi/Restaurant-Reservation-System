from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.contrib import messages

from .models import Table
from .forms import ReservationForm

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
    return render(request, 'restaurant/reserve_table.html', context={'form': form, 'table': table})
