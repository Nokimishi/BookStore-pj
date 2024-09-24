from django.contrib import admin
from book_store3.models import *
# Register your models here.
class PorductAdmin(admin.ModelAdmin):
    list_display = ['id','name','image','category','genre','language','bookauthor','qty','price','created_at']

admin.site.register(Category)
admin.site.register(Language)
admin.site.register(Author)
admin.site.register(Product, PorductAdmin)
admin.site.register(Order)
admin.site.register(Cart)
admin.site.register(mostsell)
admin.site.register(Feedback)
admin.site.register(UserProfile)

#admin pass 1234

