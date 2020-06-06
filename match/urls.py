from django.urls import path

from . import views

app_name = "match"

urlpatterns = [
    path('country/list/', views.CountryListView.as_view(), name="country-list"),
    path('create/', views.CreateMatch.as_view(), name="create-match"),
    path('list/', views.MatchList.as_view(), name="match-list"),

    path('update/<int:pk>/', views.UpdateMatch.as_view(), name="match-update"),
    path('detail/<int:pk>/', views.MatchDetailOverview.as_view(), name="match-detail"),
]
