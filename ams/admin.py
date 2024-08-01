from django.contrib import admin
from . models import Project, Container, Product, ContainerRelation, ProductDependency


class ProjectAdmin(admin.ModelAdmin):
    list_display = ['id','code','label', 'modified_at', 'modified_by', 'created_at', 'created_by' ]

class ContainerAdmin(admin.ModelAdmin):
    list_display = ['id','code', 'client_name', 'modified_at']

class ProductAdmin(admin.ModelAdmin):
    list_display = ['container', 'element','step', 'data_type', 'status', 'layer', 'lod', 'version', 'filepath','modified_at']

class ContainerRelationAdmin(admin.ModelAdmin):
    list_display = ['id', 'from_container','relation_type', 'get_connections']

    def get_connections(self,obj):
        return [input.code for input in obj.to_containers.all()]
    
class ProductDependencyAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'get_connections']

    def get_connections(self,obj):
        return [input for input in obj.dependencies.all()]


admin.site.register(Project, ProjectAdmin)
admin.site.register(Container, ContainerAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ContainerRelation, ContainerRelationAdmin)
admin.site.register(ProductDependency, ProductDependencyAdmin)