from django.urls import path
from myapp import views1

app_name = 'myapp'

urlpatterns = [
    path(r'index/', views1.index, name='index'),
    path(r'about/',views1.about,name = 'about'),
    path(r'<int:book_id>/',views1.detail, name='detail'),
    path(r'findbooks/',views1.findbooks,name='findbooks'),
    path(r'place_order/',views1.place_order,name='place_order'),
    path(r'review/',views1.review,name = 'review'),
    path(r'login/',views1.user_login,name = 'login'),
    path(r'logout/',views1.user_logout,name = 'logout'),
    path(r'register/',views1.register,name = 'register'),
    path(r'chk_reviews/<int:book_id>/',views1.chk_reviews, name='chk_reviews'),
    ]
