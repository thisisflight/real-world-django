from django import forms
from .models import Enroll, Event


class EventCreateUpdateForm(forms.ModelForm):
    date_start = forms.DateTimeField(label='Дата начала',
                                     widget=forms.DateTimeInput(format="%Y-%m-%dT%H:%M",
                                                                attrs={'type': 'datetime-local'})
                                     )

    class Meta:
        model = Event
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['is_private'].widget.attrs.update({'class': 'form-control form-check-input'})
        select_fields = ('category', 'features')
        for field in select_fields:
            self.fields[field].widget.attrs.update({'class': 'form-select'})
        fields_form_control = ('title', 'logo', 'description', 'date_start', 'participants_number')
        for field in fields_form_control:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')

        if Event.objects.filter(title=title).exists():
            raise forms.ValidationError(f'Событие с названием {title} уже существует')
        return cleaned_data


class EnrollToEventForm(forms.ModelForm):
    class Meta:
        model = Enroll
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget = forms.HiddenInput()

    def clean(self):
        cleaned_data = super().clean()
        if Enroll.objects.filter(user=cleaned_data.get('user'), event=cleaned_data.get('event')).exists():
            raise forms.ValidationError(f'Вы уже записаны на это событие')
        return cleaned_data
