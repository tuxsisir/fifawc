from django.contrib import admin

from .models import Match, Country

admin.site.register([Country, Match])
