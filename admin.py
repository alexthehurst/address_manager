from django.contrib import admin

# Register your models here.
from .models import Address

class AddressAdmin(admin.ModelAdmin):
	fieldsets = [
		(None,	{'fields': ['user_input']}),
	]
	list_display = ('user_input', 'creation_time')
	list_filter = ('user_input',)
	search_fields = ('user_input',)

admin.site.register(Address, AddressAdmin)
