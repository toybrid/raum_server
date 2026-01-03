from django.db import models, transaction
from django.conf import settings


class TimeMixin(models.Model):
    '''
    Abstract base model to add created_at, updated_at, created_by, and updated_by fields.
    This mixin can be inherited by other models to automatically include these fields.
    '''
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=64, blank=True, null=True)
    updated_by = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        abstract = True

class UpdateMixin(models.Model):
    """
    Mixin class to provide an update_from_dict method for Django models.

    This abstract model allows updating specified fields of a model instance from a dictionary.
    The fields that can be updated should be listed in the 'updatable_fields' attribute of the subclass.

    Methods:
        update_from_dict(data: dict):
            Updates the model instance's fields specified in 'updatable_fields' with values from the provided 
            dictionary. Saves the instance after updating.

    Usage:
        class MyModel(UpdateMixin):
            updatable_fields = ['field1', 'field2']
    """
    class Meta:
        abstract = True

    def update_from_dict(self, data: dict):
        """
        Updates the model instance's fields from a given dictionary.

        Iterates over the fields specified in `self.updatable_fields` and updates each field with the corresponding 
        value from the `data` dictionary if present. After updating, saves the instance and returns it.

        Args:
            data (dict): A dictionary containing field-value pairs to update the instance.

        Returns:
            self: The updated model instance.
        """
        for field in self.updatable_fields:
            if field in data:
                setattr(self, field, data[field])
        self.save()
        return self

class ContainerType(TimeMixin):
    class Meta:
        verbose_name_plural = 'Container Types'
    code = models.CharField(max_length=64, unique=True)
    label = models.CharField(max_length=64)

    def __str__(self) -> str:
        return self.label

class Status(TimeMixin):
    class Meta:
        verbose_name_plural = 'Statuses'
    code = models.CharField(max_length=64, unique=True)
    label = models.CharField(max_length=64)

    def __str__(self) -> str:
        return self.label

class Element(TimeMixin):
    class Meta:
        verbose_name_plural = 'Elements'
    code = models.CharField(max_length=64, unique=True)
    label = models.CharField(max_length=64)

    def __str__(self) -> str:
        return self.label

class DataType(TimeMixin):
    class Meta:
        verbose_name_plural = 'Data Types'
    code = models.CharField(max_length=64, unique=True)
    label = models.CharField(max_length=64)

    def __str__(self) -> str:
        return self.label
    
class BundleType(TimeMixin):
    class Meta:
        verbose_name_plural = 'Bundle Types'
    code = models.CharField(max_length=64, unique=True)
    label = models.CharField(max_length=64)

    def __str__(self) -> str:
        return self.label
    
class Project(TimeMixin, UpdateMixin):
    """
    Represents a project entity with a unique code, label, and client name.
    Attributes:
        code (str): Unique, non-editable identifier for the project.
        label (str): Descriptive label for the project.
        client_name (str): Unique name of the client associated with the project.
        updatable_fields (list): Fields that can be updated ('label', 'client_name').
    Methods:
        __str__(): Returns the project's code as its string representation.
    Meta:
        verbose_name_plural: Plural name for the model in the admin interface ('Projects').
    """
    class Meta:
        verbose_name_plural = 'Projects'

    def __str__(self) -> str:
        return self.code
    
    code = models.CharField(max_length=64, unique=True, editable=False)
    label = models.CharField(max_length=64)
    client_name = models.CharField(max_length=64, unique=True)

    updatable_fields = ['label', 'client_name']


class Container(TimeMixin, UpdateMixin):
    """
    Represents a container entity within a project, encapsulating metadata and relationships.
    Attributes:
        project (Project): Reference to the associated project.
        code (str): Unique identifier for the container within a project.
        client_name (str): Name of the client associated with the container.
        container_type (ContainerType): Type/category of the container.
        frame_range (dict, optional): JSON field specifying the frame range; defaults to empty dict.
    Meta:
        unique_together: Ensures that the combination of 'project' and 'code' is unique.
        verbose_name_plural: Sets the plural name for the model as 'Containers'.
    updatable_fields (list): Specifies fields that can be updated: 'client_name', 'frame_range', 'container_type'.
    Methods:
        __str__(): Returns the container's code as its string representation.
    """
    class Meta:
        unique_together = ('project','code')
        verbose_name_plural = 'Containers'

    def __str__(self) -> str:
        return self.code
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='containers')
    code = models.CharField(max_length=128)
    client_name = models.CharField(max_length=64)
    container_type = models.ForeignKey(ContainerType, on_delete=models.SET_NULL, blank=True, null=True,related_name='containers')
    frame_range = models.JSONField(null=True, blank=True, default=dict)

    updatable_fields = ['client_name', 'frame_range', 'container_type']



class Product(TimeMixin, UpdateMixin):
    """
    Represents a product entity with versioning and metadata.

    This model tracks products identified by a combination of container, element, variant, component, layer, version, and extension.
    It automatically increments the version field when saving a new product with the same identifying fields.
    Additional attributes such as task, filepath, frame_range, description, and metadata are supported.

    Attributes:
        container (ForeignKey): Reference to the Container model.
        element (str): Name of the element.
        variant (str): Variant identifier.
        component (str): Component identifier.
        layer (str): Layer identifier.
        task (str, optional): Task name.
        filepath (str, optional): File path, must be unique.
        extension (str): File extension.
        frame_range (str, optional): Frame range information.
        version (int, optional): Version number, auto-incremented.
        description (str, optional): Description of the product.
        metadata (dict, optional): Additional metadata in JSON format.
        updatable_fields (list): Fields that can be updated.

    Meta:
        unique_together: Ensures uniqueness across container, element, variant, component, layer, version, and extension.
        verbose_name_plural: 'Products'

    Methods:
        save(*args, **kwargs): Overrides save to auto-increment version if not set.
    """
    class Meta:
        unique_together = ('container', 'element', 'variant', 'component', 'layer','version', 'extension')
        verbose_name_plural = 'Products'

    def save(self, *args, **kwargs):
        """
        Saves the Product instance to the database, automatically incrementing the version if not set or zero.

        If the instance's version is not set or is zero, this method retrieves the latest version of a Product
        with the same container, element, layer, variant, component, and extension, and sets the version to one
        higher than the latest found (or 1 if none exist). The operation is performed within an atomic transaction
        to ensure consistency.

        Args:
            *args: Variable length argument list passed to the parent save method.
            **kwargs: Arbitrary keyword arguments passed to the parent save method.

        Returns:
            None
        """
        if not self.version or self.version == 0:
            with transaction.atomic():
                latest = (
                    Product.objects
                    .select_for_update()
                    .filter(
                        container=self.container,
                        element=self.element,
                        layer=self.layer,
                        variant=self.variant,
                        component=self.component,
                        extension=self.extension
                    )
                    .order_by('-version')
                    .first()
                )
                self.version = (latest.version + 1) if latest else 1
                super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)

    container = models.ForeignKey(Container, on_delete=models.CASCADE)
    data_type = models.ForeignKey(DataType, on_delete=models.SET_NULL, null=True, blank=True)
    element = models.ForeignKey(Element, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.ForeignKey(Status, on_delete=models.SET, null=True, blank=True)
    variant = models.CharField(max_length=128)
    component = models.CharField(max_length=64)
    layer = models.CharField(max_length=128)
    task = models.CharField(max_length=64, blank=True, null=True)
    filepath = models.CharField(max_length=2048, unique=True, null=True, blank=True)
    extension = models.CharField(max_length=8)
    frame_range = models.CharField(max_length=128, blank=True, null=True)
    version = models.IntegerField(null=True, blank=True, default=0)
    description = models.TextField(null=True, blank=True)
    metadata = models.JSONField(null=True, blank=True, default=dict)
    approved_at = models.DateTimeField(null=True, blank=True, editable=False)
    approved_by = models.CharField(max_length=64, blank=True, null=True)

    updatable_fields = ['task', 'filepath', 'frame_range', 'metadata', "updated_by", 'status', 'description']


class ProductDependency(TimeMixin):
    class Meta:
        verbose_name_plural = 'Product Dependencies'
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    inputs = models.ManyToManyField(Product, related_name='%(class)s_products', blank=True)



class Bundle(TimeMixin):
    class Meta:
        unique_together = ('container','package','bundle_type','version')

    def save(self, *args, **kwargs):
        if not self.version or self.version == 0:
            with transaction.atomic():
                latest = (
                    Bundle.objects
                    .select_for_update()
                    .filter(
                        container=self.container,
                        package=self.package,
                        bundle_type=self.bundle_type,
                    )
                    .order_by('-version')
                    .first()
                )
                self.version = (latest.version + 1) if latest else 1
                super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)

    container = models.ForeignKey(Container, on_delete=models.CASCADE)
    package = models.CharField(max_length=64)
    bundle_type = models.ForeignKey(BundleType, on_delete=models.SET_NULL, null=True, blank=True)
    version = models.IntegerField(null=True, blank=True, default=0)
    description = models.TextField(null=True, blank=True)
    products = models.ManyToManyField(Product, related_name='%(class)s_products', blank=True)
