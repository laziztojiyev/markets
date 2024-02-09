from django.conf.urls.static import static
from django.contrib.auth.views import LoginView
from django.urls import path

from apps.views import ProductListView, ProductDetailView, LogoutView, RegisterView, ForgotPasswordView, \
    UserTemplateView, WishlistView, OrderView, OrderedTemplateView
from root import settings

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('product-detail/<int:pk>', ProductDetailView.as_view(), name='product_detail'),
    path('login', LoginView.as_view(template_name='apps/auth/login.html', next_page='product_list'), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('register', RegisterView.as_view(), name='register'),
    path('forgot_password', ForgotPasswordView.as_view(), name='forgot_password'),
    path('profile', UserTemplateView.as_view(), name='user_profile'),
    path('wishlist/<int:product_id>', WishlistView.as_view(), name='wishlist_create'),
    path('order', OrderView.as_view(), name='order'),
    path('ordered',OrderedTemplateView.as_view(),name = 'ordered'),

]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL,
                                                                                        document_root=settings.MEDIA_ROOT)