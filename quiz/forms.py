from django import forms
from django.forms.widgets import RadioSelect, Textarea
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from quiz.models import Profile

BRANCH_CHOICES = [
    ('tong-cong-ty-phat-dien-1', _('tong-cong-ty-phat-dien-1')),
    ('cong-ty-co-phan-nhiet-dien-quang-ninh', _('cong-ty-co-phan-nhiet-dien-quang-ninh')),
    ('cong-ty-co-phan-thuy-dien-da-nhim-ham-thuan-da-mi', _('cong-ty-co-phan-thuy0dien-da-nhim-ham-thuan-da-mi')),
    ('cong-ty-nhiet-dien-duyen-hai', _('cong-ty-nhiet-dien-duyen-hai')),
    ('cong-ty-nhiet-dien-nghi-son', _('cong-ty-nhiet-dien-nghi-son')),
    ('cong-ty-nhiet-dien-uong-bi', _('cong-ty-nhiet-dien-uong-bi')),
    ('cong-ty-thuy-dien-dai-ninh', _('cong-ty-thuy-dien-dai-ninh')),
    ('cong-ty-thuy-dien-dong-nai', _('cong-ty-thuy-dien-dong-nai')),
    ('cong-ty-thuy-dien-ban-ve', _('cong-ty-thuy-dien-ban-ve')),
    ('cong-ty-thuy-dien-song-tranh', _('cong-ty-thuy-dien-song-tranh')),
    ('cong-ty-co-phan-phat-trien-dien-luc-viet-nam', _('cong-ty-co-phan-phat-trien-dien-luc-viet-nam')),
    ('thuc-tap-vien-dhd', _('thuc-tap-vien-dhd'))
]


class QuestionForm(forms.Form):
    def __init__(self, question, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        choice_list = [x for x in question.get_answers_list()]
        self.fields["answers"] = forms.ChoiceField(choices=choice_list,
                                                   widget=RadioSelect)


class EssayForm(forms.Form):
    def __init__(self, question, *args, **kwargs):
        super(EssayForm, self).__init__(*args, **kwargs)
        self.fields["answers"] = forms.CharField(
            widget=Textarea(attrs={'style': 'width:100%'}))


class QuizProfileForm(forms.ModelForm):
    full_name = forms.CharField(
        label=_('Full Name'), max_length=191, required=True,
        widget=forms.TextInput(attrs={'class': 'input is-normal'})
    )
    identity_code = forms.CharField(
        label=_('Identity Code'), max_length=191, required=False,
        widget=forms.TextInput(attrs={
            'class': 'input is-normal', 'readonly': 'readonly', 'disabled': 'disabled'
        })
    )

    def __init__(self, *args, **kwargs):
        super(QuizProfileForm, self).__init__(*args, **kwargs)
        self.fields['identity_code'].initial = self.instance.id
        self.fields['full_name'].initial = self.instance.user.first_name
        self.fields['department'].required = True
        self.fields['full_name'].required = True
        self.fields['id_card'].required = True
    
    def clean_full_name(self):
        data = self.cleaned_data['full_name']
        if len(data) < 5:
            raise ValidationError(_('Full name too short!'))
        return data

    def clean_id_card(self):
        data = self.cleaned_data['id_card']
        if len(data) < 9:
            raise ValidationError(_('ID Card too short!'))
        return data

    class Meta:
        model = Profile
        fields = (
            'full_name', 'gender', 'identity_code', 'id_card', 
            'branch', 'dob', 'department', 'title'
        )

        labels = {
            'gender': _('Gender'),
            'department': _('Department'),
            'title': _('Position'),
            'dob': _('DoB'),
            'id_card': _('Identity Card'),
            'branch': _('Branch')
        }

        widgets = {
            'gender': forms.Select(attrs={'class': 'input is-normal'}),
            'department': forms.Select(attrs={'class': 'input is-normal'}),
            'title': forms.TextInput(attrs={'class': 'input is-normal'}),
            'id_card': forms.TextInput(attrs={'class': 'input is-normal'}),
            'branch': forms.Select(attrs={'class': 'input is-normal'}, choices=BRANCH_CHOICES),
            'dob': forms.DateInput(attrs={'class': 'input is-normal'}),
        }
