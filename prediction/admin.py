from django.contrib import admin

from prediction.models import MatchOutcome, Prediction, PointScored

admin.site.register([Prediction, MatchOutcome, PointScored])
