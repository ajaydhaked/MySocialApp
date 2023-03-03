from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from .forms import Dweetform
from django.contrib import messages
from .models import Dweet,Profile,User
from django.contrib.auth.forms import AuthenticationForm
from .forms import customUserCreationForm
# Create your views here.
def dashboard(request):
    if(not request.user.is_authenticated):
        return redirect("mySocialApp:Login")

    form = Dweetform(request.POST or None)
    if(request.method=="POST"):
        if(form.is_valid()):
            dweet = form.save(commit=False)
            dweet.user = request.user
            dweet.save()
            return redirect("mySocialApp:dashboard")
    followed_dweets = Dweet.objects.filter(
    user__profile__in=request.user.profile.follows.all()
    ).order_by("-created_at")
    return render(request,"mySocialApp/dashboard.html",{"form":form,"dweets":followed_dweets})
    
def profile_list(request):
    if(not request.user.is_authenticated):
        return redirect("mySocialApp:Login")
    profiles = Profile.objects.exclude(user = request.user)
    return render(request,"mySocialApp/profile_list.html",{'profiles':profiles})

def profile(request,pk):
    if(not request.user.is_authenticated):
        return redirect("mySocialApp:Login")
    if not hasattr(request.user, 'profile'):
        missing_profile = Profile(user=request.user)
        missing_profile.save()
    profile = Profile.objects.get(pk=pk)
    if(request.method=="POST"):
            current_user_profile = request.user.profile
            data = request.POST
            action = data.get("follow")
            if(action == "follow"):
                current_user_profile.follows.add(profile)
            elif(action == "unfollow"):
                current_user_profile.follows.remove(profile)
            current_user_profile.save()
    return render(request,"mySocialApp/profile.html", {"profile" : profile})


def register(request):
    if(request.method=="POST"):
        print(request.POST)
        form = customUserCreationForm(request.POST)
        if request.POST["password1"]!=request.POST["password2"]:
            messages.error(request,'both passwords should be same')
            form = customUserCreationForm
            context = {"form":form}
            return render(request,'registration/register.html',context)
        if User.objects.filter(username=request.POST['username']):
            messages.error(request,'username already exists')
            form = customUserCreationForm
            context = {"form":form}
            return render(request,'registration/register.html',context)
        if form.is_valid():
            print(form)
            user=form.save()
            login(request,user)
            messages.success(request,"Your Account has been created")
            return redirect("mySocialApp:dashboard")
        else:
            messages.error(request,"Your password cant be too similar to your other personal information.")
            messages.error(request,"Your password must contain at least 8 characters.")
            messages.error(request,"Your password cant be a commonly used password.")
            messages.error(request,"Your password cant be entirely numeric.")
            form = customUserCreationForm
    else:
        form = customUserCreationForm
    context = {'form': form}
    return render(request,'registration/register.html',context)

def LogOut(request):
    logout(request)
    return redirect("mySocialApp:dashboard")
def Login(request):
    if request.method=="POST":
        form = AuthenticationForm(request,data = request.POST)
        if form.is_valid():
            print("form valid")
            username= form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request,user)
                return redirect("mySocialApp:dashboard")
        else:
            messages.error(request,"Invalid username or password")
    return render(request,"registration/login.html")