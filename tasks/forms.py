from django import forms
from .models import Task
 

class TasksForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['tittle', 'description', 'important']
        widgets = {
            'tittle': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Introduce el titulo'}),
            'description': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Introduce la descripcion'}),
            'important': forms.CheckboxInput(attrs={'class':'form-check-input m-auto'}),
        }