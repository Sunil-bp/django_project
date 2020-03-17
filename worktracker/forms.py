from django import forms
from django.forms import ModelForm, Textarea
from django.contrib.auth.models import User
from worktracker.models import Login_data,Task,Userstat,Rules

class View_3_form(ModelForm):


    class Meta:
        model = Task
        fields = ['priority', 'description', 'notes', 'tags']
        labels = {
            'description': ('Describe the task at hand'),

        }
        help_texts = {
            'description': ('Explain the task '),
            'notes': ('Complete explanation of everyting the task at hand'),
        }
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 4, 'cols': 5}),
            'tags': forms.Textarea(attrs={'rows': 2, 'cols': 5}),
            'description': forms.Textarea(attrs={'cols': 3, 'rows': 3})}

class Rules_form(ModelForm):
    class Meta:
        model = Rules
        fields = ['rule', 'notes',]
        labels = {
            'rule': ('Rules'),

        }
        help_texts = {
            'rule': ('State the rule  '),
            'notes': ('Complete explanation of everyting the rule at hand'),
        }
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 4, 'cols': 5}),
           }


class Stop_task_form(ModelForm):

    def __init__(self, *args, **kwargs):
        super(Stop_task_form, self).__init__(*args, **kwargs)
        self.fields['description'].widget.attrs['readonly'] = True
        self.fields['notes'].widget.attrs['readonly'] = True
        self.fields['tags'].widget.attrs['readonly'] = True
        self.fields['create_on'].widget.attrs['readonly'] = True

        self.fields['priority'].widget.attrs['readonly'] = True
        self.fields['timetaken'].widget.attrs['readonly'] = True

    class Meta:
        model = Task
        fields = ['priority', 'description', 'notes', 'tags','create_on','timetaken','ending']
        labels = {
            'description': ('Describe the task at hand'),
        }
        help_texts = {
            'description': ('Explain the task '),
            'notes': ('Complete explanation of everyting the task at hand'),
        }
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 4, 'cols': 5}),
            'tags': forms.Textarea(attrs={'rows': 2, 'cols': 5}),
            'description': forms.Textarea(attrs={'cols': 3, 'rows': 3  })}

        disabled = {'description', 'notes', 'tags','create_on','timetaken'}


