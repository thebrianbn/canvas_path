from django import forms
from .models import Homework, Exam, HomeworkGrade, ExamGrade
from django.forms.models import inlineformset_factory


class HomeworkCreationForm(forms.ModelForm):
    """ Form for professors to create homeworks. """

    hw_details = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Homework
        fields = ("hw_no", "hw_details",)


class ExamCreationForm(forms.ModelForm):
    """ Form for professors to create exams. """

    exam_details = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Exam
        fields = ("exam_no", "exam_details",)


# create formset classes for grade submission
HomeworkGradeFormset = inlineformset_factory(Homework, HomeworkGrade, fields=("grade",), can_delete=False)
ExamGradeFormset = inlineformset_factory(Exam, ExamGrade, fields=("grade",), can_delete=False)
