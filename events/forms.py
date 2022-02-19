from django import forms
from .models import Enroll, Event, Category, Feature, Favorite, Review


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


class EventFilterForm(forms.Form):
    category = forms.ModelChoiceField(label='Категория',
                                      queryset=Category.objects.all(),
                                      required=False)
    features = forms.ModelMultipleChoiceField(label='Свойства',
                                              queryset=Feature.objects.all(),
                                              required=False)
    date_start = forms.DateTimeField(label='Дата начала',
                                     widget=forms.DateInput(format="%Y-%m-%d",
                                                            attrs={'type': 'date'}),
                                     required=False)
    date_end = forms.DateTimeField(label='Дата окончания',
                                   widget=forms.DateInput(format="%Y-%m-%d",
                                                          attrs={'type': 'date'}),
                                   required=False)
    is_private = forms.BooleanField(label='Private',
                                    widget=forms.CheckboxInput(attrs={'type': 'checkbox',
                                                                      'class': 'form-check-input'}),
                                    required=False)
    is_available = forms.BooleanField(label='Есть места',
                                      widget=forms.CheckboxInput(attrs={'type': 'checkbox',
                                                                        'class': 'form-check-input'}),
                                      required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].widget.attrs.update({'class': 'form-select'})
        self.fields['features'].widget.attrs.update({'class': 'form-select', 'multiple': True})
        self.fields['date_start'].widget.attrs.update({'class': 'form-control'})
        self.fields['date_end'].widget.attrs.update({'class': 'form-control'})


class EventAddToFavoriteForm(forms.ModelForm):
    class Meta:
        model = Favorite
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget = forms.HiddenInput()

    def clean(self):
        cleaned_data = super().clean()

        if Favorite.objects.filter(user=cleaned_data['user'], event=cleaned_data['event']).exists():
            raise forms.ValidationError(f'Событие уже добавлено в избранное')

        return cleaned_data


class ReviewForm(forms.ModelForm):
    CHOICES = ((1, 1), (2, 2), (3, 3), (4, 4), (5, 5))
    rate = forms.ChoiceField(label='Рейтинг', choices=CHOICES)

    class Meta:
        model = Review
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].widget = forms.HiddenInput()
        self.fields['event'].widget = forms.HiddenInput()
        self.fields['rate'].widget.attrs.update({'class': 'form-select'})
        self.fields['text'].widget.attrs.update({'class': 'form-control', 'rows': '3'})

    def clean(self):
        cleaned_data = super().clean()
        if Review.objects.filter(user=cleaned_data['user'], event=cleaned_data['event']).exists():
            raise forms.ValidationError(f'Вы уже оставили отзыв на это событие')

        return cleaned_data
