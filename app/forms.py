from django import forms


class UserUpdateProfileForm(forms.Form):
    username = forms.CharField(label='You name', max_length=120)
    email = forms.EmailField(label='You email address',)
    profile_image = forms.ImageField(label='Profile image', required=False)


class PostCreateForm(forms.Form):
    title = forms.CharField(label='Title of the post', max_length=120)
    text = forms.CharField(label='Post content')
    image = forms.ImageField(required=False)