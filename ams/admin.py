from django.contrib import admin
from . models import Project, Container, Product, ContainerRelation, ProductDependency, Bundle


class ProjectAdmin(admin.ModelAdmin):
    list_display = ['id','code','label', 'modified_at', 'modified_by', 'created_at', 'created_by' ]
    list_per_page = 20

class ContainerAdmin(admin.ModelAdmin):
    list_display = ['id','code', 'client_name', 'project','modified_at']
    list_filter = ['project', 'container_type']
    search_fields = ['project__code', 'container_type__code', 'client_name', 'code']
    list_per_page = 20

class ProductAdmin(admin.ModelAdmin):
    list_display = ['id','container', 'element','step', 'data_type', 'status', 'layer', 'lod', 'version', 'filepath','modified_at']
    list_filter = ['step', 'element', 'data_type', 'status']
    search_fields = ['element__code', 'step__code', 'data_type__code', 'status__code','container__code', 'layer', 'task', 'filepath']
    list_per_page = 20

class ContainerRelationAdmin(admin.ModelAdmin):
    list_display = ['id', 'from_container','relation_type', 'get_connections']
    list_filter = ['relation_type',]
    search_fields = ['from_container__code', 'relation_type__code']
    list_per_page = 20

    def get_connections(self,obj):
        return [input.code for input in obj.to_containers.all()]
    
class ProductDependencyAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'get_connections', 'modified_at', 'created_by']
    search_fields = ['product__slug', 'product__filepath']
    list_per_page = 20

    def get_connections(self,obj):
        return [input for input in obj.dependencies.all()]
    
class BundleTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'container','bundle_type', 'version', 'get_connections', 'modified_at']
    list_filter = ['step', 'bundle_type']
    search_fields = ['step__code', 'bundle_type__code', 'container__code']
    list_per_page = 20

    def get_connections(self,obj):
        return [product for product in obj.products.all()]


admin.site.register(Project, ProjectAdmin)
admin.site.register(Container, ContainerAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ContainerRelation, ContainerRelationAdmin)
admin.site.register(ProductDependency, ProductDependencyAdmin)
admin.site.register(Bundle, BundleTypeAdmin)