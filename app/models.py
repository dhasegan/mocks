from django.db import models

from django.contrib.auth.models import User

class MUser(User):
    description = models.CharField(max_length=400)
    skypeId = models.CharField(max_length=40)
    isMocker = models.BooleanField(default=False)
    price = models.CharField(max_length=40)

    def __unicode__(self):
        return self.email

class Interview(models.Model):
    mocker = models.ForeignKey(MUser, related_name="mer")
    mockee = models.ForeignKey(MUser, related_name="mee", null=True, blank=True)
    start = models.DateTimeField()

    def __unicode__(self):
        return str(self.start)