from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


# Create your models here.

class TagItemManager(models.Manager):
    def get_tag_for(self, obj_type, obj_id):
        content_type = ContentType.objects.get_for_model(obj_type)

        return TagItem.objects.select_related('tag').filter(content_type=content_type, object_id=obj_id)


class Tag(models.Model):
    label = models.CharField(max_length=255)

    def __str__(self):
        return self.label


class TagItem(models.Model):
    objects = TagItemManager()

    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    # Type (product, video, article)
    # ID
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
