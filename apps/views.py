from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, TemplateView, FormView, DetailView, UpdateView

from apps.forms import UserRegistrationForm, OrderModelForm, UserSettingsForm
from apps.models import Product, User, ProductImage, WishList
from apps.tasks import send_to_email


class CategoryTemplateView(TemplateView):
    template_name = 'apps/base.html'


class ProductListView(ListView):
    paginate_by = 9
    model = Product
    queryset = Product.objects.order_by('-id')
    template_name = 'apps/product/product_grid.html'
    context_object_name = 'product_list'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'apps/product/product_detail.html'

class ProductImageView(TemplateView):
    model = ProductImage
    template_name = 'apps/product/product_detail.html'
    context_object_name = 'product_image'


# class LoginFormView(FormView):
#     model = User
#     template_name = 'apps/auth/login.html'
#     context_object_name = 'login'
#     form_class = LoginAuthenticationForm
#
#     def form_valid(self, form):
#         email = form.data['email']
#         password = form.data['password']
#         user = authenticate(self.request, email=email, password=password)
#         if user:
#             login(self.request, user)
#             return redirect('product_list')
#         return super().form_valid(form)


class LogoutView(ListView):
    model = User
    template_name = 'apps/auth/logout.html'
    context_object_name = 'logout'


class RegisterView(FormView):
    form_class = UserRegistrationForm
    template_name = 'apps/auth/register.html'
    success_url = '/'

    def form_valid(self, form):
        form.save()
        send_to_email.delay([form.data.get('email')], form.data.get('first_name'))
        return super().form_valid(form)


class ForgotPasswordView(TemplateView):
    template_name = 'apps/auth/forgot_password.html'


class ProductResourceView(ListView):
    pass


class UserTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'apps/auth/profile.html'


class WishlistView(View):

    def get(self, request, *args, **kwargs):
        product_id = kwargs['product_id']
        wishlist, created = WishList.objects.get_or_create(user=request.user, product_id=product_id)
        if not created:
            wishlist.delete()
        return redirect('/')


class OrderView(FormView):
    form_class = OrderModelForm
    template_name = 'apps/product/product_detail.html'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return redirect(reverse('product_detail', kwargs={'pk': self.request.POST.get('product_id')}))

    def get_success_url(self):
        return reverse('product_detail', kwargs={'pk': self.request.POST.get('product')})


class OrderedTemplateView(TemplateView):
    template_name = 'apps/product/ordered.html'


class ErrorPage404View(TemplateView):
    template_name = 'apps/errors/error_404.html'


class ErrorPage500View(TemplateView):
    template_name = 'apps/errors/error_500.html'


class UserUpdateView(UpdateView):
    form_class = UserSettingsForm
    template_name = 'apps/auth/profile.html'
    success_url = reverse_lazy('login')

    def get_object(self, queryset=None):
        return self.request.user

    def form_invalid(self, form):
        return super().form_invalid(form)


class ChangePasswordView(PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = 'apps/auth/profile.html'
    success_url = reverse_lazy('login')

    def form_invalid(self, form):
        return super().form_invalid(form)
