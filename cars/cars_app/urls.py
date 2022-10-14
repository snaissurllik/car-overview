from django.urls import path, re_path
from .views import *


urlpatterns = [
    path('', CarHome.as_view(), name='home'),
    path('about/', about, name='about'),
    path('addarticle/', AddArticle.as_view(), name='addarticle'),
    path('feedback/', FeedBackView.as_view(), name='feedback'),
    path('feedbacksuccess', FeedbackSuccess.as_view(), name='feedbacksuccess'),
    path('signin/', LoginUser.as_view(), name='signin'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('logout', logout_user, name='logout'),
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    path('category/<slug:category_slug>/', CarCategory.as_view(), name='category')
]
