from django.db import models

# Create your models here.

class URL(models.Model):
    url= models.URLField(max_length=2000)

class URLVote(models.Model):
    user= models.ForeignKey("auth.User",on_delete=models.CASCADE,related_name='url_votes')
    file_identity= models.ForeignKey("hashes.FileIdentity",on_delete=models.PROTECT,related_name='URL_votes')
    url= models.ForeignKey("URL",on_delete=models.PROTECT,related_name='url_votes')
    
    class Meta:
        unique_together=(('url','file_identity','user'))
