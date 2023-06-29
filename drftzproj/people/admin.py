from django.contrib import admin

from people.models import Profile


@admin.register(Profile)
class CategoryAdmin(admin.ModelAdmin):

    pass

