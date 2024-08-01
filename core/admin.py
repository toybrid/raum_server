from django.contrib import admin
from . models import ContainerType, Status, Element, DataType, Step, RelationType


class ContainerTypeAdmin(admin.ModelAdmin):
    list_display = ['id','code','label', 'modified_at']

class StatusAdmin(admin.ModelAdmin):
    list_display = ['id','code','label', 'modified_at']

class ElementAdmin(admin.ModelAdmin):
    list_display = ['id','code','label', 'modified_at']

class DataTypeAdmin(admin.ModelAdmin):
    list_display = ['id','code','label', 'modified_at']

class StepAdmin(admin.ModelAdmin):
    list_display = ['id','code','label', 'modified_at']

class RelationTypeAdmin(admin.ModelAdmin):
    list_display = ['id','code','label', 'modified_at']


admin.site.register(ContainerType, ContainerTypeAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(Element, ElementAdmin)
admin.site.register(DataType, DataTypeAdmin)
admin.site.register(Step, StepAdmin)
admin.site.register(RelationType, RelationTypeAdmin)