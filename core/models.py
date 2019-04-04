import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings


class DocumentSupertype(models.Model):
    name = models.CharField("name of supertype",
                            max_length=settings.TEXT_FIELD_LENGTH, unique=True)


class Owner(models.Model):
    owner_key = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                 editable=False)


class Document(models.Model):
    doc_id = models.CharField("id of document",
                              max_length=settings.TEXT_FIELD_LENGTH,
                              unique=True)
    text = models.TextField("source of document")
    doc_type = models.ForeignKey(DocumentSupertype, on_delete=models.PROTECT)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    is_visible = models.BooleanField(default=True)


class AnalyzerType(models.Model):
    name = models.CharField("name of analyze, which provide these analyzers",
                            max_length=settings.TEXT_FIELD_LENGTH, unique=True)


class Analyzer(models.Model):
    version = models.IntegerField("version of current analyzer")
    name = models.CharField("name of analyzer",
                            max_length=settings.TEXT_FIELD_LENGTH)
    analyzer_type = models.ForeignKey(AnalyzerType, on_delete=models.PROTECT)

    class Meta:
        unique_together = ('version', 'name',)


class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=settings.TEXT_FIELD_LENGTH)
    last_name = models.CharField(max_length=settings.TEXT_FIELD_LENGTH)
    owner = models.OneToOneField(Owner, on_delete=models.CASCADE)

    @classmethod
    def create(cls, **kwargs):
        kwargs['owner'] = Owner.objects.create()
        user = cls(**kwargs)
        user.save()
        return user

    def __str__(self):
        return self.email


class Organisation(models.Model):
    name = models.CharField(max_length=settings.TEXT_FIELD_LENGTH, unique=True)
    registration_date = models.DateField(auto_now=True)
    is_activated = models.BooleanField(default=False)
    members = models.ManyToManyField(CustomUser)
    owner = models.OneToOneField(Owner, on_delete=models.CASCADE)

    @classmethod
    def create(cls, **kwargs):
        kwargs['owner'] = Owner.objects.create()
        org = cls(**kwargs)
        org.save()
        return org


class TextPosition(models.Model):
    start_position = models.IntegerField()
    length = models.IntegerField()
    document = models.ForeignKey(Document, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('start_position', 'length', 'document')


class Analyze(models.Model):
    time = models.DateTimeField(blank=True)
    analyzer = models.ForeignKey(Analyzer, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True)
    text_position = models.ForeignKey(TextPosition, on_delete=models.PROTECT,
                                      blank=True)
    raw_data = models.ForeignKey("RawData", on_delete=models.PROTECT,
                                 blank=True)

    def clean(self):
        super().clean()
        if (self.text_position is None and self.raw_data is not None) or \
                (self.text_position is not None and self.raw_data is None):
            raise ValidationError(_('Validation error text'),
                                  code="exactly one of raw data and tex "
                                       "position must be null")


class RawData(models.Model):
    text = models.TextField()
    analyze_source = models.OneToOneField(Analyze, on_delete=models.SET_NULL,
                                          null=True)


class Link(models.Model):
    doc_from = models.ForeignKey(Document, on_delete=models.CASCADE,
                                 related_name="source_of_link")
    doc_to = models.ForeignKey(Document, on_delete=models.CASCADE,
                               related_name="link_value")
    analyze_source = models.OneToOneField(Analyze, on_delete=models.SET_NULL,
                                          null=True)
    text_position = models.ManyToManyField(TextPosition)


class PropertyType(models.Model):
    name = models.CharField(max_length=settings.TEXT_FIELD_LENGTH, unique=True)


class Property(models.Model):
    int_value = models.IntegerField(blank=True)
    text_value = models.CharField(max_length=settings.TEXT_FIELD_LENGTH,
                                  blank=True)
    date_value = models.DateTimeField(blank=True)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    property_type = models.ForeignKey(PropertyType, on_delete=models.PROTECT)
    analyze_source = models.OneToOneField(Analyze, on_delete=models.SET_NULL,
                                          null=True)


class DataSource(models.Model):
    source_link = models.URLField()
    crawler_name = models.CharField(max_length=settings.TEXT_FIELD_LENGTH)
