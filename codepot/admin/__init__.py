from django.contrib import admin

from codepot.models import (
    PromoCode,
    PromoCodeClassification,
    Purchase,
    PurchaseInvoice,
    Ticket,
    PriceTier,
    Product,
    AppSettings,
)

@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = (
        'code',
        'usage_limit',
        'discount',
        'active',
        'classification',
        'sent',
    )


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'promo_code',
        'payment_type',
        'payment_status',
        'product',
        'confirmation_sent',
        'fake',
    )

@admin.register(PurchaseInvoice)
class PurchaseInvoiceAdmin(admin.ModelAdmin):
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


@admin.register(AppSettings)
class AppSettingsAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'value',
    )
