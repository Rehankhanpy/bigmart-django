from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import *

# Register your models here.
class AccountAdmin(UserAdmin):
       list_display = ['email', 'firstname', 'lastname', 'username', 'last_login', 'date_joined', 'is_active']
       list_display_links = ('email', 'firstname', 'lastname')
       readonly_fields = ('last_login', 'date_joined')
       ordering = ('-date_joined',)
       
       filter_horizontal = ()
       list_filter = ()
       fieldsets = ()

class CategoryAdmin(admin.ModelAdmin):
       prepopulated_fields = {'slug':('name',)}
       list_display = ('name','slug')


class ProductAdmin(admin.ModelAdmin):
       list_display = ('name','price','stock','category','modified_date','is_available')
       prepopulated_fields = {'slug':('name',)}




admin.site.register(category, CategoryAdmin)
admin.site.register(Accounts, AccountAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(banner)
