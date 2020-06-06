from django import forms
from django.db.models import Q

from match.constants import GROUP_STAGE, ROUND_OF_SIXTEEN, QUARTER_FINALS, SEMI_FINALS, FINALS, THIRD_PLACE

from match.models import Country
from .models import Prediction, MatchOutcome, PointScored


class PredictionForm(forms.ModelForm):
    class Meta:
        model = Prediction
        exclude = ['id', 'user', 'match']
        labels = {'most_foul': "Team with Most Foul Commits"}

    def __init__(self, *args, **kwargs):
        match = kwargs.pop('match')
        super().__init__(*args, **kwargs)
        self.fields['winning_team'].queryset = Country.objects.filter(
            Q(name=match.home.name) | Q(name=match.away.name))
        self.fields['most_foul'].queryset = Country.objects.filter(
            Q(name=match.home.name) | Q(name=match.away.name))


class MatchOutcomeForm(forms.ModelForm):
    class Meta:
        model = MatchOutcome
        exclude = ['id', 'match']

    def __init__(self, *args, **kwargs):
        self.match = kwargs.pop('match')
        super().__init__(*args, **kwargs)
        self.fields['winning_team'].queryset = Country.objects.filter(
            Q(name=self.match.home.name) | Q(name=self.match.away.name))
        self.fields['most_foul'].queryset = Country.objects.filter(
            Q(name=self.match.home.name) | Q(name=self.match.away.name))
        self.fields['most_foul'].required = False

    def clean(self):
        cd = self.cleaned_data
        if not cd.get('winning_team') and cd.get('home_goal') != cd.get('away_goal'):
            raise forms.ValidationError("Please select draw values.")
        return cd

    @staticmethod
    def has_number(bonus_answer):
        return any(char.isdigit() for char in bonus_answer)

    @staticmethod
    def extract_number(bonus_answer):
        num_list = [x for x in bonus_answer if x.isdigit()]
        try:
            return int("".join(num_list))
        except ValueError:
            return

    @staticmethod
    def upper_nearest_answer(actual_ans, nearest_, user_answers):
        if actual_ans in user_answers:
            return
        nearest_diff = actual_ans - nearest_
        upper_nearest = actual_ans + nearest_diff
        return upper_nearest

    @staticmethod
    def get_score_by_match(match_type):
        score_map = {
            GROUP_STAGE: 3,
            ROUND_OF_SIXTEEN: 13,
            QUARTER_FINALS: 23,
            SEMI_FINALS: 33,
            THIRD_PLACE: 43,
            FINALS: 53
        }
        return score_map.get(match_type, 3)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        nearest_answer = None
        upper_nearest_answer = None
        lock_nearest_point = False
        predictions = Prediction.objects.filter(match=self.match).select_related(
            'user', 'match', 'winning_team', 'most_foul')
        bonus_answers = predictions.values_list('bonus_answer', flat=True)
        bonus_score_by_match = self.get_score_by_match(self.instance.match.match_type)
        # print(bonus_score_by_match)

        #  nearest answer applicable in numbers only but not in the string.
        if self.has_number(self.instance.bonus_answer):
            answers = list(filter(lambda x: x is not None, [self.extract_number(x) for x in bonus_answers]))
            if answers:
                nearest_answer = min(sorted(answers), key=lambda x: abs(x - self.extract_number(self.instance.bonus_answer)))
                actual_answer = self.extract_number(self.instance.bonus_answer)
                upper_nearest_answer = self.upper_nearest_answer(actual_answer, nearest_answer, answers)
                # print("nearest answer --> ", nearest_answer)
                # print("upper nearest answer --> ", upper_nearest_answer)

        for prediction in predictions:
            point_count = 0
            obj, created = PointScored.objects.get_or_create(user=prediction.user, match=prediction.match)
            if prediction.winning_team == self.instance.winning_team:
                point_count += 1
            if prediction.home_goal == self.instance.home_goal:
                point_count += 1
            if prediction.away_goal == self.instance.away_goal:
                point_count += 1
            if prediction.red_card == self.instance.red_card:
                point_count += 1
            if prediction.yellow_card == self.instance.yellow_card:
                point_count += 1
            if prediction.penalty_goal == self.instance.penalty_goal:
                point_count += 1
            if prediction.most_foul == self.instance.most_foul:
                point_count += 1
            if self.has_number(prediction.bonus_answer) and self.has_number(self.instance.bonus_answer):
                # print("outside no where...", prediction.user)
                obj.nearest = False
                obj.matching = False
                if self.extract_number(prediction.bonus_answer) == self.extract_number(self.instance.bonus_answer):
                    lock_nearest_point = True
                    # print("extract number and check match", prediction.user)
                    point_count += bonus_score_by_match
                    obj.matching = True
            elif prediction.bonus_answer.lower() == self.instance.bonus_answer.lower():
                # for the case of string comparison
                # print("string player comparison exact that's it ", prediction.user)
                obj.matching = True
                point_count += bonus_score_by_match
            else:
                # print("No match at all")
                obj.matching = False
                obj.nearest = False
            if not lock_nearest_point and nearest_answer:
                if self.extract_number(prediction.bonus_answer) == nearest_answer or \
                        self.extract_number(prediction.bonus_answer) == upper_nearest_answer:
                    # print("nearest answer:- ", prediction.user)
                    point_count += bonus_score_by_match
                    obj.nearest = True
                    obj.matching = False

            if created:
                obj.last_increased_by = point_count
                obj.points_scored = point_count
                obj.save()
            else:
                obj.points_scored -= obj.last_increased_by
                obj.last_increased_by = point_count
                obj.points_scored = point_count
                obj.save()
