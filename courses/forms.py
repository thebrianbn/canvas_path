from django import forms
from .models import Homework, Exam, HomeworkGrade, ExamGrade
from django.forms.models import inlineformset_factory

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

HomeworkGradeFormset = inlineformset_factory(Homework, HomeworkGrade, fields=("grade",), can_delete=False)
ExamGradeFormset = inlineformset_factory(Exam, ExamGrade, fields=("grade",), can_delete=False)
