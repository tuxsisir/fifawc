from django.db import models
from django.db.models import Sum, F
from django_extensions.db.models import TimeStampedModel

from fifawc.users.models import User
from match.models import Country, Match


class Prediction(TimeStampedModel):
    user = models.ForeignKey(User, related_name="my_predictions", on_delete=models.CASCADE)
    winning_team = models.ForeignKey(Country, related_name="win_predicted", on_delete=models.CASCADE, null=True, blank=True)
    match = models.ForeignKey(Match, related_name="predictions", on_delete=models.CASCADE)
    home_goal = models.PositiveSmallIntegerField(default=0)
    away_goal = models.PositiveSmallIntegerField(default=0)
    red_card = models.BooleanField(default=False)
    yellow_card = models.BooleanField(default=False)
    penalty_goal = models.BooleanField(default=False)
    most_foul = models.ForeignKey(Country, related_name="most_foul_predicted", on_delete=models.CASCADE, null=True)
    bonus_answer = models.CharField(max_length=255)

    def __str__(self):
        return "{} predicted {} as a winning team.".format(self.user.name, self.winning_team)


class MatchOutcome(TimeStampedModel):
    match = models.OneToOneField(Match, related_name="outcome", on_delete=models.CASCADE)
    winning_team = models.ForeignKey(Country, related_name="match_won", on_delete=models.CASCADE, null=True, blank=True)
    home_goal = models.PositiveSmallIntegerField(default=0)
    away_goal = models.PositiveSmallIntegerField(default=0)
    red_card = models.BooleanField(default=False)
    yellow_card = models.BooleanField(default=False)
    penalty_goal = models.BooleanField(default=False)
    most_foul = models.ForeignKey(Country, related_name="most_foul_matches", on_delete=models.CASCADE, null=True)
    bonus_answer = models.CharField(max_length=255)

    def __str__(self):
        return "{} wins the match of {}.".format(self.winning_team, self.match)


class PointScored(models.Model):
    user = models.ForeignKey(User, related_name="my_points", on_delete=models.CASCADE)
    match = models.ForeignKey(Match, related_name="points_for_match", on_delete=models.CASCADE, null=True)
    last_increased_by = models.PositiveSmallIntegerField(default=0)
    points_scored = models.PositiveSmallIntegerField(default=0)

    nearest = models.BooleanField(default=False)
    matching = models.BooleanField(default=False)
    adjusted_score = models.BooleanField(default=False)

    def __str__(self):
        return "{} scored {} points on {}".format(self.user, self.points_scored, self.match)

    @classmethod
    def total_points(cls, user):
        return cls.objects.filter(user=user).select_related('user', 'match').aggregate(Sum(F('points_scored')))
