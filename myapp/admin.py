from django.contrib import admin
from .models import Publisher, Book, Member, Order, Review


# Register your models here.
#admin.site.register(Publisher)
#admin.site.register(Book)
#admin.site.register(Member)
#admin.site.register(Order)
admin.site.register(Review)

def make_available(modeladmin, request, queryset ):

    for a in queryset:
       a.price += 10
       a.save()
    return
make_available.short_description = 'Update this fields'

class BookAdmin(admin.ModelAdmin):
    fields = [('title', 'category', 'publisher'), ('num_pages', 'price', 'num_reviews')]
    list_display = ('title', 'category', 'price')
    actions = [make_available]


admin.site.register(Book,BookAdmin)

class OrderAdmin(admin.ModelAdmin):
    fields = [('books'), ('member', 'order_type', 'order_date')]
    list_display = ('id','member','order_type','order_date','total_items')

admin.site.register(Order,OrderAdmin)

class PublisherAdmin(admin.ModelAdmin):
    fields = [('name','website','city','country')]
    list_display = ('name', 'website', 'city')
admin.site.register(Publisher,PublisherAdmin)

class MemberAdmin(admin.ModelAdmin):
    fields = ['first_name','last_name', 'status']
    list_display = ('first_name','last_name', 'status', 'books')

    def books(self,obj):
        return "\n".join([b.title for b in obj.borrowed_books.all()])

admin.site.register(Member, MemberAdmin)