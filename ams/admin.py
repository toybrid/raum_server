from django.contrib import admin
from .models import Project, ContainerType, Status, Element, DataType, BundleType, Container, Product, Bundle, ProductDependency

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("id", "code", "label", "client_name", "updated_at", "created_at", "created_by", "updated_by")
    search_fields = ("code", "client_name")
    ordering = ("code",)

@admin.register(ContainerType)
class ContainerTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "code", "label", "updated_at", "created_at", "created_by", "updated_by")
    search_fields = ("code", "label")
    ordering = ("code",)

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ("id", "code", "label", "updated_at", "created_at", "created_by", "updated_by")
    search_fields = ("code", "label")
    ordering = ("code",)

@admin.register(Element)
class ElementAdmin(admin.ModelAdmin):
    list_display = ("id", "code", "label", "updated_at", "created_at", "created_by", "updated_by")
    search_fields = ("code", "label")
    ordering = ("code",)

@admin.register(DataType)
class DataTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "code", "label", "updated_at", "created_at", "created_by", "updated_by")
    search_fields = ("code", "label")
    ordering = ("code",)

@admin.register(BundleType)
class BundleTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "code", "label", "updated_at", "created_at", "created_by", "updated_by")
    search_fields = ("code", "label")
    ordering = ("code",)

@admin.register(Container)
class ContainerAdmin(admin.ModelAdmin):
    list_display = ("id", "code", "container_type", "updated_at", "created_at", "created_by", "updated_by")
    search_fields = ("code", "container_type__code")
    list_filter = ("container_type", 'project__code')
    ordering = ("code",)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id", "container", "element", "variant", "component", "layer", "filepath","version", "status", 
        "approved_at", "approved_by", "updated_at", "created_at", "created_by", "updated_by"
        )
    search_fields = ("element__code", "variant", "component", "layer", "filepath")
    list_filter = ("element", "status")
    ordering = ("element",)


@admin.register(Bundle)
class BundleAdmin(admin.ModelAdmin):
    list_display = (
        "id", "container","package","bundle_type", "version", "description", 
        "updated_at", "created_at", "created_by", "updated_by"
        )
    search_fields = ("bundle_type__code", "bundle_type__label")
    list_filter = ("bundle_type",)
    ordering = ("bundle_type__code",)


@admin.register(ProductDependency)
class ProductDependencyAdmin(admin.ModelAdmin):
    list_display = ("id", "product")
    search_fields = ("id",)

# Register your models here.
admin.site.site_header = "RAUM Admin Portal"
admin.site.site_title = "RAUM Admin Portal"
admin.site.index_title = "Welcome to RAUM Admin Portal"
admin.site.empty_value_display = '-empty-'