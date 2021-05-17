from .models import insta
from django.shortcuts import render
import pandas
from instaloader import Profile, Instaloader
import re
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, JsonResponse


# Create your views here.

def fun():
    print('In fun function')
    l = Instaloader()
    l.login("username", "Password")
    df = pandas.read_csv(r'C:\Users\ajain\Downloads\Instagram.csv')
    st = ''' Andhra Pradesh|Arunachal Pradesh|Assam|Bihar|Karnataka|Kerala|Chhattisgarh|Uttar Pradesh|Goa|Gujarat|Haryana
                  |Maharashtra|Manipur|Meghalaya|Mizoram|Nagaland|Orissa||Punjab|Rajasthan||Sikkim||Tamil Nadu||Telangana|Tripura|Uttarakhand
                  |Himachal Pradesh|Jammu and Kashmir|Jharkhand|West Bengal|Madhya Pradesh '''
    for i in df['Instagram URL']:
        try:
            profile = Profile.from_username(l.context, i[26:].replace('/', ""))
        except:
            continue
        follower = profile.followers
        followee = profile.followees
        name = profile.full_name
        category = profile.business_category_name
        Bio = profile.biography
        s = profile.biography.split('\n')
        for j in s:
            m = re.match(st, j, re.IGNORECASE)
            if m:
                city = m.group()
                break
            else:
                city = ''
        for j in s:
            if re.match('^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$', j):
                contact = j
                break
            else:
                contact = ''
        print(city, contact, i)
        s = insta(follower=follower, followee=followee, name=name, category=category, Bio=Bio, city=city,
                  contact=contact)
        s.save()


def sign_up(request):
    if request.method == 'POST':
        fm = UserCreationForm(request.POST)
        if fm.is_valid():
            fm.save()
            return HttpResponseRedirect('/login/')
    else:
        fm = UserCreationForm()
    return render(request, 'pro_insta/signup.html', {'form': fm})


def user_login(request):
    if request.method == 'POST':
        fm = AuthenticationForm(request=request, data=request.POST)
        if fm.is_valid():
            uname = fm.cleaned_data['username']
            pas = fm.cleaned_data['password']
            user = authenticate(username=uname, password=pas)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
    else:
        fm = AuthenticationForm()
    return render(request, 'pro_insta/login.html', {'forms': fm})


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/login/')


def retrieve_data(request, follower_count, following_count, category):
    print(follower_count)
    print(following_count)
    emails = insta.objects.all().filter(
        follower__range=[0, follower_count], followee__range=[0, follower_count], category=category)

    print(emails)

    return JsonResponse([email.serialize() for email in emails], safe=False)


def index(request):
    if request.user.is_authenticated:

        categories = insta.objects.values('category').distinct()
        for category in categories:
            print(category)

        return render(request, 'pro_insta/index.html', {'categories': categories})
    else:
        return HttpResponseRedirect('/login/')
