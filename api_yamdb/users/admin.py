from six import with_metaclass

from django.contrib import admin
from django.db import models

from .models import User

def getter_for_related_field(name, admin_order_field=None, short_description=None):
    related_names = name.split('__')
    def getter(self, obj):
        for related_name in related_names:
            obj = getattr(obj, related_name)
        return obj
    getter.admin_order_field = admin_order_field or name
    getter.short_description = short_description or related_names[-1].title().replace('_',' ')
    return getter


class RelatedFieldAdminMetaclass(type(admin.ModelAdmin)):
    def __new__(cls, name, bases, attrs):
        new_class = super(RelatedFieldAdminMetaclass, cls).__new__(cls, name, bases, attrs)
        for field in new_class.list_display:
            if '__' in field:
                setattr(new_class, field, getter_for_related_field(field))
        return new_class


class RelatedFieldAdmin(with_metaclass(RelatedFieldAdminMetaclass, admin.ModelAdmin)):
    def get_queryset(self, request):
        qs = super(RelatedFieldAdmin, self).get_queryset(request)
        select_related = [field.rsplit('__',1)[0] for field in self.list_display if '__' in field]
        model = qs.model
        for field_name in self.list_display:
            try:
                field = model._meta.get_field(field_name)
            except models.FieldDoesNotExist:
                continue
            if isinstance(field, models.ManyToOneRel):
                select_related.append(field_name)
        return qs.select_related(*select_related)


@admin.register(User)
class UserInfoAdmin(RelatedFieldAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'email', 'bio', 'role')
    list_display_links = list_display
    list_filter = ('role', )
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'user__email', 'role')
