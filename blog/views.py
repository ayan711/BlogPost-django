from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from .models import Post
from django.contrib.auth.models import User
from django.urls import reverse
# similar to login_required decorator used for class view 
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
# importing class based views
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

posts = [
    {
        'author': 'Ayan',
        'title': 'Post 1',
        'content': 'Greetings of the day !!!',
        'date_posted': 'August 27, 2020'
    },
    {
        'author': 'Mane Dean',
        'title': 'Life ....',
        'content': 'Its a big thing to talk about',
        'date_posted': 'Jan 8, 2021'
    }
]



# Create your views here.

def home(request):

    # context={'post':posts} # static posts

    context={'post': Post.objects.all()}

    return render(request,'blog/home.html',context=context) 
    # return HttpResponse('<h1> Welcome to Blog </h1>')

def about(request):

    return render(request,'blog/about.html',{'title':'About'}) 
    # return HttpResponse('<h1> About - Blog </h1>')

class PostListView(ListView):
    """ Class based view of ListView type to list all the posts present. """
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'post'
    ordering = ['-date_posted']

    ## Adding pagination functionality by defining this attr
    paginate_by=3

    # This function can be used to search blogs with specific name
    # def get_queryset(self):
    #     return Post.objects.filter(title__icontains='on')[:5]


class UserPostListView(ListView):
    """
        Returns User based post lists via pagination
    """
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html

    ## variable which can be used in template to access attributesv
    context_object_name = 'posts'
    paginate_by = 5


    def get_queryset(self):
        """
        Over-riding querset method responsible for returning list of data.
        We are doing this because we will have dynamic query to be build via the username to be passed in the url.
        So we user ## "kwargs" ## argument to fetch the name and get the list of results.
        Also order_by attribute will be linked to the query.

        """
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model=Post

    ## over ride the internal working to pass customized error handling of in-correct post id

class PostCreateView(LoginRequiredMixin,CreateView):

    ## This method looks for template of  model_form.html to load form

    """
     This will provide an in built form to create entry

     params : 
        1) LoginRequiredMixin - Forcing login to access this view
        2) CreateView - Inheriting CreateView class
    """
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        """ Over riding base form_valid method as user id is manadatory for form creation 
        so we are setting up the form value first with user id and then passing it to base/super form_valid method """
        form.instance.author = self.request.user
        return super().form_valid(form)

    # def get_success_url(self):
    #     """
    #     This is used for redirect after successful post action.
    #     If after successful post request you want to re-direct
    #     to a page which does not contain dynamic url you can use this method 
    # 
    #     """
    #     return reverse('blog-home')#, kwargs={'pk': self.object.pk})


class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    ## This method looks for template of  model_form.html to load form

    """
     This will provide an in built form to create entry

     params : 
        1) LoginRequiredMixin - Forcing login to access this view
        2) CreateView - Inheriting CreateView class
        3) UserPassesTestMixin - For checking if the post belongs to him
    """
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        """ Over riding base form_valid method as user id is manadatory for form creation 
        so we are setting up the form value first with user id and then passing it to base/super form_valid method """
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        """
        This method consist of condition  in which user should be able to perform the 
        mentioned task of view.

        Here we check if user id is same as post's author id.

        """
        # getting the current object accessed by the view
        post=self.get_object()

        ## Check if the post user id is same as login id to ensure if the creator of post is able to modify the posts
        if self.request.user == post.author:
            return True
        return False



class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    ## This method looks for template of  model_form.html to load form

    """
     Post Deletion
     This expects template of name < model_confirm_detail.html > since its regarding content deletion
    """
    model = Post
    ## for re direction post deletion
    success_url= '/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        """
        This function is required to be over-rided from UserPassesTestMixin class

        """
        # getting the current object accessed by the view
        post=self.get_object()


        if self.request.user == post.author:
            return True
        return False

