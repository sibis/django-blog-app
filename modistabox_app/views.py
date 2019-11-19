from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions, status
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt

from modistabox_app.models import Blog
from datetime import datetime
from modistabox_app.serializers import BlogSerializer, BlogListsSerializer


@csrf_exempt
@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated,))
def list_blogs(request):
    try:
        blogs = BlogListsSerializer(Blog.objects.all(), many=True)
        return Response({'msg': 'Blogs retrived successfully!', 'data': blogs.data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'msg': str(e)}, status=status.HTTP_404_NOT_FOUND)


@csrf_exempt
@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated,))
def create_blog(request):
    blog_serializer = BlogSerializer(data=request.data)
    if blog_serializer.is_valid():
        blog_obj = Blog.objects.create(
            title=request.data.get('title'),
            content=request.data.get('content'),
            created_by=request.user,
            created_on=datetime.now()
        )
        return Response(blog_serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(blog_serializer._errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated,))
def update_blog(request):
    blog_serializer = BlogSerializer(data=request.data)
    if blog_serializer.is_valid():
        blog_obj = Blog.objects.get(id=request.data.get('id'))
        if blog_obj.created_by == request.user:
            blog_obj.content = request.data.get('content')
            blog_obj.title = request.data.get('title')
            blog_obj.save()
            return Response(blog_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'msg': 'User has no permission to perform this operation'
            }, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(blog_serializer._errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated,))
def view_blog(request):
    try:
        blog_id = request.data.get('id')
        blog_obj = Blog.objects.get(id=blog_id)
        blog = BlogListsSerializer(blog_obj)
        edit_allowed = 1
        if blog_obj.created_by == request.user:
            edit_allowed = 0
        return Response({
            'msg': 'Blog retrieved successfully!',
            'data': blog.data,
            'edit_allowed': edit_allowed
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'msg': str(e)}, status=status.HTTP_404_NOT_FOUND)


@csrf_exempt
@api_view(['DELETE'])
@permission_classes((permissions.IsAuthenticated,))
def delete_blog(request):
    try:
        blog_id = request.data.get('id')
        blog = Blog.objects.get(id=blog_id)
        if blog.created_by == request.user:
            blog.delete()
            return Response({'msg': 'Blog deleted successfully!'}, status=status.HTTP_200_OK)
        else:
            return Response({'msg': 'User has no permission to perform this operation'},
                            status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'msg': str(e)}, status=status.HTTP_404_NOT_FOUND)
