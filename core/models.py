from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError


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
    name = models.CharField(max_length=150, unique=True)
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
                                 related_name="source of link")
    doc_to = models.ForeignKey(Document, on_delete=models.CASCADE,
                               related_name="link value")
    analyze_source = models.OneToOneField(Analyze, on_delete=models.SET_NULL,
                                          null=True)
    text_position = models.ManyToManyField(TextPosition,
                                           through="LinkPosition",
                                           through_fields=("link",
                                                           "text_position"))


class LinkPosition(models.Model):
    link = models.ForeignKey(Link, on_delete=models.CASCADE)
    text_position = models.ForeignKey(TextPosition, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('text_position', 'link',)


class PropertyType(models.Model):
    name = models.CharField(max_length=45, unique=True)


class Property(models.Model):
    int_value = models.IntegerField(blank=True)
    text_value = models.CharField(max_length=45, blank=True)
    date_value = models.DateTimeField(blank=True)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    type = models.ForeignKey(PropertyType, on_delete=models.PROTECT)
    analyze_source = models.OneToOneField(Analyze, on_delete=models.SET_NULL,
                                          null=True)
