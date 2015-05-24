# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from models import Activities, User_Activity, lastUpdate, userTime, Comment
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.contrib.auth import authenticate, login, logout
import xmlparser
import forms
from datetime import datetime, timedelta
from django.template.loader import get_template
from django.template import RequestContext
import urllib2
from BeautifulSoup import BeautifulSoup

"""
Needed methods to process info from XML and web scrapping.
"""

# Create your views here.
@csrf_exempt
def localTime():
    return datetime.now() + timedelta(hours=2)

def getChosenActs(user):
    acts = userTime.objects.filter(user=user)
    return acts

def getStyle(user):
    try:
        styleParam = User_Activity.objects.get(user = user)
    except User_Activity.DoesNotExist:
        styleParam = User_Activity(user=user, colour='white')

    return styleParam

def getDuratrion(start, end):
    d =  end - start

    print end
    print start

    hours = d.seconds/3600
    mins = (d.seconds%3600)/60

    result = ("Duracion: "
            + str(d.days) + " dias, " 
            + str(hours) + "horas, "
            + str(mins) + "minutos ")

    print result

    return result


def longDuration(activity):
    try:
        return int(activity['duracion'])
    except KeyError:
        return 0

def getTime(activity):
    try:
        hora = activity['hora']
    except KeyError:
        hora = '00:00'

    time = datetime.strptime(activity['fecha'].split(' ')[0] 
                    + ' ' + hora , '%Y-%m-%d %H:%M')
    return time

def getPrice(activity):
    try:
        return activity['precio']
    except KeyError:
        return 'Gratuito'

def linkContent(url):
    output = ""
    try:
        content = urllib2.urlopen(url)
    except urllib2.HTTPError:
        return output

    html = content.read()

    soup = BeautifulSoup(''.join(html))
    soup.prettify()

    listDiv = soup.findAll('div', {'class': 'parrafo'})
    
    for div in listDiv:
        if div is not None:
            output += str(div)

    return output

"""
Views methods for every url on the website.
"""

def update(request):
    content = xmlparser.getNews()

    counter = 0
    for activity in content:
        counter += 1
        new_entry = Activities(id=counter,
                    title=activity['title'],
                    eventType=activity['tipo'].split("/")[3],
                    price=getPrice(activity),
                    time=getTime(activity),
                    duration=getDuratrion(getTime(activity), 
                        datetime.strptime(activity['final'].split('.')[0],'%Y-%m-%d %H:%M:%S')),
                    longDuration=longDuration(activity),
                    description=activity['url'],
                    )
        new_entry.save()

    update = lastUpdate(id=1, time=localTime())
    update.save()

    if request is not None:
        return HttpResponseRedirect("/todas")

def myLogin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            print "Logged in"
            if user.is_active:
                login(request, user)

        return HttpResponseRedirect("/")

def myLogout(request):
    if request.method == "GET":
        logout(request)
    return HttpResponseRedirect("/")

def help(request):
    if request.method == "GET":
        template = get_template("index.html")
        c = RequestContext(request, {'help': True, 'notInUser': True})

        if request.user.is_authenticated():
            c['authenticated'] = True
            c['user'] = request.user

        return HttpResponse(template.render(c))

def style(request):
    if request.method == "POST":
        if len(request.POST['title']) < 1:
                title = None
        else:
            title = request.POST['title']

        if len(request.POST['description']) < 1:
            description = None
        else:
            description = request.POST['description']

        try:
            color = request.POST['color']
        except:
            color = None

        try:
            user = User_Activity.objects.get(user=request.user)
            if title is not None:
                user.title = title
            if description is not None:
                user.description = description
            if color is not None:
                user.colour = color
        except User_Activity.DoesNotExist:
            user = User_Activity(user=user, title=title, description=description, colour=color)

        user.save()

    return HttpResponseRedirect("/" + str(request.user) + "/pg=0")

def commentAct(request, resource):
    if request.method == "POST":
        comment = request.POST['comment']

        com = Comment(user=request.user, comment=comment)

        activity = Activities.objects.get(id=int(resource))
        com.activity = activity
        com.save()

    return HttpResponseRedirect("/")

def sumScore(request, resource):
    if request.method == "GET":
        activity = Activities.objects.get(id=int(resource))
        activity.score = activity.score + 1
        activity.save()

        return HttpResponse(activity.score)


def add(request, resource):
    if request.method == "POST":
        actID = request.POST['activity']
            
        act = Activities.objects.get(id=actID)

        try:
            User.objects.get(username=resource)
            try:
                user_act = User_Activity.objects.get(user=resource)
                user_act.activity.add(act)
            except User_Activity.DoesNotExist:
                user_act = User_Activity(user=resource)
                user_act.activity_id = 0
                user_act.save()
                user_act.activity.add(act)

            try:
                userTime.objects.get(user=resource, activityID=actID)
            except userTime.DoesNotExist:
                user_time = userTime(time=localTime(), user=resource, activityID=actID)
                user_time.save()

            return HttpResponseRedirect("/")
        except User.DoesNotExist:
            return HttpResponseNotFound("You must be logged to add avtivities" +
                                        " to your personal page.")

def rss(request, resource):
    if request.method == "GET":
        try:
            template = get_template("index.rss")

            user = User.objects.get(username=resource)
            username = user.username

            try:
                user_act = User_Activity.objects.get(user=username)
                activities = user_act.activity.all()
            except User_Activity.DoesNotExist:
                activities = None

            c = RequestContext(request, {'user': resource,
                                'host': request.META['HTTP_HOST'],
                                'activities': activities})

            return HttpResponse(template.render(c))
        except User.DoesNotExist:
            return HttpResponse("The requested username does not match any user.")

def mainRss(request):
    if request.method == "GET":
        template = get_template("index.rss")

        activities = Activities.objects.order_by('time')[0:10]

        c = RequestContext(request, {"main": True,
                            'host': request.META['HTTP_HOST'],
                            'activities': activities})

        return HttpResponse(template.render(c))


def filter(request):
    if request.method == "POST":
        searchkey = request.POST['search']
        price = request.POST['price']

        activities = Activities.objects.all().filter(title__icontains=searchkey,
                                                    price=price)

        styleParam = getStyle(request.user)

        form = forms.LoginForm()
        search = forms.SearchForm()

        template = get_template("index.html")
        c = RequestContext(request, {'styleParam': styleParam,
                            'all': True,
                            'search': search,
                            'notInUser': True, 'form': form,
                            'title': ("Actividades resultantes" + 
                                    " de la busqueda: " + searchkey),
                            'activities': activities})

        update = lastUpdate.objects.get(id=1)

        if request.user.is_authenticated():
            c['authenticated'] = True
            c['user'] = request.user
            c['update'] = update.time
            c['comment'] = forms.CommentForm()

        return HttpResponse(template.render(c))

def main(request):
    if request.method == "GET":
        try:
            Activities.objects.get(pk=1)
        except Activities.DoesNotExist:
            print "Updating..."
            update(None)

        activities = Activities.objects.order_by('time')[0:10]
        users = User.objects.all()

        for user in users:
            try:
                aux = User_Activity.objects.get(user=user)
            except User_Activity.DoesNotExist:
                aux = User_Activity(user=user,
                                        title="Página de " + str(user),
                                        description="",
                                        colour="white")
                aux.save()

        styleParam = getStyle(request.user)

        styles = User_Activity.objects.all()

        form = forms.LoginForm()
        template = get_template("index.html")

        chosen = getChosenActs(request.user)

        c = RequestContext(request, {'styles': styles,
                            'styleParam': styleParam,
                            'main': True,
                            'notInUser': True, 'form': form,
                            'title': 'Próximos 10 eventos',
                            'activities': activities,
                            'chosen': chosen,
                            'title2': 'Páginas personales',
                            'users': users})

        if request.user.is_authenticated():
            c['authenticated'] = True
            c['user'] = request.user
            c['comment'] = forms.CommentForm()

        return HttpResponse(template.render(c))

def all(request):
    if request.method == "GET":
        if len(Activities.objects.all()) == 0:
            print "Updating..."
            update(None)

        activities = Activities.objects.order_by('time')

        styleParam = getStyle(request.user)

        chosen = getChosenActs(request.user)

        form = forms.LoginForm()
        search = forms.SearchForm()
        template = get_template("index.html")
        c = RequestContext(request, {'styleParam': styleParam,
                            'all': True,
                            'search': search,
                            'notInUser': True, 'form': form,
                            'title': 'Eventos en los próximos 100 días',
                            'activities': activities,
                            'chosen': chosen})

        update = lastUpdate.objects.get(id=1)

        print lastUpdate

        if request.user.is_authenticated():
            c['authenticated'] = True
            c['user'] = request.user
            c['update'] = update.time
            c['comment'] = forms.CommentForm()

        return HttpResponse(template.render(c))

def activity(request, resource):
    if request.method == "GET":
        try:
            activities = []
            activity = Activities.objects.get(id=int(resource))
            activities.append(activity)

            description = linkContent(activity.description)


            styleParam = getStyle(request.user)

            form = forms.LoginForm()
            template = get_template("index.html")
            c = RequestContext(request, {'styleParam': styleParam,
                                'inAct': True,
                                'notInUser': True, 'form': form,
                                'title': activity.title,
                                'activities': activities,
                                'description': description})
            if request.user.is_authenticated():
                c['authenticated'] = True
                c['user'] = request.user
                c['comment'] = forms.CommentForm()

            return HttpResponse(template.render(c))
        except Activities.DoesNotExist:
            return HttpResponse("Activity ID does not match any activity.")

def user(request, resource, indice):
    if request.method == "GET":
        try:
            user = User.objects.get(username=resource)
            username = user.username

            try:
                user_act = User_Activity.objects.get(user=username)
                activities = user_act.activity.all()

                group = []

                for i in range((len(activities)/10)+1):
                    start = 10*i
                    if (10 + 10*i) > len(activities):
                        end = len(activities)
                    else:
                        end = 10 + 10*i

                    group.append(activities[start:end])
                    indexes = range(len(group) + 1)

            except User_Activity.DoesNotExist:
                group = [[]]

            styles = User_Activity.objects.all()
            styleParam = getStyle(request.user)

            comments = Comment.objects.all()

            style = forms.StyleForm()
            form = forms.LoginForm()
            template = get_template("index.html")
            c = RequestContext(request, {'comments': comments,
                                'styles': styles,
                                'userPage': resource,
                                'styleParam': styleParam,
                                'style': style,
                                'form': form,
                                'title': styleParam.title,
                                'username': username,
                                'group': group[int(indice)],
                                'i': int(indice),
                                'length': len(group)-1})
            if request.user.is_authenticated():
                c['authenticated'] = True
                c['user'] = request.user
                c['comment'] = forms.CommentForm()

            return HttpResponse(template.render(c))

        except User.DoesNotExist:
            return HttpResponse("The requested username does not match any user.")
