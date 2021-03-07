from django.db import models


class MemberManager(models.Manager):
    def all(self):
        qs = super(MemberManager, self).all()
        return qs

    def active(self):
        qs = super(MemberManager, self).filter(active=True)
        return qs

    def deactive(self):
        qs = super(MemberManager, self).filter(active=False)
        return qs


class MeetupManager(models.Manager):
    def all(self):
        qs = super(MeetupManager, self).all()
        return qs

    def active(self):
        qs = super(MeetupManager, self).filter(active=True)
        return qs

    def deactive(self):
        qs = super(MeetupManager, self).filter(active=False)
        return qs


class Member(models.Model):
    full_name = models.CharField(max_length=300, blank=False, null=False, unique=True)
    active = models.BooleanField(null=False, default=True)
    email = models.EmailField()
    objects = MemberManager()


class Meetup(models.Model):
    combination = models.CharField(max_length=10, blank=False, null=False, unique=True)
    meetings = models.PositiveSmallIntegerField(default=0)
    active = models.BooleanField(null=False, default=True)
    objects = MeetupManager()


