from django import forms
from django.core.files.uploadhandler import InMemoryUploadedFile
from django.core.exceptions import ValidationError
class UserBioForm(forms.Form):
    name = forms.CharField()
    age = forms.IntegerField(label='You age', min_value=1, max_value=99)
    bio = forms.CharField(label='Biography', widget=forms.Textarea)

def validate_file_name(file: InMemoryUploadedFile) -> None:
    if file.name and 'virus' in file.name:
        raise ValidationError('В названии файла не должно быть слово - virus')
class UploadFileForm(forms.Form):
    file = forms.FileField(validators=[validate_file_name])