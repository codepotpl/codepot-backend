from django.contrib import admin

from codepot.models import (
    PromoCode,
    PromoCodeClassification,
    Purchase,
    PurchaseInvoice,
    PriceTier,
    Product,
    AppSettings,
    Workshop,
    WorkshopTag,
    WorkshopMessage,
    WorkshopMentor,
    TimeSlotTier,
    TimeSlot,
    ResetPassword,
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


@admin.register(Workshop)
class WorkshopAdmin(admin.ModelAdmin):
  list_display = (
    'title',
    'max_attendees',
  )


class LimitedWorkshop(Workshop):
  class Meta:
    proxy = True


@admin.register(LimitedWorkshop)
class LimitedWorkshopAdmin(admin.ModelAdmin):
  list_display = (
    'title',
    'max_attendees',
  )
  exclude = ['attendees']


@admin.register(WorkshopTag)
class WorkshopTagAdmin(admin.ModelAdmin):
  list_display = (
    'name',
  )


@admin.register(WorkshopMessage)
class WorkshopMessageAdmin(admin.ModelAdmin):
  pass  # TODO workshop title / message id


@admin.register(TimeSlotTier)
class TimeSlotTierAdmin(admin.ModelAdmin):
  list_display = (
    'id',
    'day',
    'date_from',
    'date_to',
  )


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
  list_display = (
    'id',
    'room_no',
    'timeslot_tier',
    'workshop',
  )


@admin.register(AppSettings)
class AppSettingsAdmin(admin.ModelAdmin):
  list_display = (
    'name',
    'value',
  )


@admin.register(ResetPassword)
class ResetPasswordAdmin(admin.ModelAdmin):
  list_display = (
    'email',
    'token',
    'active',
  )


@admin.register(WorkshopMentor)
class WorkshopMentorAdmin(admin.ModelAdmin):
  list_display = (
    'first_name',
    'last_name',
    'tagline',
  )
