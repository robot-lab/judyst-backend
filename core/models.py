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
