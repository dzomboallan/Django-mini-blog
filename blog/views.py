from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from .models import BlogPost, BlogAuthor, Comments
from django.contrib.auth.models import User
from django.views import generic
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.urls import reverse

# Create your views here.
def index(request):
    return render(request, 'index.html')

class BlogListView(generic.ListView):
    model = BlogPost
    paginate_by = 5

class BlogListByAuthorView(generic.ListView):
    model = BlogPost
    paginate_by = 5
    template_name = 'blog/blog_list_by_author.html'

    def get_queryset(self):
        id = self.kwargs['pk']
        target_author = get_object_or_404(BlogAuthor, pk = id)
        return BlogPost.objects.filter(author = target_author)
    
    def get_context_data(self, **kwargs):
        """Add BlogAuthor to context so they can be displayed in the template"""
        # Call the base implementation first to get a context
        context = super(BlogListByAuthorView, self).get_context_data(**kwargs)
        # Get the blogger object from the 'pk' URL parameter and add it to the context
        context['blogger'] = get_object_or_404(BlogAuthor, pk=self.kwargs['pk'])
        return context
    
class BlogDetailView(generic.DetailView):
    model = BlogPost

class BloggerListView(generic.ListView):
    model = BlogAuthor
    paginate_by = 5

class BlogCommentCreate(LoginRequiredMixin, CreateView):
    """Form for adding a blog comment. Requires login."""
    model = Comments
    fields = ['description',]

    def get_context_data(self, **kwargs):
        """Add associated blog to form template so can display its title in HTML."""
        context = super(BlogCommentCreate, self).get_context_data(**kwargs)
        context['blog'] = get_object_or_404(BlogPost, pk = self.kwargs['pk'])
        return context
    
    def form_valid(self, form):
        """Add author and associated blog to form data before setting it as valid (so it is saved to model)"""
        # Add logged-in user as author of comment
        form.instance.author = self.request.user
        # Associate comment with blog based on passed id
        form.instance.blog = get_object_or_404(BlogPost, pk = self.kwargs['pk'])
        # Call super-class from validation behaviour
        return super(BlogCommentCreate, self).form_valid(form)
    
    def get_success_url(self):
        """After posting comment return to associated blog."""
        return reverse('blog-detail', kwargs={'pk': self.kwargs['pk'],})