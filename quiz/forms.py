from django import forms
from django.forms.widgets import RadioSelect, Textarea
from django.core.exceptions import ValidationError
from quiz.models import Profile

class QuestionForm(forms.Form):
    def __init__(self, question, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        choice_list = [x for x in question.get_answers_list()]
        self.fields["answers"] = forms.ChoiceField(choices=choice_list, widget=RadioSelect)

class EssayForm(forms.Form):
    def __init__(self, question, *args, **kwargs):
        super(EssayForm, self).__init__(*args, **kwargs)
        self.fields["answers"] = forms.CharField(
            widget=Textarea(attrs={'style': 'width:100%'}))


class QuizProfileForm(forms.ModelForm):
    full_name = forms.CharField(
        label='Họ tên', max_length=191, required=True,
        widget=forms.TextInput(attrs={'class': 'input is-normal'})
    )
    # identity_code = forms.CharField(
    #     label='Mã dự thi', max_length=191, required=False,
    #     widget=forms.TextInput(attrs={
    #         'class': 'input is-normal', 'readonly': 'readonly', 'disabled': 'disabled'
    #     })
    # )

    def __init__(self, *args, **kwargs):
        super(QuizProfileForm, self).__init__(*args, **kwargs)
        # self.fields['identity_code'].initial = self.instance.id
        self.fields['full_name'].initial = self.instance.user.first_name
        self.fields['department'].required = True
        # self.fields['branch'].required = True
        self.fields['full_name'].required = True
        self.fields['id_card'].required = True
    
    def clean_full_name(self):
        data = self.cleaned_data['full_name']
        if len(data) < 5:
            raise ValidationError('Tên quá ngắn!')
        return data

    def clean_id_card(self):
        data = self.cleaned_data['id_card']
        if len(data) < 3:
            raise ValidationError('Không hợp lệ')
        return data

    class Meta:
        model = Profile
        fields = (
            'full_name', 'gender', 'id_card', 'grade',
            'branch', 'dob', 'department', 'title'
        )

        labels = {
            'gender': 'Giới tính',
            'department': 'Phòng ban',
            'grade': 'Bậc thợ',
            'dob': 'Ngày sinh',
            'id_card': 'Mã nhân viên',
            'branch': 'Công ty',
            'title': 'Chức danh'
        }

        widgets = {
            'gender': forms.Select(attrs={'class': 'input is-normal'}),
            'department': forms.Select(attrs={'class': 'input is-normal'}),
            'id_card': forms.TextInput(attrs={'class': 'input is-normal', 'readonly': 'readonly'}),
            'grade': forms.TextInput(attrs={'class': 'input is-normal'}),
            'title': forms.TextInput(attrs={'class': 'input is-normal'}),
            # 'branch': forms.Select(attrs={'class': 'input is-normal'}),
            'dob': forms.DateInput(attrs={'class': 'input is-normal'}),
        }
