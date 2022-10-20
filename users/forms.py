from django import forms


from .models import Owner


class RegisterForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Enter password',
    }))

    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Enter password again',
    }))
    class Meta:
        model = Owner
        fields = ['username', 'email', 'password']

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] ='Enter username'
        self.fields['email'].widget.attrs['placeholder'] ='Enter email'


    def clean_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "Password does not match."
            )
        if password.isalnum() == False:
            raise forms.ValidationError(
                "Password must be alphabet and number"
            )
        
        if len(password) < 6 or len(password) > 14:
            raise forms.ValidationError(
                "Password must be more than 3 and less than 40"
            )
        
        return password

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if username.isalnum() == False:
            raise forms.ValidationError(
                "Username must be alphabet and number"
            )


        if len(username) < 3 or len(username) > 40:
            raise forms.ValidationError(
                "Username needs to be more than 3 and less than 40"
            )
        
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        print(Owner.objects.filter(email=email).exists())
        if Owner.objects.filter(email=email).exists()==True:
            raise forms.ValidationError(
                "This email is already used"
            )
        return email
        
class LoginForm(forms.ModelForm):
    class Meta:
        model = Owner
        fields = ['email', 'password']

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['placeholder'] ='Enter email'
        self.fields['password'].widget.attrs['placeholder'] ='Enter password'

        for field in self.fields:
            self.fields[field].widget.attrs['class'] ='form-control'

    def clean_body(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if Owner.objects.filter(email=email, password=password).exists()==False:
            raise forms.ValidationError(
                'Invalid value'
            )
        

    