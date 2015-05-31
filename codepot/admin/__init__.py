from django.contrib import admin

from codepot.models import (
    PromoCode,
    PromoCodeClassification,
    Purchase,
    Ticket,
    Price,
)

@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    pass


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    pass


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    pass


@admin.register(PromoCodeClassification)
class PromoCodeClassificationAdmin(admin.ModelAdmin):
    pass


@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'date_from',
        'date_to',
        'first_day_net',
        'first_day_total',
        'second_day_net',
        'second_day_total',
        'both_days_net',
        'both_days_total',
        'tickets_purchased',
    )
