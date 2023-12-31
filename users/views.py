from django.shortcuts import render
from django.shortcuts import render,redirect,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import auth
from django.db.models import Q
from .models import *
from .forms import *
# Create your views here.


@login_required
def main(request):
    role = Role.objects.get(id=2)
    context = {
        'student': UserGroup.objects.filter(role=role),
        'group': UserGroup.objects.filter(user=request.user),
        'user': User.objects.get(username=request.user),
    }
    return render(request, 'home/index.html',context)


@login_required
def main2(request):
    usergorup = UserGroup.objects.get(user=request.user)
    role = Role.objects.get(id=1)
    context = {
        'Teacher': UserGroup.objects.filter(role=role,group=usergorup.group),
        'user': User.objects.get(username=request.user),
    }
    return render(request, 'index2.html',context)


@login_required
def chat(request,id):
    Student = User.objects.get(id=id)
    print(id,request.user.id)
    if request.method == 'POST':
        form = Chatform(data=request.POST,files=request.FILES)
        if form.is_valid():
            chat = form.save(commit=False)
            chat.user1 = request.user
            chat.user2 = Student
            chat.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        form = Chatform()
    context = {
        'form': form,
        'user': User.objects.get(username=request.user),
        'student': Student,
        'chat': Chat.objects.raw(f"""
                 SELECT * 
                 from users_chat
                 where (user1_id={request.user.id} or user1_id={id}) and (user2_id={request.user.id} or user2_id={id})
                 ORDER by data asc
        """)
    }
    return render(request, 'home/chat.html',context)


@login_required
def chat2(request,id):
    Teacher = User.objects.get(id=id)
    chats = Chat.objects.all()
    if request.method == 'POST':
        form = Chatform(data=request.POST,files=request.FILES)
        if form.is_valid():
            chat = form.save(commit=False)
            chat.user1 = request.user
            chat.user2 = Teacher
            chat.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        form = Chatform()
    context = {
        'form': form,
        'user': User.objects.get(username=request.user),
        'Teacher': 	Teacher,
        'chat': Chat.objects.raw(f"""
                 SELECT * 
                 from users_chat
                 where (user1_id={request.user.id} or user1_id={id}) and (user2_id={request.user.id} or user2_id={id})
                 ORDER by data asc
        """)
    }
    return render(request, 'chat.html',context)


def login(request):
    if request.method == 'POST':
        form = Userloginform(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username,password=password,)
            if user and user.is_active:
                auth.login(request,user)
                if user.role == Role.objects.get(id=1):
                    if UserGroup.objects.filter(user=user).exists():
                        return redirect(reverse('main'))
                    else:
                        return redirect(reverse('register2'))
                elif user.role == Role.objects.get(id=2):
                    if UserGroup.objects.filter(user=user).exists():
                        return redirect(reverse('main2'))
                    else:
                        return redirect(reverse('register2'))
                else:
                    return redirect(reverse('login'))
    else:
        form = Userloginform()
    context = { 'form':form }
    return render(request, 'registration/login.html',context)



def register(request):
    if request.method == 'POST':
        form = Userregisterform(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('login'))
    else:
        form = Userregisterform()
    context = { 'form': form }
    return render(request, 'registration/register.html', context)


@login_required
def register2(request):
    if request.method == 'POST':
        form = UserGroupform(data=request.POST)
        if form.is_valid():
            usergroup = form.save(commit=False)
            usergroup.user = request.user
            usergroup.role = request.user.role
            usergroup.save()
            if request.user.role == Role.objects.get(id=2):
                return redirect(reverse('main2'))
            elif request.user.role == Role.objects.get(id=1):
                return redirect(reverse('main'))
            else:
                return redirect(reverse('login'))
    else:
        form = UserGroupform()
    context = {
        'form': form,
        'group': Group.objects.all()
    }
    return render(request, 'registration/register2.html', context)


def logout(request):
    auth.logout(request)
    return redirect(reverse('login'))


@login_required
def profil(request):
    if request.method == 'POST':
        form = Userprofilform(data=request.POST,files=request.FILES,instance=request.user)
        if form.is_valid():
            form.save()
            return redirect(reverse('profil'))
    else:
        form = Userprofilform(instance=request.user)
    context = {
        'form': form,
        'user': User.objects.get(username=request.user),
    }
    return render(request, 'home/user-profile.html', context)