from django.contrib import admin
from django.urls import path, include
from blog import views as b_views
from users import views as u_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('jet/', include('jet.urls', 'jet')),
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    path('admin/', admin.site.urls),
    path('', b_views.home, name='blog-home'),
    path('topics/', b_views.topics_list, name='topics-list'),
    path('~<str:title>/', b_views.genre, name='genre'),
    path('search/', b_views.search_result, name='search'),
    path('@<str:username>/', u_views.profile, name='profile'),
    path('@<str:username>/has-recommended', u_views.profile_claps, name='profile-claps'),
    path('@<str:username>/followers', u_views.user_followers, name='user-followers'),
    path('@<str:username>/following', u_views.user_following, name='user-following'),
    path('new-story/', u_views.add_story, name='add-story'),
    path('@<str:username>/<slug:slug>/edit', u_views.edit_story, name='edit-story'),
    path('@<str:username>/<slug:slug>/delete', u_views.delete_story, name='delete-story'),
    path('@<str:username>/<slug:slug>', u_views.show_story, name='show-story'),
    path('@<str:username>/<slug:slug>/report', u_views.story_report, name='story-report'),
    path('@<str:username>/<slug:slug>/responses', u_views.responses, name='responses'),
    path('@<str:username>/<slug:slug>/response/<int:id>/delete', u_views.response_delete, name='response-delete'),
    path('@<str:username>/<slug:slug>/response/<int:id>/report', u_views.response_report, name='response-report'),
    path('bookmarks/', u_views.bookmarks, name='bookmarks'),
    path('profile-edit/', u_views.profile_edit, name='profile-edit'),
    path('api/register', u_views.create_account, name='create_account'),
    path('login/', u_views.login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('follow/', u_views.profile_follow_toggle, name='follow'),
    path('api/register', u_views.create_account, name='create_account'),
    path('bookmark/', u_views.bookmark_toggle, name='bookmark'),
    path('like/', u_views.like_toggle, name='like'),
    path('response_claps/', u_views.response_claps_toggle, name='response_claps'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
