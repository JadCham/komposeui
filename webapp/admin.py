from django.contrib import admin
from .models import Upload


class UploadAdmin(admin.ModelAdmin):
    """
    Upload Admin Class
    Displays uploaded files and their corresponding conversions in the admin page
    """

    list_display = ("id", "input_text", "timestamp", "output_text")
    search_fields = ("id", "timestamp", "ip")
    readonly_fields = ['timestamp']


admin.site.register(Upload, UploadAdmin)
