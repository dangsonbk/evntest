from django import forms
from django.forms.widgets import RadioSelect, Textarea
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from quiz.models import Profile

BRANCH_CHOICES = [
    ('tong-cong-ty-phat-dien-1', _('Tổng công ty Phát điện 1')),
    ('cong-ty-co-phan-nhiet-dien-quang-ninh', _('Công ty Cổ phần Nhiệt điện Quảng Ninh')),
    ('cong-ty-co-phan-thuy0dien-da-nhim-ham-thuan-da-mi', _('Công ty Cổ phần Thủy điện Đa Nhim-Hàm Thuận-Đa Mi')),
    ('cong-ty-nhiet-dien-duyen-hai', _('Công ty Nhiệt điện Duyên Hải')),
    ('cong-ty-nhiet-dien-nghi-son', _('Công ty Nhiệt điện Nghi Sơn')),
    ('cong-ty-nhiet-dien-uong-bi', _('Công ty Nhiệt điện Uông Bí')),
    ('cong-ty-thuy-dien-dai-ninh', _('Công ty Thủy điện Đại Ninh')),
    ('cong-ty-thuy-dien-dong-nai', _('Công ty Thủy điện Đồng Nai')),
    ('cong-ty-thuy-dien-ban-ve', _('Công ty Thủy điện Bản Vẽ')),
    ('cong-ty-thuy-dien-song-tranh', _('Công ty Thủy điện Sông Tranh')),
    ('cong-ty-co-phan-phat-trien-dien-luc-viet-nam', _('Công ty Cổ phần Phát triển Điện lực Việt Nam')),
    ('thuc-tap-vien-dhd', _('Thực tập viên DHD'))
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
            'title': _('Title'),
            'dob': _('DoB'),
            'id_card': _('Identity Card'),
            'branch': _('Branch')
        }

        widgets = {
            'gender': forms.Select(attrs={'class': 'input is-normal'}),
            'department': forms.TextInput(attrs={'class': 'input is-normal'}),
            'title': forms.TextInput(attrs={'class': 'input is-normal'}),
            'id_card': forms.TextInput(attrs={'class': 'input is-normal'}),
            'branch': forms.Select(attrs={'class': 'input is-normal'}, choices=BRANCH_CHOICES),
            'dob': forms.DateInput(attrs={'class': 'input is-normal'}),
        }
