from django import forms
from .models import Homework, Exam, HomeworkGrade, ExamGrade
from django.forms.models import inlineformset_factory


class HomeworkCreationForm(forms.ModelForm):

    hw_details = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Homework
        fields = ("hw_no", "hw_details",)


class ExamCreationForm(forms.ModelForm):

    exam_details = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Exam
        fields = ("exam_no", "exam_details",)


HomeworkGradeFormset = inlineformset_factory(Homework, HomeworkGrade, fields=("grade",), can_delete=False)
ExamGradeFormset = inlineformset_factory(Exam, ExamGrade, fields=("grade",), can_delete=False)
