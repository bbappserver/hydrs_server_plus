from django.db import models
from django.contrib.auth import models
from urls.models import URLVote
# Create your models here.

class Filetype(models.Model):
    MIME = models.CharField(max_length=64)
    UTI= models.CharField(max_length=64,null=True,blank=True)

    def __str__(self):
        return self.MIME

class FileIdentity(models.Model):
    sha256=models.BinaryField(null=True,blank=True,unique=True)
    size=models.PositiveIntegerField(null=True,blank=True)
    filetype = models.ForeignKey("Filetype",on_delete=models.PROTECT,null=True,blank=True,related_name='+')

    def url_counts(self):
        return URLVote.objects.filter(file_identity=self).values(('url')).annotate(count=models.Count('url'))
    def deletion_counts(self):
        return DeletionVote.objects.filter(file_identity=self).values(('deletion_type')).annotate(count=models.Count('deletion_type'))

class DeletionVote(models.Model):
    DELETION_UNSPECIFIED='?'
    DELETION_INAPPROPRIATE='i'
    DELETION_DISLIKE='d'

    DELETION_TYPE_CHOICES=(
        (DELETION_UNSPECIFIED,'Unspecified'),
        (DELETION_INAPPROPRIATE,'Inappropriate for this client'),
        (DELETION_DISLIKE,'I Don\'t like it')
    )
    file_identity= models.ForeignKey("FileIdentity",on_delete=models.PROTECT,related_name='+')
    user= models.ForeignKey("auth.User",on_delete=models.CASCADE,related_name='deletion_votes')
    deletion_type=models.CharField(max_length=1,choices=DELETION_TYPE_CHOICES)

    class Meta:
        unique_together=(('file_identity','user'))


class Collection(models.Model):
    unordered_members= models.ManyToManyField("FileIdentity",blank=True)
    parents = models.ManyToManyField("self",blank=True,related_name="children")

class OrderedCollectionMembers(models.Model):
    file_identity= models.ForeignKey("FileIdentity",on_delete=models.CASCADE,related_name='+')
    collection= models.ForeignKey("Collection",on_delete=models.CASCADE,related_name="ordered_members")
    ordinal= models.PositiveSmallIntegerField()