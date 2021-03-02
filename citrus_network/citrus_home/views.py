from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
# from django.contrib.auth.models import User
from .models import CitrusAuthor, Post, Comment
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth import authenticate, login, logout
from django.http.response import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect
from http import HTTPStatus
from .profile_form import ProfileForm, ProfileFormError
from django.urls import reverse
from django.contrib.auth.models import User
import uuid
import requests
import re
from rest_framework.decorators import api_view
from django import forms
from .serializers import AuthorSerializer
from django.urls import resolve


def home_redirect(request):
    if request.method == 'GET':
        # get current user and create a post and comment
        mock_response = [
            {
                'type':"post",
                'title':"A post title about a post about web dev",
                'id':"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/764efa883dda1e11db47671c4a3bbd9e",
                'source':"http://lastplaceigotthisfrom.com/posts/yyyyy",
                'origin':"http://whereitcamefrom.com/posts/zzzzz",
                'description':"This post discusses stuff -- brief",
                'contentType':"text/plain",
                'content':"Þā wæs on burgum Bēowulf Scyldinga, lēof lēod-cyning, longe þrāge folcum gefrǣge (fæder ellor hwearf, aldor of earde), oð þæt him eft onwōc hēah Healfdene; hēold þenden lifde, gamol and gūð-rēow, glæde Scyldingas. Þǣm fēower bearn forð-gerīmed in worold wōcun, weoroda rǣswan, Heorogār and Hrōðgār and Hālga til; hȳrde ic, þat Elan cwēn Ongenþēowes wæs Heaðoscilfinges heals-gebedde. Þā wæs Hrōðgāre here-spēd gyfen, wīges weorð-mynd, þæt him his wine-māgas georne hȳrdon, oð þæt sēo geogoð gewēox, mago-driht micel. Him on mōd bearn, þæt heal-reced hātan wolde, medo-ærn micel men gewyrcean, þone yldo bearn ǣfre gefrūnon, and þǣr on innan eall gedǣlan geongum and ealdum, swylc him god sealde, būton folc-scare and feorum gumena. Þā ic wīde gefrægn weorc gebannan manigre mǣgðe geond þisne middan-geard, folc-stede frætwan. Him on fyrste gelomp ǣdre mid yldum, þæt hit wearð eal gearo, heal-ærna mǣst; scōp him Heort naman, sē þe his wordes geweald wīde hæfde. Hē bēot ne ālēh, bēagas dǣlde, sinc æt symle. Sele hlīfade hēah and horn-gēap: heaðo-wylma bād, lāðan līges; ne wæs hit lenge þā gēn þæt se ecg-hete āðum-swerian 85 æfter wæl-nīðe wæcnan scolde. Þā se ellen-gǣst earfoðlīce þrāge geþolode, sē þe in þȳstrum bād, þæt hē dōgora gehwām drēam gehȳrde hlūdne in healle; þǣr wæs hearpan swēg, swutol sang scopes. Sægde sē þe cūðe frum-sceaft fīra feorran reccan",
                # the author has an ID where by authors can be disambiguated
                'author':{
                    'type':"author",
                    'id':"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
                    'host':"http://127.0.0.1:5454/",
                    'displayName':"Lara Croft",
                    'url':"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
                    'github': "http://github.com/laracroft"
                },
                'categories':["web","tutorial"],
                'count': 1023,
                'size': 50,
                'comments':[
                    {
                        'type':"comment",
                        'author':{
                            'type':"author",
                            # ID of the Author (UUID)
                            'id':"http://127.0.0.1:5454/author/1d698d25ff008f7538453c120f581471",
                            # url to the authors information
                            'url':"http://127.0.0.1:5454/author/1d698d25ff008f7538453c120f581471",
                            'host':"http://127.0.0.1:5454/",
                            "displayName":"Greg Johnson",
                            # HATEOS url for Github API
                            'github': "http://github.com/gjohnson"
                        },
                        'comment':"Sick Olde English",
                        'contentType':"text/markdown",
                        # ISO 8601 TIMESTAMP
                        'published':"2015-03-09T13:07:04+00:00",
                        # ID of the Comment (UUID)
                        'id':"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/de305d54-75b4-431b-adb2-eb6b9e546013/comments/f6255bb01c648fe967714d52a89e8e9c",
                    }
                ],
                'published':"2015-03-09T13:07:04+00:00",
                'visibility':"PUBLIC",
                'unlisted': False,
            },
            {
                'type':"post",
                'title':"How to work on Django",
                'id':"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/764efa883dda1e11db47671c4a3bbd9e",
                'source':"http://lastplaceigotthisfrom.com/posts/yyyyy",
                'origin':"http://heroku.com/posts/aaaa",
                'description':"This post discusses stuff -- brief",
                'contentType':"text/plain",
                'content':"Þā wæs on burgum Bēowulf Scyldinga, lēof lēod-cyning, longe þrāge folcum gefrǣge (fæder ellor hwearf, aldor of earde), oð þæt him eft onwōc hēah Healfdene; hēold þenden lifde, gamol and gūð-rēow, glæde Scyldingas. Þǣm fēower bearn forð-gerīmed in worold wōcun, weoroda rǣswan, Heorogār and Hrōðgār and Hālga til; hȳrde ic, þat Elan cwēn Ongenþēowes wæs Heaðoscilfinges heals-gebedde. Þā wæs Hrōðgāre here-spēd gyfen, wīges weorð-mynd, þæt him his wine-māgas georne hȳrdon, oð þæt sēo geogoð gewēox, mago-driht micel. Him on mōd bearn, þæt heal-reced hātan wolde, medo-ærn micel men gewyrcean, þone yldo bearn ǣfre gefrūnon, and þǣr on innan eall gedǣlan geongum and ealdum, swylc him god sealde, būton folc-scare and feorum gumena. Þā ic wīde gefrægn weorc gebannan manigre mǣgðe geond þisne middan-geard, folc-stede frætwan. Him on fyrste gelomp ǣdre mid yldum, þæt hit wearð eal gearo, heal-ærna mǣst; scōp him Heort naman, sē þe his wordes geweald wīde hæfde. Hē bēot ne ālēh, bēagas dǣlde, sinc æt symle. Sele hlīfade hēah and horn-gēap: heaðo-wylma bād, lāðan līges; ne wæs hit lenge þā gēn þæt se ecg-hete āðum-swerian 85 æfter wæl-nīðe wæcnan scolde. Þā se ellen-gǣst earfoðlīce þrāge geþolode, sē þe in þȳstrum bād, þæt hē dōgora gehwām drēam gehȳrde hlūdne in healle; þǣr wæs hearpan swēg, swutol sang scopes. Sægde sē þe cūðe frum-sceaft fīra feorran reccan",
                # the author has an ID where by authors can be disambiguated
                'author':{
                    'type':"author",
                    'id':"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
                    'host':"http://127.0.0.1:5454/",
                    'displayName':"Craft Smith",
                    'url':"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
                    'github': "http://github.com/laracroft"
                },
                'categories':["web","tutorial"],
                'count': 1023,
                'size': 50,
                'comments':[
                    {
                        'type':"comment",
                        'author':{
                            'type':"author",
                            # ID of the Author (UUID)
                            'id':"http://127.0.0.1:5454/author/1d698d25ff008f7538453c120f581471",
                            # url to the authors information
                            'url':"http://127.0.0.1:5454/author/1d698d25ff008f7538453c120f581471",
                            'host':"http://127.0.0.1:5454/",
                            "displayName":"Greg Johnson",
                            # HATEOS url for Github API
                            'github': "http://github.com/gjohnson"
                        },
                        'comment':"Sick Olde English",
                        'contentType':"text/markdown",
                        # ISO 8601 TIMESTAMP
                        'published':"2015-03-09T13:07:04+00:00",
                        # ID of the Comment (UUID)
                        'id':"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/de305d54-75b4-431b-adb2-eb6b9e546013/comments/f6255bb01c648fe967714d52a89e8e9c",
                    }
                ],
                'published':"2012-03-09T13:07:04+00:00",
                'visibility':"PUBLIC",
                'unlisted': False,
            },
        ]
        
        return render(request, 'citrus_home/index.html', {'json_list': mock_response})

def login_redirect(request):
    if request.method == "POST":
        print("here")
        username = request.POST.get('username')
        password = request.POST.get('password')
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = authenticate(username=username, password=password)
            # login the current user
            login(request,user)
            # print out the ID of the current user
            print("ID: ",request.user.id)
            # logout user 
            # logout(request)
            return redirect(home_redirect)

        # if the user is not authenticated return the same html page 
        else:
            return render(request, 'citrus_home/login.html', {'form':form})

    form = AuthenticationForm()
    return render(request, 'citrus_home/login.html', {'form':form})


def register_redirect(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # creates the user object
            user = form.save()
            # login with newly created user
            username = request.POST.get('username')
            password = request.POST.get('password')
            # create CitrusAuthor
            citrusAuthor = CitrusAuthor.objects.create(type="author",id=str(uuid.uuid4()), user=user,displayName=user.username)
            citrusAuthor.save()
            # post = Post.objects.create(id="1", title="alex", description="myfirstpost", content="should work", author=citrusAuthor,commonmark=False, visibility='PVA')
            # post.save()
            return redirect(home_redirect) 
    
    # return form with user input if not valid
    else:
        form = UserCreationForm()
    return render(request, 'citrus_home/register.html', {'form': form})

"""
handles get requests with id and retrieve author profile information: username, displayname, github
handles post requests to state changes to author profile information: username, displayname, github 
Expected: POST - POST body = {"username": "new_username", "displayName": "new_displayName", "github":"new_github"} 
URL:/service/author/{AUTHOR_ID}
"""
def manage_profile(request, id):

    if request.method == 'GET':
        profile = get_object_or_404(CitrusAuthor, id=id)
        current_profile = { 'username': profile.user,
                            'displayName': profile.displayName,
                            'github': profile.github}
        form = ProfileForm(current_profile)

        return render(request, 'citrus_home/profile.html/',{'form': form, 'user': profile})
        
    # if this is a POST request we need to process the form data
    elif request.method == 'POST':
        # NEED TO SANITIZE DATA AND CHECK FOR UNCHANGED INPUT
        
        new_username = request.POST.get('username')
        new_displayName = request.POST.get('displayName')
        new_github = request.POST.get('github')

        try:
            profile = get_object_or_404(CitrusAuthor, id=id)

            # set which fields are valid/invalid for the html
            field_validities = setFormErrors(profile,new_username,new_displayName,new_github)
            pf_form_errors = ProfileFormError(field_validities[0],field_validities[1],field_validities[2])
            try:
                validate_fields(field_validities)
            except forms.ValidationError:
                #if the github, username, or display name exists and was someone elses return the users original information
                current_profile = { 'username': profile.user,'displayName': profile.displayName,'github': profile.github }
                form = ProfileForm(current_profile)

                return render(request, 'citrus_home/profile.html',{'form': form, 'user': profile, 'pf_form_errors':pf_form_errors})
            
            #if fields were valid, assign them to user
            profile.user.username = new_username
            profile.displayName = new_displayName
            profile.github = new_github
            profile.user.save()
            profile.save()

            response = JsonResponse({
                "message": "profile updated!"
            })
            response.status_code = 200
            return HttpResponseRedirect(reverse('profile',  kwargs={ 'id': str(profile.id) }))

        except (KeyError, CitrusAuthor.DoesNotExist):
            response = JsonResponse({
                "message": "couldn't update profile"
            })
            response.status_code = 418
            return response
    #not POST AND GET SO return sth else 
    else:
        response = JsonResponse({
            "message": "Method Not Allowed. Only support GET and POST"
        })

        response.status_code = 405
        return response

def setFormErrors(profile,new_username,new_displayName,new_github):
    u_valid = validate_username(profile, new_username)
    d_valid = validate_displayName(profile,new_displayName)
    g_valid = validate_github(profile,new_github)
    
    return [u_valid,d_valid,g_valid] 

def validate_fields(field_validities):
    print(field_validities)
    if False in field_validities:
        raise forms.ValidationError(u'one of three fields  are already in use.')
    else:
        return

def validate_username(profile, new_username):
    #cant query for username attributes from Citrus Author object
    if User.objects.filter(username=new_username).exists():
        existing_user = User.objects.get(username=new_username) 
        
        if  existing_user.id != profile.user.id:
            print("username is not available, someone who is not you has it")
            return False
            #raise forms.ValidationError(u'Username "%s" is already in use.' % new_username)
        else:
            print("you did not change your username - this one is already yours")
            return True
    else:
        print("username is available - no one had it yet")
        return True


def validate_displayName(profile, new_displayName):
  
    if CitrusAuthor.objects.filter(displayName=new_displayName).exists():
        existing_user = CitrusAuthor.objects.get(displayName=new_displayName)
        if existing_user.id != profile.id:
            print("display name is not available, someone who is not you has it")
            return False
            #raise forms.ValidationError(u'Display Name "%s" is already in use.' % new_displayName)
        else:
            print("you did not change your display name - this one is already yours")
            return True
    else:
        print("display name is available - no one had it yet")
        return True

def validate_github(profile,  new_github):
   
    if CitrusAuthor.objects.filter(github=new_github).exists():
        existing_user = CitrusAuthor.objects.get(github=new_github)
        if existing_user.id != profile.id:
            print("github uri is not available, someone who is not you has it")
            return False
            #raise forms.ValidationError(u'github "%s" is already in use.' % new_github)
        else:
            print("you did not change your github uri - this one is already yours")
            return True
    else:
        print("github uri is available - no one had it yet")
        return True
        
"""
retrieve github username from github url 
"""
def sanitize_git_url(git_url):
    git_username = re.sub('http://github.com/|https://github.com/|https://www.github.com/|http://www.github.com/', '', git_url)
    return git_username

"""
handles get request and list events for the github username 
Expected: 
URL:/service/author/{AUTHOR_ID}/github
reference: https://towardsdatascience.com/build-a-python-crawler-to-get-activity-stream-with-github-api-d1e9f5831d88
"""
def get_github_events(request, id):
    if request.method == 'GET':
        # look up user by their id, if not exist, return 404 response
        profile = get_object_or_404(CitrusAuthor, id=id)
        
        #sanitize github url to get github username
        git_username = sanitize_git_url(profile.github)

        response = requests.get('https://api.github.com/users/{username}/events'.format(username=git_username))

        # validate if username exists:
        if response.status_code == 404:
            err_response = JsonResponse({
                "message": "Profile not found"
            })
            err_response.status_code = 404
            return err_response

        # process data to customized json response
        data = response.json()
        results = []
        
        event_actions = {
            'WatchEvent': 'starred', 
            'PushEvent': 'pushed to', 
            'CreateEvent': "created", 
            'DeleteEvent':'deleted',
            'ForkEvent':'forked',
            'CommitCommentEvent':'committed comment on',
            'IssueCommentEvent': 'issued comment on',
            'IssueEvent': 'issued event on',
            'PullRequestEvent': 'made a pull request on',
            'PullRequestReviewEvent': 'reviewed a pull request on',
            'ReleaseEvent': 'made a realease on'
        }
        
        for event in data:
            if event['type'] in event_actions:
                name = event['actor']['display_login']
                action = event_actions[event['type']] 
                repo = event['repo']['name']
                time = event['created_at']
                action_str = {
                    'type':event['type'],
                    'name':name,
                    'action':action,
                    'repo':repo,
                    'time':time,
                }
                results.append(action_str)
            if event['type'] == 'ForkEvent':
                name = event['actor']['display_login']
                repo = event['repo']['name']  
                forked_repo = event['payload']['forkee']['full_name'] 
                time = event['created_at']
                action_str = {
                    'type':event['type'],
                    'name':name,
                    'action':action,
                    'forked_repo':forked_repo,
                    'repo':repo,
                    'time':time,
                }
                results.append(action_str)
        response = JsonResponse({'events':results})
        response.status_code = 200
        return response

"""
handle the creation of a new post object
GET Requests:
URL: ://service/author/{AUTHOR_ID}/posts/{POST_ID} will get you the post of that author with up to 5 comments
POST Requests:
URL: ://service/author/{AUTHOR_ID}/posts/{POST_ID=null} will create the post for that author.
POST Body: {
    "title": "second post",
    "description": "description of the second post -> caruso is the goat",
    "categories": "fitness, travel, compsci",
    "content": "long detailed content of the post",
    "origin": "local host:9900"
} 
PUT Requests:
URL: ://service/author/{AUTHOR_ID}/posts/{POST_ID}
PUT Body: {
    {
    "title": "goat post",
    "description": "Caruso is the goat",
    "categories": "fitness, travel, compscience",
    "content": "first post with new API",
    "origin": "local host:9900",
    "private_to_author": "True",
    "public": "False",
    "private_to_friend": "False",
    "shared_with": "alex"
}
}
DELETE Requests:
URL: ://service/author/{AUTHOR_ID}/posts/{POST_ID} -> this will delete the post with the id you provided. 
"""
# the csrf_exempt token is there if you're testing with postman
@csrf_exempt
def manage_post(request, id, **kwargs):
    pid = kwargs.get('pid')
    print(request.method)
    if request.method == "POST":
        body = json.loads(request.body)
        author = CitrusAuthor.objects.get(id=id)
        post = Post.objects.create(id=str(uuid.uuid4()), title=body['title'], description=body['description'],content=body['content'], categories=body['categories'], author=author, origin=body['origin'], visibility=body['visibility'], shared_with=body['shared_with'])
        return returnJsonResponse(specific_message="post created", status_code=200)

    
    elif request.method == 'DELETE':
        posts = Post.objects.get(id=pid)
        posts.delete()
        return returnJsonResponse(specific_message="post deleted", status_code=200)

    # update an existing post made by the user
    elif request.method == "PUT":
        # check if form is valid here
        body = json.loads(request.body)
        author = CitrusAuthor.objects.get(id=id)
        post = Post.objects.get(id=pid)
        # this code only works on posts where private to author is true. 
        # update fields of the post object
        post.title = body['title']
        post.description = body['description']
        post.content = body['content']
        post.visibility = body['visibility']
        post.shared_with = body['shared_with']
        post.save()
        
        return returnJsonResponse(specific_message="post updated", status_code=200)

 
    elif request.method == "GET":
        # potentially check if the user is authenticated
        author = CitrusAuthor.objects.get(id=id)
        posts = Post.objects.get(id=pid)
        comments = Comment.objects.filter(post=posts)
        comments_arr = create_comment_list(posts)
        author_data = convertAuthorObj(author)
        # check for post categories and put them into an array
        categories = posts.categories.split()
        return_data = {
            "type": "post",
            "title": posts.title,
            "id": posts.id,
            "source": "localhost:8000/some_random_source",
            "origin": posts.origin,
            "description": posts.description,
            "contentType": "text/plain",
            "content": posts.content,
            # probably serialize author here and call it
            "author": author_data,
            "categories": categories,
            "count": comments.count(),
            "comments": comments_arr, 
            "published": posts.created,
            "visibility": posts.visibility,
            "unlisted": "false"
        }
        return JsonResponse(return_data, status=200)
    
    else:
        return returnJsonResponse(specific_message="method not supported", status_code=400)

"""
handles GET & POST requests for comments
"""
@csrf_exempt
def handle_comment(request, id, pid):
    if request.method == "POST":
        print("inside handle comments")
        # create a comment and attach it to the post matching the provided post id
        body, post, author = setup(request, id, pid)
        Comment.objects.create(author=author, post=post, comment=body['comment'], id=uuid.uuid4()).save()
        return returnJsonResponse(specific_message="comment added", status_code=200)
    
    elif request.method == "GET":
        # check the request to see if there's a specified indices of comments requested. 
        post = Post.objects.get(id=pid)
        comment_arr = create_comment_list(post)
        return JsonResponse({
            "comments": comment_arr
        }, status=200)

    else:
        return returnJsonResponse(specific_message="method not available", status_code=400)


"""
arguments: takes in a post object and optionally a start and end index
return: a list of comments for the specified post
"""
def create_comment_list(post, **kwargs):
    # if start index and end index arguemnts provided return specified indices
    if "start_index" and "end_index" in kwargs:
        start_index = kwargs.get('start_index')
        end_index = kwargs.get('end_index')
        # get all comments associated with this post and sort by most recently published
        comments = Comment.objects.filter(post=post).order_by('-published')[start_index:end_index+1]
    else:
        comments = Comment.objects.filter(post=post).order_by('-published')[:5]
    comments_arr = []
    for comment in comments:
            # get the author of the comment
        author = CitrusAuthor.objects.get(id=comment.author.id)
        comment_data = {
            "type": "comment", 
            "author": convertAuthorObj(author),
            "comment": comment.comment,
            "contentType": "text/markdown",
            "published": comment.published,
            "id": comment.id,
        }
        comments_arr.append(comment_data)
    return comments_arr


"""
arguments: request, author id, post id
returns: returns the body of the request, the CitrusAuthor object associated with the id and the Post object associated with the pid
"""
def setup(request, id, pid):
        return json.loads(request.body), Post.objects.get(id=pid), CitrusAuthor.objects.get(id=id)


"""
arguments: message, status_code
return: custom json response
"""
def returnJsonResponse(specific_message, status_code):
    return JsonResponse({
        "message": specific_message
    }, status=status_code)


"""
arguments: CitrusAuthor object
return: dictionary with CitrusAuthor fields
"""
def convertAuthorObj(author):
        author_data = {
            "type": author.type,
            "id": author.id,
            "host": author.host,
            "displayName": author.displayName,
            "url": "somerandomUrl for now",
            "github": author.github
        }
        return author_data


"""
arguments: string that reads true or false
return: boolean value of string
"""
def stringToBool(value):
    if value == "True": 
        return True
    elif value == "False":
        return False