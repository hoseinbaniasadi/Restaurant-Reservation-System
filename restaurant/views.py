import requests
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponse

from .models import Review, Table, Reservation, Payment
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
            reservation.save()
            return redirect('create_payment', reservation_id=reservation.id)
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



def create_payment(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    toman_total_price = reservation.table.price * reservation.number_of_pepole
    rial_total_price = toman_total_price * 10

    zarinpal_request_url = 'https://sandbox.zarinpal.com/pg/v4/payment/request.json'

    requset_header = {
        'accept': 'application/json',
        'content-type': 'application/json',
    }

    request_data = {
        'merchant_id': 'abcABCabcABCabcABCabcABCabcABCabcABC',
        'amount': rial_total_price,
        'description': f"Reservation for {reservation.table.name}",
        'callback_url': request.build_absolute_uri(reverse('verify_payment')),
    }

    res = requests.post(url=zarinpal_request_url, data=json.dumps(request_data), headers=requset_header)

    data = res.json()['data']
    authority = data['authority']

    Payment.objects.create(reservation=reservation, amount=toman_total_price, zarinpal_authority=authority)  

    if 'errors' not in data or len(data['errors']) == 0:
        return redirect('https://sandbox.zarinpal.com/pg/StartPay/{authority}'.format(authority=authority))
    else:
        return HttpResponse('Error from zarinpal')
    

def verify_payment(request):
    authority = request.GET.get('Authority')
    status = request.GET.get('Status')

    payment = get_object_or_404(Payment, zarinpal_authority=authority)
    toman_total_price = payment.amount
    rial_total_price = toman_total_price * 10

    if status == 'OK':

        request_header = {
        'accept': 'application/json',
        'content-type': 'application/json',
        }

        request_data = {
            'merchant_id': 'abcABCabcABCabcABCabcABCabcABCabcABC',
            'amount': rial_total_price,
            'authority': authority,
        }

        res = requests.post(
            url='https://sandbox.zarinpal.com/pg/v4/payment/verify.json',
            data=json.dumps(request_data),
            headers=request_header,
            )

        if 'errors' not in res.json()['data']:
            data = res.json()['data']
            payment_code = data['code']

            if payment_code == 100:
                payment.status = 'completed'
                payment.zarinpal_ref_id = data['ref_id']
                payment.zarinpal_data = data
                payment.save()
                payment.reservation.is_confirmed = True
                payment.reservation.save()
                
                return HttpResponse('پرداخت شما با موفقیت انجام شد')
            
            elif payment_code == 101:
                return HttpResponse('پرداخت شما با موفقیت انجام شد، البته این تراکنش قبلا ثبت شده است')
            
        else:
            payment.status = 'failed'
            payment.save()
            error_code = res.json['errors']['code']
            error_messege = res.json['errors']['message']
            return HttpResponse(f'{error_messege} {error_code}تراکنش ناموفق بود ')
        
    
    else:
        return HttpResponse('تراکنش ناموفق بود')




