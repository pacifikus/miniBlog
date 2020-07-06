from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import  generic
from .models import Blog, Blogger, BlogMessage, Comment
from .forms import NewCommentForm
from django.shortcuts import get_object_or_404
from django.urls import reverse


def index(request):
    num_blogs = Blog.objects.count()
    num_messages = BlogMessage.objects.count()
    num_bloggers = Blogger.objects.count()
    recent_posts = BlogMessage.objects.order_by('-create_date')[:3]

    return render(
        request,
        'index.html',
        context={'num_blogs': num_blogs, 'num_messages': num_messages, 'num_bloggers': num_bloggers,
                 'recent_posts': recent_posts},
    )


class BlogListView(generic.ListView):
    model = Blog
    paginate_by = 10


class BloggerList(generic.ListView):
    model = Blogger
    paginate_by = 10


class BlogDetailView(generic.DetailView):
    model = Blog


class BloggerDetailView(generic.DetailView):
    model = Blogger


class BlogMessageDetailView(generic.DetailView):
    model = BlogMessage


@login_required
def new_comment(request, blog_id, post_id):
    if request.method == 'POST':
        post = get_object_or_404(BlogMessage, pk=post_id)
        form = NewCommentForm(request.POST)
        if form.is_valid():
            author = request.user
            text = form.data['text']
            comment = Comment(author=author, text=text, blog_message=post)
            comment.save()
            return HttpResponseRedirect(reverse('message_detail', args=(blog_id, post_id)))
    else:
        form = NewCommentForm()

    return render(request, 'miniBlog/new_comment.html', {'form': form})
