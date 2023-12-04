from django.forms import ModelForm
from my_auth.models import NewUser, Profile
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import authenticate
from django import forms
from PIL import Image


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Add a valid email address.')

    class Meta:
        model = NewUser
        fields = ('email', 'username', 'password1', 'password2', )
        # widgets = {
        #     'country': forms.SelectMultiple(attrs={'class': 'input-text', 'autofocus': True}),
        #     }
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirm your passowrd'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Enter your passowrd'})
        self.fields['username'].widget.attrs.update({'placeholder': 'Enter your username'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Enter your email address'})
		
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
 

class AccountVerificationForm(ModelForm):
	id = forms.IntegerField(min_value=1)
	
	class Meta:
		model = NewUser
		fields = ('is_active', 'id' )
        # widgets = {
        #     'is_active': forms.TextInput(attrs={'class': 'input-text', 'autofocus': True, "hidden":"hidden"}),
        #     }
    

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

    #     for field in self.fields:
    #         self.fields[field].widget.attrs.update({'class': 'form-control', 'hidden':'hidden'})
 

class TutorRegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Add a valid email address.')

    class Meta:
        model = NewUser
        fields = ('email', 'username', 'password1', 'password2', )
        # widgets = {
        #     'country': forms.SelectMultiple(attrs={'class': 'input-text', 'autofocus': True}),
        #     }
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirm your passowrd'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Enter your passowrd'})
        self.fields['username'].widget.attrs.update({'placeholder': 'Enter your username'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Enter your email address'})
		
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
 
class TutorAccRegistrationForm(ModelForm):

    class Meta:
        model = Profile
        fields = ('bio', 'image' )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].widget.attrs.update({'placeholder': 'Enter your image'})
        self.fields['bio'].widget.attrs.update({'placeholder': 'Enter your bio'})
		
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class AccountAuthenticationForm(UserChangeForm):

	password = forms.CharField(label='Password', widget=forms.PasswordInput)

	class Meta:
		model = NewUser
		fields = ('email', 'password')
       
        

	def clean(self):
		if self.is_valid():
			email = self.cleaned_data['email']
			password = self.cleaned_data['password']
			if not authenticate(email=email, password=password):
				raise forms.ValidationError("Invalid login")
    
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['password'].widget.attrs.update({'placeholder': 'Enter your passowrd'})
		self.fields['email'].widget.attrs.update({'placeholder': 'Enter your email address'})
		
		for field in self.fields:
			self.fields[field].widget.attrs.update({'class': 'form-control'})
 
   
    
                 
    

class AccountUpdateForm(forms.ModelForm):

	class Meta:
		model = NewUser
		fields = ['country', 'email', 'username', 'first_name', 'last_name', 'phone', 'disability',  ]

	def clean_email(self):
		email = self.cleaned_data['email']
		try:
			account = NewUser.objects.exclude(pk=self.instance.pk).get(email=email)
		except NewUser.DoesNotExist:
			return email
		raise forms.ValidationError('Email "%s" is already in use.' % account)

	def clean_username(self):
		username = self.cleaned_data['username']
		try:
			account = NewUser.objects.exclude(pk=self.instance.pk).get(username=username)
		except NewUser.DoesNotExist:
			return username
		raise forms.ValidationError('Username "%s" is already in use.' % username)
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['username'].widget.attrs.update({'placeholder': 'Enter your username'})
		self.fields['email'].widget.attrs.update({'placeholder': 'Email'})
		
		for field in self.fields:
			self.fields[field].widget.attrs.update({'class': 'form-control'})


class ProfileUpdateForm(forms.ModelForm):
	class Meta:
		model = Profile
		
		fields = ('bio', 'image', 'specialty', 'facebook_link','instagram_link','twitter_link','linkedin_link',)
    
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['image'].widget.attrs.update({'placeholder': 'Enter your image'})
		self.fields['bio'].widget.attrs.update({'placeholder': 'Enter your bio'})

		for field in self.fields:
			self.fields[field].widget.attrs.update({'class': 'form-control'})


class ProfilePicUpdateForm(forms.ModelForm):
	x = forms.FloatField(widget=forms.HiddenInput())
	y = forms.FloatField(widget=forms.HiddenInput())
	width = forms.FloatField(widget=forms.HiddenInput())
	height = forms.FloatField(widget=forms.HiddenInput())

	class Meta:
		fields = ('image',)
		model = Profile
		fields = ('image', 'x', 'y', 'width', 'height', )
		widgets = {
			'file': forms.FileInput(attrs={
				'accept': 'image/*'  # this is not an actual validation! don't rely on that!
			})
		}

		def save(self):
			photo = super(ProfilePicUpdateForm, self).save()

			x = self.cleaned_data.get('x')
			y = self.cleaned_data.get('y')
			w = self.cleaned_data.get('width')
			h = self.cleaned_data.get('height')

			image = Image.open(photo.file)
			cropped_image = image.crop((x, y, w+x, h+y))
			resized_image = cropped_image.resize((200, 200), Image.ANTIALIAS)
			resized_image.save(photo.file.path)

			return photo


    
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['image'].widget.attrs.update({'placeholder': 'Enter your image', 'id':'id_file'})

		for field in self.fields:
			self.fields[field].widget.attrs.update({'class': 'form-control'})