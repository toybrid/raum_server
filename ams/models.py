import uuid
from django.db import models
from django.conf import settings
from core.models import ContainerType, Element, Status, Step, DataType, RelationType, BundleType

from helpers.model_base import RaumBaseClass

# Create your models here.

class Project(RaumBaseClass):
    class Meta:
        verbose_name_plural = 'Projects'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=64, unique=True)
    label = models.CharField(max_length=64)
    client_name = models.CharField(max_length=64, unique=True)

    def __str__(self) -> str:
        return self.code


class Container(RaumBaseClass):
    class Meta:
        unique_together = ('project','code')
        verbose_name_plural = 'Containers'

    def __str__(self) -> str:
        return self.code
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, )
    container_type = models.ForeignKey(ContainerType, on_delete=models.PROTECT)
    code = models.CharField(max_length=128)
    client_name = models.CharField(max_length=64)
    frame_range = models.JSONField(null=True, blank=True, default=dict)

class ContainerRelation(RaumBaseClass):
    class Meta:
        unique_together = ('from_container','relation_type')
        verbose_name_plural = 'Container Relations'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    from_container = models.ForeignKey(Container, on_delete=models.CASCADE)
    relation_type = models.ForeignKey(RelationType, on_delete=models.CASCADE)
    to_containers = models.ManyToManyField(Container, related_name='%(class)s_containers')

class Product(RaumBaseClass):
    class Meta:
        unique_together = ('container','step', 'element', 'data_type', 'lod', 'layer','version')
        verbose_name_plural = 'Products'

    def __str__(self) -> str:
        return self.slug

    def save(self, *args, **kwargs):
        if not self.version or self.version==0:
            try:
                latest_instance = Product.objects.filter(
                                                    container = self.container,
                                                    step = self.step,
                                                    element = self.element,
                                                    data_type = self.data_type,
                                                    layer = self.layer,
                                                    lod=self.lod
                                                    ).latest('created_at')
                next_version = latest_instance.version + 1
                self.version = next_version
            except self.DoesNotExist:
                self.version = 1
        self.slug = f'{self.container.project.code}/{self.container.code}/{self.step.code}/{self.element.code}/{self.data_type.code}/{self.lod}/{self.layer}/{self.version}'

        super(Product, self).save(*args, **kwargs)

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    container = models.ForeignKey(Container, on_delete=models.CASCADE, editable=False)
    step = models.ForeignKey(Step, on_delete=models.PROTECT)
    element = models.ForeignKey(Element, on_delete=models.PROTECT)
    data_type = models.ForeignKey(DataType, on_delete=models.PROTECT)
    lod = models.CharField(max_length=64)
    layer = models.CharField(max_length=128)
    task = models.CharField(max_length=64, blank=True, null=True)
    filepath = models.CharField(max_length=2048, unique=True, null=True, blank=True)
    extension = models.CharField(max_length=8)
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    frame_range = models.JSONField(null=True, blank=True, default=dict)
    version = models.IntegerField(null=True, blank=True, default=0)
    slug = models.CharField(max_length=4096, null=True, blank=True, editable=False, unique=True)
    metadata = models.JSONField(null=True, blank=True, default=dict)
    approved_at = models.DateTimeField(null=True, blank=True, editable=False)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET_NULL)

class ProductDependency(RaumBaseClass):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    dependencies = models.ManyToManyField(Product, related_name='%(class)s_products', blank=True)

class Bundle(RaumBaseClass):
    class Meta:
        unique_together = ('container','step','bundle_type','version')
    def save(self, *args, **kwargs):
        if not self.version or self.version==0:
            try:
                latest_instance = Bundle.objects.filter(
                                                    container = self.container,
                                                    step = self.step,
                                                    bundle_type = self.bundle_type,
                                                    ).latest('created_at')
                next_version = latest_instance.version + 1
                self.version = next_version
            except self.DoesNotExist:
                self.version = 1
        self.slug = f'{self.container.project.code}/{self.container.code}/{self.step.code}/{self.bundle_type.code}/{self.version}'

        super(Bundle, self).save(*args, **kwargs)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    container = models.ForeignKey(Container, on_delete=models.CASCADE)
    step = models.ForeignKey(Step, on_delete=models.SET_NULL, null=True)
    bundle_type = models.ForeignKey(BundleType, on_delete=models.SET_NULL, null=True)
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True)
    version = models.IntegerField(null=True, blank=True, default=0)
    description = models.TextField(null=True, blank=True)
    slug = models.CharField(max_length=4096, null=True, blank=True, editable=False, unique=True)
    products = models.ManyToManyField(Product, related_name='%(class)s_products', blank=True)
    approved_at = models.DateTimeField(null=True, blank=True, editable=False)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET_NULL)