from django.contrib import admin

from codepot.models import (
    PromoCode,
    PromoCodeClassification,
    Purchase,
    Ticket,
    PriceTier,
    Product,
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


@admin.register(PriceTier)
class PriceAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'date_from',
        'date_to',
        'tickets_purchased',
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'price_tier',
        'price_net',
        'price_vat',
    )
