from django import forms

from user.models import Profiles


class ProfileForm(forms.ModelForm):

    def clean_max_dating_age(self):

        max_dating_age = self.cleaned_data.get('max_dating_age')
        min_dating_age = self.cleaned_data.get('min_dating_age')

        if max_dating_age < min_dating_age:
            raise forms.ValidationError('最大匹配年龄必须大于等于最小匹配年龄')

        return max_dating_age

    def clean_max_distance(self):
        min_distance = self.cleaned_data.get('min_distance')
        max_distance = self.cleaned_data.get('max_distance')

        if min_distance > max_distance :
            raise forms.ValidationError('最大匹配公里数必须大于等于最小匹配公里数')
        return max_distance


    class Meta:
        model = Profiles
        fields = [
            'location',
            'min_distance',
            'max_distance',
            'min_dating_age',
            'max_dating_age',
            'dating_sex',
        ]
        # fields = '__all__' 如果全部字段都要都话就这么写
