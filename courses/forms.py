from django import forms
from .models import HomeworkGrade, ExamGrade
from django.forms.models import modelformset_factory

"""
class HomeworkGradesForm(forms.ModelForm):

    class Meta:
        model = HomeworkGrade
        fields = ("grade",)


class ExamGradesForm(forms.ModelForm):

    class Meta:
        model = ExamGrade
        fields = ("grade",)
"""

HomeworkGradeFormset = modelformset_factory(HomeworkGrade, fields=("grade",))
ExamGradeFormset = modelformset_factory(ExamGrade, fields=("grade",))
