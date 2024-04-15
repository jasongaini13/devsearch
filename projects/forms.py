from django.forms import ModelForm
from .models import Project, Review
from django import forms

class ProjectForm(ModelForm):
    class Meta:
        model=Project
        fields=['title','fetured_image','description','demo_link','source_link','tags']
        widges ={
            'tags': forms.CheckboxSelectMultiple(),
        }

    def __init__(self,*args,**kwargs):
        super(ProjectForm,self).__init__(*args,**kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input','tags':'checkbox'})

        # self.fields['title'].widget.attrs.update({'class':'input','placeholder':'Add title'})

        # self.fields['description'].widget.attrs.update({'class':'input' })
        
class ReviewForm(ModelForm):
    class Meta:
        model= Review
        fields = ['value','body']

        labels={
            'value':'place your vote',
            'body':'add a comment with your vote'
        }        

    def __init__(self,*args,**kwargs):
        super(ReviewForm,self).__init__(*args,**kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input','tags':'checkbox'})