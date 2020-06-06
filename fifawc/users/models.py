import os
import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from fifawc.users.constants import USER_GENDER, MALE


def get_dp_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "{}.{}".format(uuid.uuid4(), ext)[:99]
    return os.path.join('uploads/user-picture/', filename)


class User(AbstractUser):
    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    profile_picture = models.ImageField(
        upload_to=get_dp_path, null=True, blank=True, help_text="Display/Profile Picture of the User")
    gender = models.PositiveSmallIntegerField(choices=USER_GENDER, default=MALE)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})

    @property
    def total_points(self):
        from prediction.models import PointScored
        return PointScored.total_points(self)

    def get_profile_picture(self):
        if self.profile_picture:
            return self.profile_picture.url
        else:
            return "{0}images/default_pp.jpg".format(settings.STATIC_URL)
