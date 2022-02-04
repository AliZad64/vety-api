import inspect
import uuid
from functools import partial

from django.core.validators import RegexValidator
from django.db import models, transaction
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _


from config.utils.managers import SignalsManager, SoftDeleteSignalsManager
from config.utils.utils import generate_random_code

generate_code = partial(generate_random_code, length=8)


class SingletonModel(models.Model):
    updated = models.DateTimeField(editable=False, auto_now=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super(SingletonModel, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class Entity(models.Model):
    class Meta:
        abstract = True

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(editable=False, auto_now_add=True)
    updated = models.DateTimeField(editable=False, auto_now=True)


class UUIDPrimaryKeyField(models.UUIDField):

    def __init__(self, *args, **kwargs):
        kwargs['primary_key'] = True
        kwargs['unique'] = True
        kwargs['editable'] = False
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        value = super().pre_save(model_instance, add)

        if value is None:
            value = uuid.uuid4()
            setattr(model_instance, self.attname, value)

        return value


class CharFieldDigitsOnly(models.CharField):
    default_validators = [RegexValidator(r'^([\s\d]+)$', 'Only digits characters')]


class BaseModel(models.Model):
    class Meta:
        abstract = True


class ActiveModel(models.Model):
    active = models.BooleanField(_('Active'), default=True)

    class Meta:
        abstract = True


class CodeModel(models.Model):
    code = models.CharField(
        max_length=32,
        default=generate_code,
        verbose_name=_('Model code'),
        unique=True,
    )

    class Meta:
        abstract = True



class SlugModel(BaseModel):
    slug = models.SlugField(max_length=16)

    class Meta:
        abstract = True


class TimestampedModel(BaseModel):
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('Created at')
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name=_('Updated at')
    )

    class Meta:
        abstract = True


class UUIDModel(BaseModel):
    id = UUIDPrimaryKeyField()

    class Meta:
        abstract = True

class CustomDateTimeField(models.DateTimeField):
    def value_to_string(self, obj):
        val = self.value_from_object(obj)
        if val:
            return val.strftime("%Y-%m-%d %I%p")
        return ''

