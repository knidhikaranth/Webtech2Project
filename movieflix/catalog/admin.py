from django.contrib import admin

# Register your models here.
from .models import Ratings, Movies, Users

admin.site.register(Ratings)
#admin.site.register(Movies)
admin.site.register(Users)

@admin.register(Movies)
class MoviesAdmin(admin.ModelAdmin):
	list_display = ('title', 'id')
	search_fields = ['^title']