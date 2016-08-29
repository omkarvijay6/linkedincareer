from django.contrib.auth.forms import AuthenticationForm


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['password'].widget.attrs['class'] = 'moto-widget-contact_form-field'
        self.fields['password'].widget.attrs['placeholder'] = 'Enter your password *'
        self.fields['username'].widget.attrs['class'] = 'moto-widget-contact_form-field'
        self.fields['username'].widget.attrs['placeholder'] = 'username'
