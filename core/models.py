from django.contrib.auth.models import AbstractUser
from django.db import models


class DocumentSupertype(models.Model):
    name = models.CharField("name of supertype", max_length=45, unique=True)


class Owner(models.Model):
    owner_key = models.IntegerField(primary_key=True)


class Document(models.Model):
    doc_id = models.CharField("id of document", max_length=45, unique=True)
    text = models.TextField("source of document")
    type = models.ForeignKey(DocumentSupertype, on_delete=models.PROTECT)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    is_visible = models.BooleanField(default=True)


class AnalyzerType(models.Model):
    name = models.CharField("name of analyze, which provide these analyzers",
                            max_length=100, unique=True)


class Analyzer(models.Model):
    version = models.IntegerField("version of current analyzer")
    name = models.CharField("name of analyzer", max_length=100)
    analyzer_type = models.ForeignKey(AnalyzerType, on_delete=models.PROTECT)

    class Meta:
        unique_together = ('version', 'name',)


class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_activated = models.BooleanField(default=False)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)

    @classmethod
    def create(cls, **kwargs):
        if 'owner' in kwargs:
            del kwargs['owner']
        user = cls(owner=Owner.objects.create(), **kwargs)
        user.save()
        return user

    def __str__(self):
        return self.email


class Organisation(models.Model):
    name = models.CharField(max_length=150)
    registration_date = models.DateField(auto_now=True)
    is_activated = models.BooleanField(default=False)
    members = models.ManyToManyField(CustomUser, through='OrganisationUser',
                                     through_fields=('organisation', 'user'))

    @classmethod
    def create(cls, **kwargs):
        if 'owner' in kwargs:
            del kwargs['owner']
        org = cls(owner=Owner.objects.create(), **kwargs)
        org.save()
        return org


class OrganisationUser(models.Model):
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('organisation', 'user',)
