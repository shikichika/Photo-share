from django import forms


from users.models import Galleries




class LoginGalleryForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Enter password',
    }))

    class Meta:
        model = Galleries
        fields = ['name', 'password']
    
    def __init__(self, *args, **kwargs):
        super(LoginGalleryForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'Enter gallery name'
        self.fields['password'].widget.attrs['placeholder'] = 'Enter password'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] ='form-control'


    def clean_detail(self):
        name = self.cleaned_data.get('name')
        password = self.cleaned_data.get('password')

        is_existed = Galleries.objects.filter(name=name, password=password).exists()

        print(is_existed)

        if is_existed == False:
            raise forms.ValidationError(
                "Invalid Value"
            )

            
        
        

