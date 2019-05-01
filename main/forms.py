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

    # def __init__(self, *args, **kwargs):
    #     super(LabForm, self).__init__(*args, **kwargs)
    #     self.fields['start_date'].widget = widgets.AdminSplitDateTime()
    #     self.fields['due_date'].widget = widgets.AdminSplitDateTime()

class TodoForm(forms.ModelForm):

    class Meta:
        model = Todo
        fields = ['title']

class TodoCheckboxForm(forms.Form):

    # todos = forms.ModelMultipleChoiceField(
    #                     widget = forms.CheckboxSelectMultiple,
    #                     queryset = Todo.objects.all()
    # #            )

    # todos = forms.choi

    # todos = forms.BooleanField

    # class Meta:
    #     model = Todos
    #     fields = ['todos']

    def __init__(self, lab, *args, **kwargs):
        super(TodoCheckboxForm, self).__init__(*args, **kwargs)
        # todos = Todo.objects.filter(lab=lab, completed=False)
        self.fields['todos'] = forms.ModelMultipleChoiceField(
                                widget = forms.CheckboxSelectMultiple,
                                queryset = Todo.objects.filter(lab=lab, completed=False)
                                )
        
        




TodoFormSet = inlineformset_factory(Lab, Todo, form=TodoForm)