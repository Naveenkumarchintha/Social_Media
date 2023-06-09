from django.shortcuts import render
from rest_framework import generics, permissions
from .models import User, Post, Comment
from .serializers import UserSerializer, PostSerializer, CommentSerializer
from rest_framework.response import Response
from rest_framework import status


# Create your views here.
from rest_framework import generics, permissions
from .models import User, Post, Comment
from .serializers import UserSerializer, PostSerializer, CommentSerializer

class UserListAPIView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class UserDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class PostListAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

class PostDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

class CommentListAPIView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

class CommentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
# Endpoint for searching and filtering posts
class PostSearchAPIView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        search_query = self.request.query_params.get('query')
        # Perform search/filtering based on the search_query
        queryset = Post.objects.filter(title__icontains=search_query)
        return queryset

# Endpoint for retrieving post-related information
class PostInfoAPIView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Retrieve additional information about the post
        post_info = {
            'post': PostSerializer(instance).data,
            'total_comments': instance.comments.count(),
            'total_likes': instance.likes.count(),

        }
        return Response(post_info, status=status.HTTP_200_OK)

# Endpoint for managing followers and following relationships
class FollowAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user_to_follow_id = request.data.get('user_id')
        user_to_follow = User.objects.get(id=user_to_follow_id)

        # Add logic to manage the follower and following relationships
        request.user.following.add(user_to_follow)

        return Response({'message': 'Successfully followed user.'}, status=status.HTTP_201_CREATED)
