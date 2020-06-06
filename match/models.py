import os
import uuid

from django.db import models

from .constants import GROUP_STAGE, MATCH_TYPES, GROUPS, GROUP_A, ROUND_OF_SIXTEEN, QUARTER_FINALS, SEMI_FINALS, \
    THIRD_PLACE, FINALS


def get_flag_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "{}.{}".format(uuid.uuid4().hex, ext)[:99]
    return os.path.join('uploads/country/', filename)


class Country(models.Model):
    name = models.CharField(max_length=255, blank=False)
    group = models.PositiveSmallIntegerField(choices=GROUPS, default=GROUP_A)
    flag_image = models.ImageField(upload_to=get_flag_upload_path)

    def __str__(self):
        return self.name


class Match(models.Model):
    home = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, related_name='home_matches')
    away = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, related_name='away_matches')
    start_time = models.DateTimeField()
    match_type = models.PositiveSmallIntegerField(choices=MATCH_TYPES, default=GROUP_STAGE)
    bonus_question = models.TextField()

    def __str__(self):
        return "{} vs. {}".format(self.home, self.away)


    @property
    def possible_points(self):
        total_points_map = {
            GROUP_STAGE: 10,
            THIRD_PLACE: 50,
            ROUND_OF_SIXTEEN: 20,
            QUARTER_FINALS: 30,
            SEMI_FINALS: 40,
            FINALS: 60
        }
        return total_points_map.get(self.match_type, 10)
