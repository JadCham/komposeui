from django import forms
from .models import Upload
from django.core.exceptions import ValidationError
from kompose_ui import settings
from .validators import validate_file_extension
import logging

# Get logger instance
logger = logging.getLogger('default')


class UploadFileForm(forms.ModelForm):
    """
       Upload Form Class
       Handles creation and display of the upload form

       :fields input_text: Text area input for the web form to paste docker compose files
       :fields input_file: File input for the web form to upload docker compose files
       """
    class Meta:
        model = Upload
        fields = ["input_file", "input_text"]

    input_text = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'id': 'input'}),
                                 required=False)
    input_file = forms.FileField(widget=forms.FileInput(attrs={'class': 'hidden', 'type': 'file',
                                                               'onchange': "$('#converter').submit();"}),
                                 required=False)
    file_upload = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control hidden', 'id': 'input',
                                                               'type': 'hidden'}), required=False)

    def clean_file(self):
        file = self.cleaned_data.get('input_file')
        if file:    # Check if file exists
            try:
                validate_file_extension(file)
            except ValidationError as e:
                logger.error(e)
            return file
