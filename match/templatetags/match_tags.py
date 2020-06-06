from django import template

from prediction.models import Prediction, MatchOutcome, PointScored
from ..constants import GROUPS
register = template.Library()


@register.simple_tag()
def get_group_name(group_id):
    groups = dict(GROUPS)
    return groups.get(group_id, None)


@register.simple_tag()
def win_predicted_count(country):
    return Prediction.objects.select_related('winning_team').filter(winning_team__name__iexact=country).count()


@register.simple_tag()
def get_match_outcome(match):
    try:
        obj = MatchOutcome.objects.select_related('winning_team', 'match', 'match__away', 'match__home').get(match=match)
    except MatchOutcome.DoesNotExist:
        obj = None
    return obj


@register.simple_tag()
def get_match_point_of_user(match, user):
    try:
        obj = PointScored.objects.get(match=match, user=user)
    except PointScored.DoesNotExist:
        obj = None
    return obj
