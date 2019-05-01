from django import forms
from .models import Lab, Todo
from django.forms import inlineformset_factory


class LabForm(forms.ModelForm):
    title = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea)
    start_date = forms.DateField(widget=forms.SelectDateWidget)
    due_date = forms.DateField(widget=forms.SelectDateWidget)

    class Meta:
        model = Lab
        fields = ['title', 'description', 'start_date', 'due_date']

class TodoForm(forms.ModelForm):

    class Meta:
        model = Todo
        fields = ['title']

class TodoCheckboxForm(forms.Form):

    def __init__(self, lab, *args, **kwargs):
        super(TodoCheckboxForm, self).__init__(*args, **kwargs)
        self.fields['todos'] = forms.ModelMultipleChoiceField(
                                widget = forms.CheckboxSelectMultiple,
                                queryset = Todo.objects.filter(lab=lab, completed=False)
                                )
        
        




TodoFormSet = inlineformset_factory(Lab, Todo, form=TodoForm)