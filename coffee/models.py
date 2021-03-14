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

    def done_times(self, in_int):
        qs = super(MeetupManager, self).filter(active=True).filter(meetings=in_int)
        return qs


class RecordManager(models.Manager):
    def all(self):
        qs = super(RecordManager, self).all()
        return qs

    def last(self):
        qs = super(RecordManager, self).all().order_by('pk').last()
        return qs


class Member(models.Model):
    full_name = models.CharField(max_length=300, blank=False, null=False, unique=True)
    active = models.BooleanField(null=False, default=True)
    email = models.EmailField(blank=True, null=True)
    objects = MemberManager()

    @staticmethod
    def meetings_to_set():
        # based on the number of active Members
        active_members = Member.objects.active().count()
        meets = active_members // 2
        return meets


class Meetup(models.Model):
    combination = models.CharField(max_length=10, blank=False, null=False, unique=True)
    meetings = models.PositiveSmallIntegerField(default=0)
    active = models.BooleanField(null=False, default=True)
    objects = MeetupManager()

    def increment(self):
        self.meetings += 1
        self.save()
        return 0

    def members(self):
        m = []
        pair = self.combination.split('|')
        m.append(pair[0])
        m.append(pair[1])
        return m

    @staticmethod
    def highest_mtgs():
        hm = Meetup.objects.active().order_by(models.F('meetings')).last()
        return hm.meetings

    @staticmethod
    def next_highest_mtgs():
        nhm = Meetup.objects.active().order_by(models.F('meetings')).first()
        return nhm.meetings


class MeetRecord(models.Model):
    recorded = models.DateField(auto_now_add=True)
    detail = models.CharField(max_length=300, blank=False, null=False)
    # objects = RecordManager()