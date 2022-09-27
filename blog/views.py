from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from blog.forms import CreatePostForm, UpdatePostForm, RegistrationForm
from blog.models import Category, Post, Profile, Comment
import pandas as pd

def index(request):
    categories = Category.objects.all()
    context = {"title": "my home page title",
               "content": "my home page content - I just changed",
               "categories": categories}
    return render(request, 'index.html', context)

def categoryDetail(request, category_id):
    category = Category.objects.get(id=category_id)
    context = {"category": category}
    return render(request, 'category.html', context)

def createCategory(request):
    category_name = request.POST.get("category_name")
    category = Category(name=category_name)
    category.save()
    return HttpResponseRedirect(reverse('home'))


def updateCategory(request):
    category_name = request.POST.get("category_name")
    category_id = request.POST.get("category_id")
    category = Category.objects.get(id=category_id)
    category.name = category_name
    category.save()
    return HttpResponseRedirect(reverse('category', args=[str(category_id)]))


def deleteCategory(request, category_id):
    category = Category.objects.get(id = category_id)
    category.delete()
    return HttpResponseRedirect(reverse('home'))


class listPosts(ListView):
    model = Post
    template_name = "post_list.html"


class detailPost(DetailView):
    model = Post
    template_name = "post_detail.html"


class createPost(CreateView):
    model = Post
    template_name = "post_create.html"
    form_class = CreatePostForm
    # fields = "__all__"


class updatePost(UpdateView):
    model = Post
    template_name = "post_update.html"
    form_class = UpdatePostForm


class deletePost(DeleteView):
    model = Post
    template_name = "post_delete.html"
    success_url = reverse_lazy("posts")


class RegistrationView(CreateView):
    model = User
    template_name = "registration/register.html"
    form_class = RegistrationForm
    success_url = reverse_lazy("login")


def CustomRegistration(request):
    if request.method  == "POST":
        username = request.POST.get("username")
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        bio = request.POST.get("bio")
        website = request.POST.get("website")
        if password1 == password2:
            user = User.objects.create_user(username=username)
            user.first_name = firstname
            user.last_name = lastname
            user.email = email
            user.set_password(password1)
            profile = Profile(user=user)
            profile.bio = bio
            profile.website = website
            profile.save()
            return HttpResponseRedirect(reverse('login'))
        else:
            return render(request, "registration_success.html", {
                "message": "Passwords are not same"
            })
    return render(request, "registration_success.html")


def file_upload(request):
    if request.method == "POST" and request.FILES["myfile"]:
        myfile = request.FILES["myfile"]
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        upload_file_url = fs.url(filename)
        excel_data = pd.read_excel(myfile)
        data = pd.DataFrame(excel_data)
        usernames = data["Username"].tolist()
        firstnames = data["First Name"].tolist()
        lastnames = data["Last Name"].tolist()
        emails = data["Email"].tolist()
        dobs = data["DOB"].tolist()
        i = 0
        while i < len(usernames):
            username = usernames[i]
            firstname = firstnames[i]
            lastname = lastnames[i]
            email = emails[i]
            dob = str(dobs[i]).split(" ")[0].replace("-", "")
            user = User.objects.create_user(username=username)
            user.first_name = firstname
            user.last_name = lastname
            user.email = email
            user.set_password(dob)
            user.groups.add(1)
            user.save()
            i = i + 1
        return render(request, 'file_upload_form.html', {'upload_file_url':upload_file_url})
    return render(request, 'file_upload_form.html')

def sendEmail(request):
    users = User.objects.all()
    if request.method == "POST":
        subject = request.POST.get("subject")
        body = request.POST.get("body")
        receiver = User.objects.get(id=request.POST.get("user"))
        senderEmail = "gabriel_sl19798@hotmail.com"
        try:
            send_mail(subject, body, senderEmail, [receiver.email], fail_silently=False)
            return render(request, "emailsending.html",{
                "message": "email sending out",
                "users": users
            })
        except:
            return render(request, "emailsending.html", {
                "message": "email sending failed",
                "users": users
            })
    return render(request, "emailsending.html", {
        "message": "",
        "users": users
    })

def likePost(request):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return HttpResponseRedirect(reverse('post-detail', args=[request.POST.get('post_id')]))

def addComment(request):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    user = get_object_or_404(User, id=request.POST.get('user_id'))
    comment_body = request.POST.get('body')
    if comment_body != "":
        comment = Comment.objects.create(post=post, user=user, body=comment_body)
        comment.save()
    return HttpResponseRedirect(reverse('post-detail', args=[request.POST.get('post_id')]))