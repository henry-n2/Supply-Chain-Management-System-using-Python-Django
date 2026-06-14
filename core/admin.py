# # core/admin.py (Final Fixed Version)
# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from .models import Block, User, SiteConfig, HomeSlider, ManufacturerProduct, DistributorStock, RetailerStock, Order , Transaction
# class CustomUserAdmin(UserAdmin):
#     list_display = ('username', 'email', 'role', 'is_active', 'is_staff')
#     list_filter = ('role', 'is_active', 'is_staff')
#     fieldsets = (
#         (None, {'fields': ('username', 'password')}),
#         ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone')}),
#         ('Permissions', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
#         ('Important dates', {'fields': ('last_login', 'date_joined')}),
#     )
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('username', 'email', 'role', 'password1', 'password2', 'is_staff', 'is_active')}
#         ),
#     )
#     search_fields = ('username', 'email', 'first_name', 'last_name')
#     ordering = ('username',)

# # DONT UNREGISTER - JUST REGISTER YOUR CUSTOM USER MODEL
# admin.site.register(User, CustomUserAdmin)

# # Register other models
# @admin.register(SiteConfig)
# class SiteConfigAdmin(admin.ModelAdmin):
#     list_display = ('site_name',)

# @admin.register(HomeSlider)
# class HomeSliderAdmin(admin.ModelAdmin):
#     list_display = ('caption', 'is_active')
#     list_filter = ('is_active',)

# @admin.register(ManufacturerProduct)
# class ManufacturerProductAdmin(admin.ModelAdmin):
#     list_display = ('name', 'manufacturer', 'base_price', 'available_quantity')
#     list_filter = ('manufacturer',)
#     search_fields = ('name',)

# @admin.register(DistributorStock)
# class DistributorStockAdmin(admin.ModelAdmin):
#     list_display = ('product', 'distributor', 'price', 'available_quantity')
#     list_filter = ('distributor',)
#     search_fields = ('product__name',)

# @admin.register(RetailerStock)
# class RetailerStockAdmin(admin.ModelAdmin):
#     list_display = ('product', 'retailer', 'price', 'available_quantity')
#     list_filter = ('retailer',)
#     search_fields = ('product__product__name',)

# @admin.register(Order)
# class OrderAdmin(admin.ModelAdmin):
#     list_display = ('customer', 'product', 'quantity', 'order_date')
#     list_filter = ('customer', 'order_date')
#     search_fields = ('customer__username', 'product__product__product__name')



# @admin.register(Transaction)
# class TransactionAdmin(admin.ModelAdmin):
#     list_display = ('transaction_id', 'product', 'customer', 'retailer', 'amount')
#     list_filter = ('customer', 'retailer')



# @admin.register(Block)
# class BlockAdmin(admin.ModelAdmin):
#     list_display = ('index', 'timestamp', 'previous_hash', 'proof', 'block_hash')
#     readonly_fields = ('block_hash',)
    
#     def block_hash(self, obj):
#         return obj.hash
#     block_hash.short_description = 'Block Hash'


# # core/admin.py (Final Fixed Version)
# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from .models import Block, User, SiteConfig, HomeSlider, ManufacturerProduct, DistributorStock, RetailerStock, Order , Transaction
# core/admin.py
import hashlib
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Block, User, SiteConfig, HomeSlider, ManufacturerProduct, DistributorStock, RetailerStock, Order, Transaction
from core import models

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'is_active', 'is_staff')
    list_filter = ('role', 'is_active', 'is_staff')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone')}),
        ('Permissions', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'role', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)

admin.site.register(User, CustomUserAdmin)

# @admin.register(Transaction)
# class TransactionAdmin(admin.ModelAdmin):
#     list_display = ('transaction_id', 'chain_type', 'product_info', 'amount_formatted', 
#                     'party_info', 'timestamp', 'block_status')
#     list_filter = ('chain_type', 'timestamp', 'retailer')
#     search_fields = ('transaction_id', 'product__product__product__name')
#     readonly_fields = ('timestamp', 'chain_type')
#     ordering = ('-timestamp',)

#     def product_info(self, obj):
#         return obj.product.product.product.name
#     product_info.short_description = 'Product'

#     def amount_formatted(self, obj):
#         return f"₹{obj.amount:,.2f}"
#     amount_formatted.short_description = 'Amount'

#     def party_info(self, obj):
#         if obj.chain_type == 'DISTRIBUTOR':
#             return f"Distributor: {obj.retailer.get_full_name()}"
#         return f"Customer: {obj.customer.get_full_name()}"
#     party_info.short_description = 'Counterparty'

#     def block_status(self, obj):
#         if obj.block_set.exists():
#             return obj.block_set.first().hash[:20] + '...'
#         return 'Pending'
#     block_status.short_description = 'Block Hash'
# def __str__(self):
#         return f"{self.chain_type} | {self.transaction_id} | {self.customer} → {self.retailer} | {self.amount}"








# @admin.register(Block)
# class BlockAdmin(admin.ModelAdmin):
#     list_display = ('index', 'timestamp', 'prev_hash_short', 'proof', 'block_hash_short', 'transaction_count')
#     list_filter = ('timestamp',)
#     search_fields = ('previous_hash', 'proof')
#     readonly_fields = ('timestamp', 'hash')
#     ordering = ('-index',)

#     def prev_hash_short(self, obj):
#         return f"{obj.previous_hash[:20]}..." if obj.previous_hash else ''
#     prev_hash_short.short_description = 'Previous Hash'

#     def block_hash_short(self, obj):
#         return f"{obj.hash[:20]}..."
#     block_hash_short.short_description = 'Block Hash'

#     def transaction_count(self, obj):
#         return obj.transactions.count()
#     transaction_count.short_description = 'Transactions'

#     def hash(self, obj):
#         return obj.hash
#     hash.short_description = 'Full Hash'




# Fixed vvvvvvvvvv
# @admin.register(Block)
# class BlockAdmin(admin.ModelAdmin):
#     list_display = ('index', 'chain_type', 'timestamp', 'prev_hash_short', 'full_block_hash', 'transaction_count')
#     list_filter = ('chain_type', 'timestamp')
#     search_fields = ('previous_hash', 'proof')
#     readonly_fields = ('timestamp', 'hash', 'chain_type')
#     ordering = ('-index',)

#     def prev_hash_short(self, obj):
#         return f"{obj.previous_hash[:20]}..." if obj.previous_hash else ''
#     prev_hash_short.short_description = 'Previous Hash'

#     def full_block_hash(self, obj):
#         return obj.hash
#     full_block_hash.short_description = 'Block Hash'

#     def transaction_count(self, obj):
#         return obj.transactions.count()
#     transaction_count.short_description = 'Transactions'

# from django.contrib import admin
# from core.models import Transaction, Block

# if admin.site.is_registered(Transaction):
#     admin.site.unregister(Transaction)

# if admin.site.is_registered(Block):
#     admin.site.unregister(Block)


from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Block, Transaction, User, SiteConfig, HomeSlider, ManufacturerProduct, DistributorStock, RetailerStock, Order

# @admin.register(Block)
# class BlockAdmin(admin.ModelAdmin):
#     list_display = (
#         'index', 'chain_type', 'timestamp', 'prev_hash_short', 'full_block_hash', 'transaction_count', 'view_transactions_link'
#     )
#     list_filter = ('chain_type', 'timestamp')
#     search_fields = ('previous_hash', 'proof')
#     readonly_fields = ('timestamp', 'hash', 'chain_type')
#     ordering = ('-index',)

#     def prev_hash_short(self, obj):
#         return f"{obj.previous_hash[:20]}..." if obj.previous_hash else ''
#     prev_hash_short.short_description = 'Previous Hash'

#     def full_block_hash(self, obj):
#         return obj.hash
#     full_block_hash.short_description = 'Block Hash'

#     def transaction_count(self, obj):
#         return obj.transactions.count()
#     transaction_count.short_description = 'Transactions'

#     def view_transactions_link(self, obj):
#         count = obj.transactions.count()
#         if count == 0:
#             return "No transactions"
#         url = (
#             reverse("admin:core_transaction_changelist")
#             + f"?block__id__exact={obj.id}"
#         )
#         return format_html('<a href="{}">View {} transaction{}</a>', url, count, '' if count == 1 else 's')
#     view_transactions_link.short_description = 'Transactions'

# # Register other models as usual
# @admin.register(Transaction)
# class TransactionAdmin(admin.ModelAdmin):
#     list_display = ('transaction_id', 'chain_type', 'product_info', 'amount_formatted',
#                     'party_info', 'timestamp', 'block_status')
#     list_filter = ('chain_type', 'timestamp', 'retailer')
#     search_fields = ('transaction_id', 'product__product__product__name')
#     readonly_fields = ('timestamp', 'chain_type')
#     ordering = ('-timestamp',)

#     def product_info(self, obj):
#         return obj.product.product.product.name
#     product_info.short_description = 'Product'

#     def amount_formatted(self, obj):
#         return f"₹{obj.amount:,.2f}"
#     amount_formatted.short_description = 'Amount'

#     def party_info(self, obj):
#         if obj.chain_type == 'DISTRIBUTOR':
#             return f"Distributor: {obj.retailer.get_full_name()}"
#         return f"Customer: {obj.customer.get_full_name()}"
#     party_info.short_description = 'Counterparty'

#     def block_status(self, obj):
#         if obj.block_set.exists():
#             return obj.block_set.first().hash
#         return 'Pending'
#     block_status.short_description = 'Block Hash'

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.urls import reverse
from django.utils.html import format_html
from .models import Block, User, SiteConfig, HomeSlider, ManufacturerProduct, DistributorStock, RetailerStock, Order, Transaction

# --- Fix User Registration Conflict ---
if admin.site.is_registered(User):
    admin.site.unregister(User)

# Register Custom User Admin
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'is_active', 'is_staff')
    list_filter = ('role', 'is_active', 'is_staff')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone')}),
        ('Permissions', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'role', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)
# --- Block Admin ---
@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    list_display = (
        'index', 'chain_type', 'timestamp', 'prev_hash_short', 
        'full_block_hash', 'transaction_count', 'view_transactions_link'
    )
    list_filter = ('chain_type', 'timestamp')
    search_fields = ('previous_hash', 'proof')
    readonly_fields = ('timestamp', 'hash', 'chain_type')
    ordering = ('-index',)

    def prev_hash_short(self, obj):
        return f"{obj.previous_hash[:20]}..." if obj.previous_hash else ''
    prev_hash_short.short_description = 'Previous Hash'

    def full_block_hash(self, obj):
        return obj.hash
    full_block_hash.short_description = 'Block Hash'

    def transaction_count(self, obj):
        return obj.transactions.count()
    transaction_count.short_description = 'Transactions'

    def view_transactions_link(self, obj):
        count = obj.transactions.count()
        if count == 0:
            return "No transactions"
        url = (
            reverse("admin:core_transaction_changelist")
            + f"?block__id__exact={obj.id}"
        )
        return format_html('View {} transaction{}', url, count, '' if count == 1 else 's')
    view_transactions_link.short_description = 'Transactions'

# --- Transaction Admin ---
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'chain_type', 'product_info', 'amount_formatted', 'party_info', 'timestamp', 'block_status')
    list_filter = ('chain_type', 'timestamp', 'retailer')
    search_fields = ('transaction_id', 'product__product__product__name')
    readonly_fields = ('timestamp', 'chain_type')
    ordering = ('-timestamp',)

    def product_info(self, obj):
        """Safe product name display with null checks"""
        try:
            if obj.chain_type == 'DISTRIBUTOR':
                return f"{obj.manu_product.name} (Manufacturer)"
            return f"{obj.product.product.product.name} (Retailer)"
        except AttributeError:
            return "N/A"
    product_info.short_description = 'Product'

    def amount_formatted(self, obj):
        return f"₹{obj.amount:,.2f}"
    amount_formatted.short_description = 'Amount'

    def party_info(self, obj):
        if obj.chain_type == 'DISTRIBUTOR':
            return f"Manufacturer: {obj.retailer.get_full_name()}" if obj.retailer else "No Manufacturer"
        return f"Retailer: {obj.retailer.get_full_name()}" if obj.retailer else "No Retailer"
    party_info.short_description = 'Counterparty'

    def block_status(self, obj):
        blocks = obj.block_set.all()
        if blocks.exists():
            return blocks.first().hash
        return 'Pending'
    block_status.short_description = 'Block Hash'

# --- Register Other Models ---
@admin.register(SiteConfig)
class SiteConfigAdmin(admin.ModelAdmin):
    list_display = ('site_name',)

@admin.register(HomeSlider)
class HomeSliderAdmin(admin.ModelAdmin):
    list_display = ('caption', 'is_active')
    list_filter = ('is_active',)

@admin.register(ManufacturerProduct)
class ManufacturerProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'manufacturer', 'base_price', 'available_quantity')
    list_filter = ('manufacturer',)
    search_fields = ('name',)

@admin.register(DistributorStock)
class DistributorStockAdmin(admin.ModelAdmin):
    list_display = ('product', 'distributor', 'price', 'available_quantity')
    list_filter = ('distributor',)
    search_fields = ('product__name',)

@admin.register(RetailerStock)
class RetailerStockAdmin(admin.ModelAdmin):
    list_display = ('product', 'retailer', 'price', 'available_quantity')
    list_filter = ('retailer',)
    search_fields = ('product__product__name',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'product', 'quantity', 'order_date')
    list_filter = ('customer', 'order_date')
    search_fields = ('customer__username', 'product__product__product__name')
