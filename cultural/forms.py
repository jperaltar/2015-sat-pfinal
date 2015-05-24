from django import forms

COLORS_CHOICES = (('aqua', 'Aqua'),
                    ('green', 'Green'),
                    ('red', 'Red'),
                    ('white', 'White'))

CHOICES = (('Gratuito', 'Gratuito'),
            ('2 euros', '2 euros'),
            ('5 euros', '5 euros'))

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', max_length=100, widget=forms.PasswordInput())

class StyleForm(forms.Form):
    title = forms.CharField(label='Titulo', max_length=100, required=True)
    description = forms.CharField(label='Descripcion', max_length=256, widget=forms.Textarea, required=True)
    color = forms.MultipleChoiceField(required=True, widget=forms.RadioSelect, choices=COLORS_CHOICES)

class SearchForm(forms.Form):
    search = forms.CharField(label='SearchBox', max_length=256)
    price = forms.MultipleChoiceField(required=False, widget=forms.Select, choices=CHOICES)

class CommentForm(forms.Form):
    comment = forms.CharField(label='Comment', max_length=256, widget=forms.Textarea, required=True)