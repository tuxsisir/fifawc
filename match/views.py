from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied

from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, CreateView, UpdateView, TemplateView, DetailView

from fifawc.users.models import User
from match.forms import MatchForm
from prediction.forms import PredictionForm
from prediction.models import Prediction
from .models import Country, Match


class LandingView(TemplateView):
    template_name = 'pages/home.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['users'] = User.objects.all()
        return ctx


class CountryListView(LoginRequiredMixin, ListView):
    model = Country
    template_name = 'match/country/list.html'
    queryset = Country.objects.all().order_by('group').values('name', 'flag_image', 'group')


class MatchList(LoginRequiredMixin, ListView):
    model = Match
    template_name = 'match/match/list.html'
    queryset = model.objects.select_related('home', 'away', 'outcome', 'outcome__winning_team').order_by('-start_time')


class CreateMatch(LoginRequiredMixin, CreateView):
    model = Match
    template_name = 'match/match/form.html'
    form_class = MatchForm
    success_url = reverse_lazy('match:match-list')
    success_message = "Successfully created match."

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_superuser:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        messages.success(self.request, self.success_message)
        return self.success_url


class UpdateMatch(LoginRequiredMixin, UpdateView):
    model = Match
    template_name = 'match/match/form.html'
    form_class = MatchForm
    success_url = reverse_lazy('match:match-list')
    success_message = "Successfully updated match."

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_superuser:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        messages.success(self.request, self.success_message)
        return self.success_url


class MatchDetailOverview(LoginRequiredMixin, DetailView):
    model = Match
    template_name = 'match/match/detail.html'
    queryset = model.objects.select_related('outcome', 'outcome__most_foul', 'home', 'away')

    def existing_prediction(self):
        prediction = Prediction.objects.filter(match=self.object, user=self.request.user).select_related(
            'user', 'match', 'match__home', 'match__away', 'most_foul')
        return prediction.exists(), prediction

    def prediction_deadline_exceeded(self):
        if self.object.start_time > timezone.now():
            return False
        return True

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['match_predictions'] = Prediction.objects.filter(match=self.object).select_related(
            'user', 'match', 'match__home', 'match__away', 'most_foul', 'winning_team', 'match__outcome')\
            .prefetch_related('user__my_points', 'user__my_points__match')
        predictions_exists, prediction_qs = self.existing_prediction()
        if predictions_exists:
            prediction_obj = prediction_qs.first()
            ctx['form'] = PredictionForm(initial={'prediction_id': prediction_obj.id,
                                                  'home_goal': prediction_obj.home_goal,
                                                  'away_goal': prediction_obj.away_goal,
                                                  'winning_team': prediction_obj.winning_team,
                                                  'red_card': prediction_obj.red_card,
                                                  'yellow_card': prediction_obj.yellow_card,
                                                  'penalty_goal': prediction_obj.penalty_goal,
                                                  'most_foul': prediction_obj.most_foul,
                                                  'bonus_answer': prediction_obj.bonus_answer}, match=self.object)
        else:
            ctx['form'] = PredictionForm(match=self.object)
        ctx['prediction_deadline_exceeded'] = self.prediction_deadline_exceeded()
        return ctx
