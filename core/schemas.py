from ninja import ModelSchema
from .models import ContainerType, Status, Element, DataType, Step, RelationType, BundleType


class ContainerTypeSchema(ModelSchema):
    class Meta:
        model = ContainerType
        fields = ["id" ,"code", "label"]
        fields_optional = '__all__'

class StatusSchema(ModelSchema):
    class Meta:
        model = Status
        fields = ["id" ,"code", "label"]
        fields_optional = '__all__'

class ElementSchema(ModelSchema):
    class Meta:
        model = Element
        fields = ["id" ,"code", "label"]
        fields_optional = '__all__'

class DataTypeSchema(ModelSchema):
    class Meta:
        model = DataType
        fields = ["id" ,"code", "label"]
        fields_optional = '__all__'

class StepSchema(ModelSchema):
    class Meta:
        model = Step
        fields = ["id" ,"code", "label"]
        fields_optional = '__all__'

class RelationTypeSchema(ModelSchema):
    class Meta:
        model = RelationType
        fields = ["id" ,"code", "label"]
        fields_optional = '__all__'

class BundleTypeSchema(ModelSchema):
    class Meta:
        model = BundleType
        fields = ["id" ,"code", "label"]
        fields_optional = '__all__'