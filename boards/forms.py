from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Board

# class BoardForm(forms.Form):
#     title = forms.CharField(label='제목 ', widget=forms.TextInput(attrs={
#                                                     'placeholder' : 'What is The Title ?',
#     }))
#     content = forms.CharField(label='내용',
#                                 error_messages={'required' : '제발 내용을 넣어주세요'}, 
#                                 widget=forms.Textarea(attrs={
#                                         'class' : 'Content-input',
#                                         'rows' : 5,
#                                         'cols' : 50,
#                                         'placeholder' : 'Fill the content'
#                                                                             }))

class BoardForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ['title', 'content',]
        widgets = {'title' : forms.TextInput(attrs={
            'placeholder' : '제목을 입력하세요',
            'class' : 'title'}),
            'content' : forms.Textarea(attrs={
                'placeholder' : '내용을 입력하세요',
                'classs' : 'content',
                'rows' : 5,
                'cols' : 50,})}
        error_messages = {'title' : {'required' : '제발 입력해 주세요.'},
                            'content' : {'required' : '내용 입력하세요.'}}
    
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit', '작성!'))