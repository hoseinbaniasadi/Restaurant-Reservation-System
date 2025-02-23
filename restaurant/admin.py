from django.contrib import admin

from .models import Table, Reservation, Review

@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ['name', 'capacity', 'is_available']
    list_filter = ['is_available']
    search_fields = ['name']



@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['user', 'table', 'date', 'time', 'number_of_pepole', 'is_confirmed']
    list_filter = ['is_confirmed', 'date']
    search_fields = ['user__username', 'table__name']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'table', 'comment', 'rating', 'datetime_created', 'active']
    search_fields = ['user__username', 'table__name']
    list_filter = ['active', ]