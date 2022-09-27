from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from blog.views import index, categoryDetail, createCategory, updateCategory, deleteCategory, listPosts, detailPost, \
    createPost, updatePost, deletePost, file_upload, sendEmail, likePost, addComment

urlpatterns = [
    path("", index, name="home"),
    path("category/<int:category_id>/detail", categoryDetail, name="category"),
    path("category/create", createCategory, name="create-category"),
    path("category/update", updateCategory, name="update-category"),
    path("category/<int:category_id>/delete", deleteCategory, name="delete-category"),
    path("posts/", listPosts.as_view(), name="posts"),
    path("posts/<int:pk>/detail", detailPost.as_view(), name="post-detail"),
    path("post/create", createPost.as_view(), name="post-create"),
    path("post/<int:pk>/update", updatePost.as_view(), name="post-update"),
    path("post/<int:pk>/delete", deletePost.as_view(), name="post-delete"),
    path("file_upload", file_upload, name="file_upload"),
    path("send_email", sendEmail, name="send_email"),
    path("likepost", likePost, name="like_post"),
    path("add_comment", addComment, name="add_comment"),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
