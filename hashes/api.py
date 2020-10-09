from rest_framework import serializers,viewsets,status,response,views
from django.db import transaction
from .models import FileIdentity,DeletionVote
from urls.models import URLVote
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

class VotesViewSet (viewsets.ViewSet):
    permission_classes = [IsAuthenticated,ModeratorApproved]

    @action(detail=False, methods=['post'])
    def upvote(self,request):
        user=request.user
        data =request.data

        sha2_hashes=[]
        sha2_hashes=(bytes.fromhex(x) for x in sha2_hashes)
        urls=[]
        deletions=[]

        with transaction.atomic():
            for h in sha2_hashes:
                created,fid=FileIdentity.objects.get_or_create(sha256=h)

                for d in deletions:
                    try:
                        dv= DeletionVote(file_identity=fid,deletion_type=d.deletion_type,user=user)
                        dv.save()
                    except IntegrityError as e: 
                        if 'unique constraint' in e.message: # or e.args[0] from Django 1.10
                            #partial failure due to duplicate vote
                            raise NotImplementedError()
                for u in urls:
                    try:
                        dv= URLVote(file_identity=fid,url__url=u,user=user)
                        dv.save()
                    except IntegrityError as e: 
                        if 'unique constraint' in e.message: # or e.args[0] from Django 1.10
                            #partial failure due to duplicate vote
                            raise NotImplementedError()
        #THis can be partial depending on whether you are ellegible to cast votes you have already cast
        #Return different status code on failure?
        return views.Response(status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'])
    def unvote(self,request):
        user=request.user
        data =request.data

        sha2_hashes=[]
        sha2_hashes=(bytes.fromhex(x) for x in sha2_hashes)
        urls=[]
        deletions=[]

        with transaction.atomic():
            for h in sha2_hashes:
                created,fid=FileIdentity.objects.get_or_create(sha256=h)
                for d in deletions:
                    dv= DeletionVote(file_identity=fid,deletion_type=d.deletion_type,user=user)
                    dv.delete()
                for u in urls:
                    dv= URLVote(file_identity=fid,url__url=u,user=user)
                    dv.delete()
            return views.Response(status=status.HTTP_200_OK)
        
        #Something aout the requested deletions failed possibly asking to delete a missing something
        return views.Response(status=status.HTTP_412_PRECONDITION_FAILED)


    @action(detail=False, methods=['get'])
    def url_counts(self,request):
        data=request.data
        l=FileIdentity.get(**data).url_counts()
        l=list(l)
        return views.Response(l,status=status.HTTP_200_OK)
        raise NotImplementedError()

    @action(detail=False, methods=['get'])
    def deletion_counts(self,request):
        data=request.data
        l=FileIdentity.get(**data).deletion_counts()
        l=list(l)
        return views.Response(l,satus=status.HTTP_200_OK)
        raise NotImplementedError()
            