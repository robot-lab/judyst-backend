from django.db import models


class DocumentSupertype(models.Model):
    name = models.CharField("name od supertype", max_length=45, unique=True)


class Owner(models.Model):
    pk = models.IntegerField(primary_key=True)


class Document(models.Model):
    doc_id = models.CharField("id of document", max_length=45, unique=True)
    text = models.TextField("source of document")
    type = models.ForeignKey(DocumentSupertype, on_delete=models.PROTECT)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    is_visible = models.BooleanField(default=True)
