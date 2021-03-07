from django.contrib import admin

from .models import Meetup, Member


class MembersModelAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email']

    class Meta:
        model = Member


admin.site.register(Member, MembersModelAdmin)


class MeetupModelAdmin(admin.ModelAdmin):
    list_display = ['combination', 'meetings']

    class Meta:
        model = Meetup


admin.site.register(Meetup, MeetupModelAdmin)