from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import Meetup, Member


class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = '__all__'


class MeetingForm(forms.ModelForm):
    class Meta:
        model = Meetup
        fields = '__all__'
