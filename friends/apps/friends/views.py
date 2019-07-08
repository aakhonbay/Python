from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from models import User, UserManager, Friend
import bcrypt

def index(request):

    return render(request, 'friends/index.html')

def add_user(request):
    errors = User.objects.basic_validator(request.POST)

    if errors:
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')
    else:
        hashed_password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        print hashed_password

        User.objects.create(name = request.POST['name'], alias = request.POST['alias'], email = request.POST['email'], password = hashed_password, confirm_password = hashed_password, dob = request.POST['dob'])

        request.session['name'] = request.POST ['alias']
        request.session['email']= request.POST['email']
        return redirect('/welcome')

def login(request):

    # Validate my login data
    errors = User.objects.login_validator(request.POST)
    if errors:
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')
    else:
        # log in user
        request.session['name']= User.objects.get(email=request.POST['email']).alias
        request.session['email']= request.POST['email']

        # redirect to friends page
        return redirect('/welcome')

def welcome(request):
    if 'name' not in request.session:
        return redirect('/')

    user = User.objects.get(email=request.session['email'])
    # print user.id
    request.session['id']= user.id


    all_users= User.objects.all()
    user_friends = Friend.objects.filter(user_id= user.id)
    for x in user_friends:
        all_users = all_users.exclude(id = x.friend_id)
    print len(user_friends)
    if len(user_friends) <1:
        this = "You don't have any friends yet."
    else:
        this = " "

    context ={
    "all_users" : all_users,
    "user_friends": user_friends,
    "this": this
    }

    return render(request, 'friends/friends.html', context)

def friend(request, id):
    user_id = request.session['id']

    new_friend = Friend.objects.create(user = User.objects.get(id=user_id) , friend = User.objects.get(id=id))
    print new_friend
    print id
    return redirect('/welcome')

def user(request, id):
    if 'name' not in request.session:
        return redirect('/')
    # print "x"
    info = User.objects.filter(id = id)
    # print info
    context = {
    "info":info
    }
    return render(request, 'friends/user_page.html', context)

def delete(request, id):
    # print "1"
    this = Friend.objects.filter(id = id)
    this.delete()

    print this
    return redirect('/welcome')

def logout(request):

    request.session.flush()

    return redirect('/')
