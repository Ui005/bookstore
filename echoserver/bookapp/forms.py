from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Books
from .models import UserProfile


class BookForm(forms.ModelForm):
    class Meta:
        model = Books
        fields = ['title', 'author', 'price']



User = get_user_model()
class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Обязательное поле.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Обязательное поле.')
    role = forms.ChoiceField(choices=UserProfile.USER_ROLES, required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'role')

    def save(self, commit=True):
        user = super().save(commit=True)  # Save user immediately
        profile, created = UserProfile.objects.get_or_create(user=user)
        profile.first_name = self.cleaned_data['first_name']
        profile.last_name = self.cleaned_data['last_name']
        profile.role = self.cleaned_data['role']
        profile.save()
        return user