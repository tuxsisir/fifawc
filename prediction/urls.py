from django.urls import path

from . import views

app_name = 'prediction'

urlpatterns = [
    path('create/', views.CreatePrediction.as_view(), name="create"),
    # path('update/<int:pk>/', views.UpdatePrediction.as_view(), name="update"),

    path('match-outcome/create/<int:match_id>/', views.CreateMatchOutcome.as_view(), name="match-outcome-create"),
    path('match-outcome/update/<int:pk>/', views.UpdateMatchOutcome.as_view(), name="match-outcome-update"),

    path('user-points/', views.UserPoints.as_view(), name="user-points"),

    path('prediction-point/overview/<int:user_id>/', views.PredictionPointHistory.as_view(), name="history")
]
