import random
from datetime import timedelta

import redis
from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, FormView

from apps.forms import RegisterModelForm, LoginForm
from apps.models import User
from apps.tasks import send_email


class TampLateView(TemplateView):
    template_name = 'apps/home.html'


class LoginFormView(FormView):
    form_class = LoginForm
    success_url = reverse_lazy('home')
    template_name = 'auth/login.html'

    def form_valid(self, form):
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = User.objects.filter(email=email)
            if user.exists():
                user = user.first()
                if check_password(password, user.password):
                    login(self.request, user)
                    return super().form_valid(form)
            messages.error(self.request, "Email yoki parol xato!")
            return render(self.request, self.get_template_names())

class EmailView(View):
    def post(self, request):
        r = redis.Redis()
        email = request.POST.get('email')
        code = random.randrange(10 ** 5, 10 ** 6)
        send_email.delay(email, code)
        context = {"email": email}
        r.mset({email: code})
        r.expire(email, timedelta(minutes=1))
        # hash_code = make_password(str(code))
        return render(request, 'auth/verify.html', context)
        # response.set_cookie('hash', hash_code)
        # return response

    def get(self, request):
        return render(request, 'auth/register.html')


class VerifyView(View):
    def post(self, request):
        code = request.POST.get('code')
        email = request.POST.get('email')
        r = redis.Redis(decode_responses=True)
        verify_code = r.mget(email)[0]
        if verify_code == code:
            return render(request, 'auth/set-password.html', {"email": email})

class RegisterFormView(FormView):
    form_class = RegisterModelForm
    success_url = reverse_lazy('login')
    template_name = 'auth/set-password.html'

    def form_valid(self, form):
        if form.is_valid():
            form.save()
            return redirect('login')

    def form_invalid(self, form):
        pass