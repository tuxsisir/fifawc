from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.utils import timezone

from django.views.generic.edit import ProcessFormView, CreateView, UpdateView

from fifawc.users.models import User
from match.models import Match, Country
from prediction.forms import MatchOutcomeForm
from prediction.models import Prediction, MatchOutcome


class CreatePrediction(LoginRequiredMixin, ProcessFormView):

    def post(self, *args, **kwargs):
        form_data = self.request.POST
        match_obj = get_object_or_404(Match, id=form_data.get('match'))
        if form_data.get('most_foul', 0) not in [str(match_obj.away_id), str(match_obj.home_id)]:
            messages.error(self.request, "You are trying to add data for different team which do not belong to this current match. Your action has been reported.")
            return redirect(reverse_lazy('match:match-detail', args=[form_data.get('match')]))
        if form_data.get('winning_team', None):
            if form_data.get('winning_team', 0) not in [str(match_obj.away_id), str(match_obj.home_id)]:
                messages.error(self.request, "You are trying to add data for different team which do not belong to this current match. Your action has been reported.")
                return redirect(reverse_lazy('match:match-detail', args=[form_data.get('match')]))
            winning_team = get_object_or_404(Country, id=form_data.get('winning_team'))
            if winning_team == match_obj.home and form_data.get('home_goal', 0) <= form_data.get('away_goal', 0):
                messages.error(self.request, "Select proper score lines for your winning team.")
                return redirect(reverse_lazy('match:match-detail', args=[form_data.get('match')]))
            if winning_team == match_obj.away and form_data.get('away_goal', 0) <= form_data.get('home_goal', 0):
                messages.error(self.request, "Select proper score lines for your winning team.")
                return redirect(reverse_lazy('match:match-detail', args=[form_data.get('match')]))
        else:
            pass
        if match_obj.start_time < timezone.now():
            messages.error(self.request, "Looks like, you're doing something wrong, this incident has been reported - prediction time is over.")
            return redirect(reverse_lazy('match:match-detail', args=[form_data.get('match')]))
        red_card = True if form_data.get('red_card', None) else False
        yellow_card = True if form_data.get('yellow_card', None) else False
        penalty_goal = True if form_data.get('penalty_goal', None) else False
        if form_data.get('winning_team') == "" and form_data.get('home_goal', 0) != form_data.get('away_goal', 0):
            messages.error(self.request, "Please select draw values!")
            return redirect(reverse_lazy('match:match-detail', args=[form_data.get('match')]))
        Prediction.objects.create(
            user=self.request.user,
            match_id=form_data.get('match'),
            winning_team_id=form_data.get('winning_team'),
            home_goal=form_data.get('home_goal', 0),
            away_goal=form_data.get('away_goal', 0),
            red_card=red_card,
            yellow_card=yellow_card,
            penalty_goal=penalty_goal,
            most_foul_id=form_data.get('most_foul'),
            bonus_answer=form_data.get('bonus_answer')
        )
        messages.success(self.request, "Successfully predicted the match!")
        return redirect(reverse_lazy('match:match-detail', args=[form_data.get('match')]))

    def get(self, *args, **kwargs):
        return redirect(reverse_lazy('home'))


class UpdatePrediction(LoginRequiredMixin, ProcessFormView):

    def post(self, *args, **kwargs):
        form_data = self.request.POST
        match_obj = get_object_or_404(Match, id=form_data.get('match'))
        if form_data.get('most_foul', 0) not in [str(match_obj.away_id), str(match_obj.home_id)]:
            messages.error(self.request, "You are trying to add data for different team which do not belong to this current match. Your action has been reported.")
            return redirect(reverse_lazy('match:match-detail', args=[form_data.get('match')]))
        if form_data.get('winning_team', None):
            if form_data.get('winning_team', 0) not in [str(match_obj.away_id), str(match_obj.home_id)]:
                messages.error(self.request, "You are trying to add data for different team which do not belong to this current match. Your action has been reported.")
                return redirect(reverse_lazy('match:match-detail', args=[form_data.get('match')]))
            winning_team = get_object_or_404(Country, id=form_data.get('winning_team'))
            if winning_team == match_obj.home and form_data.get('home_goal', 0) <= form_data.get('away_goal', 0):
                messages.error(self.request, "Select proper score lines for your winning team.")
                return redirect(reverse_lazy('match:match-detail', args=[form_data.get('match')]))
            if winning_team == match_obj.away and form_data.get('away_goal', 0) <= form_data.get('home_goal', 0):
                messages.error(self.request, "Select proper score lines for your winning team.")
                return redirect(reverse_lazy('match:match-detail', args=[form_data.get('match')]))
        else:
            pass
        if match_obj.start_time < timezone.now():
            messages.error(self.request, "Looks like, you're doing something wrong, this incident has been reported - prediction time is over.")
            return redirect(reverse_lazy('match:match-detail', args=[form_data.get('match')]))
        red_card = True if form_data.get('red_card', None) else False
        yellow_card = True if form_data.get('yellow_card', None) else False
        penalty_goal = True if form_data.get('penalty_goal', None) else False
        if form_data.get('winning_team') == "" and form_data.get('home_goal', 0) != form_data.get('away_goal', 0):
            messages.error(self.request, "Please select draw values!")
            return redirect(reverse_lazy('match:match-detail', args=[form_data.get('match')]))
        prediction = get_object_or_404(Prediction, id=self.kwargs['pk'])
        prediction.winning_team_id = form_data.get('winning_team')
        prediction.home_goal = form_data.get('home_goal', 0)
        prediction.away_goal = form_data.get('away_goal', 0)
        prediction.red_card = red_card
        prediction.yellow_card = yellow_card
        prediction.penalty_goal = penalty_goal
        prediction.most_foul_id = form_data.get('most_foul')
        prediction.bonus_answer = form_data.get('bonus_answer')
        prediction.save()
        messages.success(self.request, "Successfully updated your prediction of the match!")
        return redirect(reverse_lazy('match:match-detail', args=[form_data.get('match')]))

    def get(self, *args, **kwargs):
        return redirect(reverse_lazy('home'))


class CreateMatchOutcome(LoginRequiredMixin, CreateView):
    model = MatchOutcome
    template_name = 'prediction/match_outcome_form.html'
    form_class = MatchOutcomeForm

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_superuser:
            raise PermissionError
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.match = self.get_match()
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, "Successfully created match outcome and updated points of the user.")
        return reverse_lazy('prediction:user-points')

    def get_match(self):
        match = Match.objects.get(id=self.kwargs['match_id'])
        return match

    def get_form_kwargs(self):
        kw = super().get_form_kwargs()
        kw['match'] = self.get_match()
        return kw

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['match'] = self.get_match()
        return ctx


class UpdateMatchOutcome(LoginRequiredMixin, UpdateView):
    model = MatchOutcome
    template_name = 'prediction/match_outcome_form.html'
    form_class = MatchOutcomeForm

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_superuser:
            raise PermissionError
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        return super().form_valid(form)

    def get_form_kwargs(self):
        kw = super().get_form_kwargs()
        kw['match'] = self.object.match
        return kw

    def get_success_url(self):
        messages.success(self.request, "Successfully updated match outcome and updated points of the user.")
        return reverse_lazy('prediction:user-points')


class UserPoints(LoginRequiredMixin, ListView):
    model = User
    template_name = 'prediction/user_points.html'

    def get_queryset(self):
        qs = sorted(User.objects.all(),
                    key=lambda user: user.total_points['points_scored__sum'] if user.total_points['points_scored__sum'] else 0,
                    reverse=True)
        return qs


class PredictionPointHistory(LoginRequiredMixin, ListView):
    model = Prediction
    template_name = 'prediction/history.html'

    def get_queryset(self):
        qs = Prediction.objects.filter(user_id=self.kwargs['user_id']).select_related(
            'user', 'match', 'winning_team', 'match__home', 'match__away', 'most_foul', 'match__outcome',
            'match__outcome__winning_team', 'match__outcome__most_foul').order_by('-match__start_time')
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['user'] = get_object_or_404(User, id=self.kwargs['user_id'])
        return ctx
