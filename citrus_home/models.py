from django.db import models
import uuid
from django.contrib.auth.models import User
from django.core.validators import int_list_validator


class CitrusAuthor(models.Model):
    type            = models.CharField(max_length=100, default="Author")
    id              = models.CharField(max_length=50,primary_key=True)
    user            = models.OneToOneField(User, on_delete=models.CASCADE)
    host            = models.CharField(max_length=200, default="http://localhost:8000/")
    displayName     = models.CharField(max_length=300, default=f"{str(user)}")
    github          = models.CharField(max_length=300, default="", null=True)
    url             = models.CharField(max_length=300, default="http://localhost:8000/", null=True)
    profile_picture = models.ImageField(null=True, blank=True, upload_to="images/")



"""
each post has a unqiue
title, id, author, description, content, categories
common_mark = markdown
posts have different types: public, shared to friends, private to author, private to friends
"""
class Post(models.Model):
    id                  = models.CharField(max_length=50, primary_key=True)
    title               = models.CharField(max_length=200)
    description         = models.CharField(max_length=300)
    content             = models.CharField(max_length=400)
    author              = models.ForeignKey(CitrusAuthor, on_delete=models.CASCADE)
    origin              = models.CharField(max_length=300)
    commonmark          = models.BooleanField(default=False)
    # image           = models.ImageField()
    # parse this and return as list for GET request
    categories          = models.CharField(max_length=400)
    # if visibility option is not provided the default will be public
    visibility_choices  = [
        ("PUBLIC", "public"),
        ("PRIVATE_TO_AUTHOR", "private to author"),
        ("PRIVATE_TO_FRIEND", "private to friends")
    ]
    visibility          = models.CharField(max_length=50, choices=visibility_choices, default="PUBLIC")
    # if private to author or private to friends is true add usernames to shared_with
    shared_with         = models.CharField(max_length=600)
    created             = models.DateTimeField(auto_now_add=True)



"""
a comment will belong to an author and also be associated with one post
"""
class Comment(models.Model):
    author          = models.ForeignKey(CitrusAuthor, on_delete=models.CASCADE)
    post            = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment         = models.CharField(max_length=400)
    published       = models.DateTimeField(auto_now_add=True)
    id              = models.CharField(max_length=500, primary_key=True)



# https://stackoverflow.com/questions/1429293/storing-an-integer-array-in-a-django-database
class Friend(models.Model):
    uuid              = models.ForeignKey(CitrusAuthor, on_delete=models.CASCADE)
    friends_uuid    = models.TextField(validators=[int_list_validator])

class Follower(models.Model):
    uuid              = models.ForeignKey(CitrusAuthor, on_delete=models.CASCADE)
    followers_uuid  = models.TextField(validators=[int_list_validator])

class Node(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # add a node with URL
    host = models.URLField(primary_key=True)
    # if the host has been accepted
    is_verified = models.BooleanField(default=False)
    # for Basic Auth TODO later
    node_username = models.CharField(max_length=100)
    node_password = models.CharField(max_length=100)