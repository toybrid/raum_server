import uuid
from django.db import models
from helpers.model_base import RaumBaseClass

# Create your models here.

class ContainerType(RaumBaseClass):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=64, unique=True)
    label = models.CharField(max_length=64)

    def __str__(self) -> str:
        return self.label

class Status(RaumBaseClass):
    class Meta:
        verbose_name_plural = 'Statuses'
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=64, unique=True)
    label = models.CharField(max_length=64)

    def __str__(self) -> str:
        return self.label

class Element(RaumBaseClass):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=64, unique=True)
    label = models.CharField(max_length=64)

    def __str__(self) -> str:
        return self.label

class DataType(RaumBaseClass):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=64, unique=True)
    label = models.CharField(max_length=64)

    def __str__(self) -> str:
        return self.label

class Step(RaumBaseClass):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=64, unique=True)
    label = models.CharField(max_length=64)

    def __str__(self) -> str:
        return self.label

class RelationType(RaumBaseClass):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=64, unique=True)
    label = models.CharField(max_length=64)

    def __str__(self) -> str:
        return self.label