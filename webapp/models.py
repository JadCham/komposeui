from django.db import models


class Upload(models.Model):
    input_file = models.FileField(upload_to="uploads/docker-compose/", blank=True, null=True)
    timestamp = models.DateTimeField(auto_now=True)
    input_text = models.TextField(blank=True, null=True)
    ip = models.CharField(max_length=15, blank=True, null=True)

    warning = models.CharField(max_length=300, blank=True, null=True)
    output_text = models.TextField(blank=True, null=True)
    output_file = models.FilePathField(blank=True, null=True)

    def __str__(self):
        return "{0}#{1}".format(self.timestamp, self.id)
