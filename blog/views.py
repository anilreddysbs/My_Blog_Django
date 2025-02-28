from django.shortcuts import render,get_object_or_404
from .models import Profile,Post,Comment,ContactMessage
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponseRedirect,HttpResponse
# Create your views here.
def logout_view(request):
    logout(request)
    return redirect('login') 
def login_page(request):
    if request.method == 'POST':
        user=request.POST.get('username')
        password=request.POST.get('password')
        user_obj=User.objects.filter(username=user)
        if not user_obj.exists():
            messages.warning(request,"Account not found")
            return HttpResponseRedirect(request.path_info)
        user_obj=authenticate(username=user,password=password)
        if user_obj:
            login(request,user_obj)
            return redirect('/')
        messages.warning(request, 'Invalid credentials')
        return HttpResponseRedirect(request.path_info)
    return render(request,'accounts/login.html')
def about(request):
    return render(request,'base/about.html')

def register(request):
    if request.method == 'POST':
        user=request.POST.get('username')
        email=request.POST.get('email')
        password1=request.POST.get('password1')
        password2=request.POST.get('password2')
        if password1!=password2:
            messages.warning(request,"Passwords do not match")
            return redirect('register')
        user_obj=User.objects.filter(username=user,email=email)
        if user_obj.exists():
            messages.warning(request,"Username is already taken")
            return redirect('register')
        user_obj=User.objects.create(email=email,username=user)
        user_obj.set_password(password1)
        user_obj.save()
        messages.success(request, "User registration successful! Please log in.")
        return redirect('login')  
    return render(request,'accounts/register.html')
@login_required
def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    profile, created = Profile.objects.get_or_create(user=user)
    posts = Post.objects.filter(author=user).order_by('-created_at')  # Fetch user's posts

    return render(request, 'accounts/profile.html', {'profile': profile, 'posts': posts})

@login_required
def edit_profile(request,username):
    user_profile = get_object_or_404(Profile, user__username=username)

    if request.user != user_profile.user:
        return redirect("profile", username=request.user.username)  # Prevent unauthorized access

    if request.method == "POST":
        bio = request.POST.get("bio")
        profile_picture = request.FILES.get("profile_picture")

        if bio:
            user_profile.bio = bio  # Update bio
        if profile_picture:
            user_profile.profile_picture = profile_picture  # Update profile picture

        user_profile.save()  # Save changes
        return redirect("profile", username=username)  # Redirect to updated profile

    return render(request, "accounts/edit_profile.html", {"profile": user_profile})

from django.core.paginator import Paginator
from django.db.models import Q

@login_required
def post_list(request):
    query = request.GET.get('q')  # Get search query from URL
    posts = Post.objects.all().order_by('-created_at')  # Get all posts (latest first)

    # Apply search filter if query exists
    if query:
        posts = posts.filter(Q(title__icontains=query) | Q(content__icontains=query))

    # Apply pagination (5 posts per page)
    paginator = Paginator(posts, 2)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "blog/post_list.html", {"page_obj": page_obj, "query": query})

@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk) 
    comments = post.comments.filter(parent__isnull=True)  # Get only parent comments

    if request.method == "POST":
        content = request.POST.get('content')
        parent_id = request.POST.get('parent_id')  # Parent comment for replies

        if content:
            parent_comment = None
            if parent_id:
                parent_comment = Comment.objects.get(id=parent_id)

            Comment.objects.create(
                post=post,
                author=request.user,
                comment_content=content,
                parent=parent_comment
            )
            return redirect('post_detail', pk=post.pk)

    return render(request, "blog/post_detail.html", {"post": post, "comments": comments})
@login_required
def post_create(request):
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        tags = request.POST.get('tags', '')  # Get tags, default to an empty string

        if title and content:
            Post.objects.create(
                title=title,
                content=content,
                author=request.user,
                tags=tags.strip()  # Remove any accidental spaces at the beginning or end
            )
            return redirect('post_list')

    return render(request, 'blog/post_create.html')


# Update an existing post manually
@login_required
def update_post(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)

    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')

        if title and content:
            post.title = title
            post.content = content
            post.save()
            return redirect('post_list')

    return render(request, 'blog/post_update.html', {'post': post})

# Delete a post manually
@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)

    if request.method == "POST":
        post.delete()
        return redirect('post_list')

    return render(request, 'blog/post_delete.html', {'post': post})
@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if request.user == comment.author:  # Ensure only the author can delete
        comment.delete()
    
    return redirect('post_detail', pk=comment.post.id)


from .form import ContactForm
@login_required
def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process form data (you can save to database or send email)
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            # Example: Save message to a model (optional)
            ContactMessage.objects.create(name=name, email=email, message=message)

            # Show a success message
            messages.success(request, "Your message has been sent successfully!")
            return redirect('contact')  # Redirect to prevent form resubmission

    else:
        form = ContactForm()

    return render(request, 'base/contact.html', {'form': form})

from django.http import JsonResponse

def like_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if request.method == "POST":
        comment.likes += 1
        comment.save()
        return JsonResponse({"likes": comment.likes, "dislikes": comment.dislikes})

def dislike_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if request.method == "POST":
        comment.dislikes += 1
        comment.save()
        return JsonResponse({"likes": comment.likes, "dislikes": comment.dislikes})
   
def posts_by_tag(request, tag_name):
    posts = Post.objects.filter(tags__icontains=tag_name)
    return render(request, "blog/post_list.html", {"page_obj": posts, "query": tag_name})




