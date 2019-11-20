from rest_framework import serializers
from modistabox_app.models import Blog
from authentication_app.models import User


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ('title', 'content')

    def clean(self):
        super(BlogSerializer, self).clean()
        return self.cleaned_data


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name')


class BlogListsSerializer(serializers.ModelSerializer):
    created_by = UsersSerializer(required=True, allow_null=False)
    created_on = serializers.DateTimeField(format="%b %d %Y - %H:%M")

    class Meta:
        model = Blog
        fields = ('id', 'title', 'content', 'created_on', 'created_by')
        related_object = 'created_by'
