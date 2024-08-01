from django.db import models
from django.conf import settings
from account.models import User


class RaumBaseClass(models.Model):
    '''
    Base class to inherit basic properties
    '''
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='%(class)s_created_by', editable=False)
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='%(class)s_modified_by', editable=False)
    active = models.BooleanField(default=True)
    # objects = models.Manager()