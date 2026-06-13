from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.html import format_html

from .models import Profile


class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password1",
            "password2",
        ]


class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = [
            "email",
        ]


class AvatarInput(forms.ClearableFileInput):
    """
    Sobrescreve apenas o método render do ClearableFileInput
    para colocar o checkbox 'Remover avatar' colado no seu label.
    """

    def render(self, name, value, attrs=None, renderer=None):
        # Checkbox de limpar (só aparece se já existe um arquivo salvo)
        clear_checkbox = ''
        if value and hasattr(value, 'url'):
            clear_id = f'id_{name}-clear'
            clear_checkbox = format_html(
                '<span class="avatar-clear">'
                '<input type="checkbox" name="{}-clear" id="{}">'
                '<label for="{}" style="margin-left:6px;">Remover avatar atual</label>'
                '</span><br>',
                name, clear_id, clear_id,
            )

        # Renderiza o input de arquivo usando o método original do FileInput
        self.template_name = 'django/forms/widgets/file.html'
        file_input = super(forms.ClearableFileInput, self).render(name, value, attrs, renderer)

        return format_html('{}{}', clear_checkbox, file_input)


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = [
            "avatar",
            "bio",
            "github",
            "linkedin",
        ]
        widgets = {
            'avatar': AvatarInput(),
        }