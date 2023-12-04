from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView
from learn.utils import is_enrolled_in
from my_auth.forms import *
from flexyweb import settings
from my_auth.tasks import send_verification_email
from panel.models import Course
from my_auth.models import NewUser, Profile
from my_auth.serializers import NewUserSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from django.contrib import messages
from django.core.cache import cache
from django.contrib.auth import (get_user_model, login as auth_login,
    logout as auth_logout, authenticate
)
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin


from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.core.mail import EmailMultiAlternatives
from django import template


def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = NewUser.objects.filter(Q(email=data) | Q(username=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					plaintext = template.loader.get_template(
					    'registration/password_reset_email.txt')
					htmltemp = template.loader.get_template('email/confirm.html')
					# htmltemp = template.loader.get_template('registration/password_reset_email.html')
					c = {
					"email": user.email,
					'domain': request.META['HTTP_HOST'],
					'site_name': 'FlexyTuta',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)).encode().decode(),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': request.scheme,
                    'web_link':  request.scheme + "://" + request.META['HTTP_HOST'] + "/"
					}
					text_content = plaintext.render(c)
					html_content = htmltemp.render(c)
					try:
						msg = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [
						                             user.email], headers={'Reply-To': f'{user.email}'})
						msg.attach_alternative(html_content, "text/html")
						msg.send()
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					messages.info(
					    request, "Password reset instructions have been sent to the email address entered.")
					return redirect("password_reset_done")


            # else:
                # messages.info(request, "Password reset instructions have been sent to the email address entered.")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="registration/password_reset.html", context={"password_reset_form":password_reset_form, "title":"Reset your password"})

def account_verification(request, uidb64, token):
    from django.utils.http import urlsafe_base64_decode
    user_id = urlsafe_base64_decode(uidb64)
    user_id = int(user_id)
    form = AccountVerificationForm()
    if request.method == "POST":
        form = AccountVerificationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data['is_active']
            id = form.cleaned_data['id']
            try:
                user = get_object_or_404(NewUser, pk=int(id))
                user.is_active = True
                user.save()
                #print(user, id)
                messages.success(request, "Your account has been verified successfully, log in now!")
                return redirect ("login")
            except:
                messages.error(request, "This user does not exist")
                return redirect ("register")
    return render(request=request, template_name="registration/account_verification.html", context={"form":form, "title":"Confirm your account", "user_id":user_id})

# from django.utils.decorators import  method_decorator
# @login_required(login_url="login")
# @method_decorator([login_required], name='dispatch')
# class CourseListView(ListView):
class CourseListView(LoginRequiredMixin, ListView):
    queryset = Course.objects.filter(status="published")
    model = Course
    login_url = "login"
    context_object_name = "courses"
    template_name = "flexyweb/courses.html"
    paginator = Paginator
    redirect_field_name = 'courses'
    paginate_by = 12

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context['title']  =  "Courses"
        return context
    

class ProfileListView(ListView):
    queryset = Profile.objects.filter(occupation='Approved Tutor')
    model = Profile
    context_object_name = 'profiles'
    # template_name = 'profiles.html'
    template_name = 'my_auth/profile_list.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

# def courses(request):
#     courses = Course.objects.filter(status="published")
#     # courses = Course.objects.all()
#     context = dict()
#     context['courses'] = courses
#     return render(request, "flexyweb/courses.html", context)

@login_required(login_url="login")
def course(request, year, month, day, slug, pk):
    course = Course.objects.get(id=pk)
    if request.user not in course.enrollments.all():
        return redirect('course-mk', pk=course.id)
    context = dict()
    context['course'] = course
    context['title'] = f"{ course.name } | Online Course"
    context['progress'] = is_enrolled_in(request, course.id)
    return render(request, "flexyweb/course.html", context)

@login_required(login_url="login")
def courseEnrol(request, pk):
    course = Course.objects.get(id=pk)
    if request.user in course.enrollments.all():
        return redirect('course', pk=course.id, 
        slug=course.slug, day=course.publish.day,
        year=course.publish.year, month=course.publish.month)
    context = dict()
    context['course'] = course
    context['title'] = "The Most Effective Online Tutors"
    return render(request, "flexyweb/course-mk.html", context)


def home(request):
    courses = Course.objects.all()
    context = dict()
    context["courses"] = courses 
    context['title'] = "Tutoring Company in South Africa | Private Home Tutors"
    return render(request, "flexyweb/home.html", context)

def about(request):
    context = dict()
    context['title'] = "About | Private Tutors Near You"
    return render(request, "flexyweb/about.html", context)

def verify_email_sent(request):
    return render(request, "registration/verify_email_sent.html")

def logout_view(request):
	auth_logout(request)
	messages.success(request,f"You are now logged out of your account!")
	return redirect('login')
	# return redirect('logout-success')




def signup(request):
    context = {
    "title": "Register"
    }


    if request.method == 'GET':
        cache.set('next', request.GET.get('next', None))
    request.session['next'] = request.GET.get('next', None)


    user = request.user
    if user.is_authenticated:
        return redirect("profile")

    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            raw_password = form.cleaned_data['password1']
            form.save()
            user = authenticate(email=email, password=raw_password)
            # print(account, email, raw_password)
            user = get_object_or_404(NewUser, email=email)
            if user is not None:
                auth_login(request, user)
                auth_logout(request)
                auth_login(request, user)
                user.is_active = False
                user.save()
                email = user.email
                
                send_verification_email(request, user)
                messages.success(request,f"Your registration was successful, You can now sign in to your account!")
            
                next_url = cache.get('next')
                if next_url:
                    cache.delete('next')
                    return redirect(next_url)
                next_url = request.session.get("next")
                if next_url:
                        
                    return redirect(next_url)
                else:
                    return redirect("verify_email_sent")
            else:
                pass
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
                print(error)
            context['form'] = form

    else:
        form = RegistrationForm()
        context['form'] = form
    return render(request, 'auth_files/student_register.html', context)




def tutor_register(request):
    context = {
    "title": "Join"
    }


    if request.method == 'GET':
        cache.set('next', request.GET.get('next', None))

    # print(f"Session key before loggingin {request.session.session_key}")

    user = request.user
    if user.is_authenticated:
        return redirect("profile")

    form = TutorRegistrationForm(request.POST or None)
    if request.POST:
        form = TutorRegistrationForm(request.POST)
        p_form = TutorAccRegistrationForm(request.POST, request.FILES)
        # if form.is_valid():
        if form.is_valid() and p_form.is_valid():
            p = form.save()


            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            if account is not None:
                auth_login(request, account)
                user = get_object_or_404(NewUser, email=email)
                # print(user)
                p_form = TutorAccRegistrationForm(request.POST, request.FILES, instance=request.user.profile)
                p_form.save()
                profile = Profile.objects.get(user=request.user)
                profile.occupation = "Applicant Tutor"
                profile.save()
                email = user.email
                
                send_verification_email(request, user)
                auth_logout(request)
                # auth_login(request, account)
                user.is_active = False
                user.save()
                
                """
                SEND VERIFICATION EMAIL
                """
                messages.success(request,f"Your registration was successful, You are now saved as an applicant tutor!")
                next_url = cache.get('next')
                if next_url:
                    cache.delete('next')
                    return redirect(next_url)
                else:
                    return redirect("verify_email_sent")
            else:
                pass
        else:
            # messages.error(request,f"{form.errors}")
            # print(form.errors)
            for error in list(form.errors.values()):
                messages.error(request, error)
            context['form'] = form
            context['p_form'] = p_form

    else:
        form = TutorRegistrationForm()
        p_form = TutorAccRegistrationForm()
        context['form'] = form
        context['p_form'] = p_form
    return render(request, 'auth_files/tutor_register.html', context)



# @login_required(login_url="login")
# def profile_pic(request):
#     if request.method == "POST":
#         u_form = ProfilePicUpdateForm(request.POST, request.FILES, instance=request.user.profile)
#         # p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

#         if u_form.is_valid():# and p_form.is_valid():
#             u_form.save()
#             messages.success(request,f"Your account has been updated")
#             return redirect("profile_pic")
#         else:
#             for error in list(u_form.errors.values()):
#                 messages.error(request, error)

#     else:
#         u_form = ProfilePicUpdateForm(instance=request.user.profile)
#         # p_form = ProfileUpdateForm(instance=request.user.profile)

#     context = {
#         "form": u_form,
#         # "p_form": p_form,
#         "title":"Updating",
#     }
    
	
#     return render(request,"auth_files/profile_pic.html",context)

@login_required(login_url="login")
def profile_pic(request):
    # photos = Photo.objects.all()
    if request.method == 'POST':
        form = ProfilePicUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('profile_pic')
    else:
        form = ProfilePicUpdateForm(instance=request.user.profile)
    return render(request, 'auth_files/profile_update.html', {'form': form})


@login_required(login_url="login")
def profile(request):
    if request.user.profile.occupation != "Student":
        # return render(request,"auth_files/profile.html",context)
        return redirect("tprofile")
    if request.method == "POST":
        u_form = AccountUpdateForm(request.POST, instance=request.user)
        # p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid():# and p_form.is_valid():
            u_form.save()
            messages.success(request,f"Your account has been updated")
            return redirect("profile")
        else:
            for error in list(u_form.errors.values()):
                messages.error(request, error)

    else:
        u_form = AccountUpdateForm(instance=request.user)
        # p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        "form": u_form,
        # "p_form": p_form,
        "title":"Profile",
    }
    
	
    return render(request,"auth_files/profile.html",context)

@login_required(login_url="login")
def tprofile(request):
    if request.user.profile.occupation == "Student":
        # return render(request,"auth_files/profile.html",context)
        return redirect("profile")
    if request.method == "POST":
        u_form = AccountUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request,f"Your account has been updated")
            return redirect("tprofile")
        else:
            for error in list(u_form.errors.values()):
                messages.error(request, error)
            for error in list(p_form.errors.values()):
                messages.error(request, error)

    else:
        u_form = AccountUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        "form": u_form,
        "p_form": p_form,
        "title":"Profile",
    }
    if request.user.profile.occupation == "Student":
        # return render(request,"auth_files/profile.html",context)
        return redirect("profile")
    return render(request,"auth_files/tut_profile.html",context)


class UserViewSet(viewsets.ModelViewSet):
    queryset = NewUser.objects.all()
    serializer_class = NewUserSerializer

    def list(self, request):
        serializer = NewUserSerializer(self.queryset)
        return Response(serializer.data)





def login_view(request):

    context = {
    "title": "Authenticate"
    }


    if request.method == 'GET':
        cache.set('next', request.GET.get('next', None))
	

    user = request.user
    if user.is_authenticated:
        return redirect("profile")

    if request.POST:
        form = AccountAuthenticationForm(request.POST)

        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            # print(f"Session key after loggingin {request.session.session_key}")

            # if user is not None:
            #     """Try to assign user to cart"""
               
            auth_login(request, user)
            messages.success(request,f"You are now logged in to your account!")

            next_url = cache.get('next')
            if next_url:
                cache.delete('next')
                return redirect(next_url)
            else:
                
                return redirect("profile")

        else:
            # messages.error(request, form.errors)
            messages.error(request, f"Invalid login credentials.")
            for error in list(form.errors.values()):
                messages.error(request, error)
            context['login_form'] = form

    else:
        form = AccountAuthenticationForm()

        context['login_form'] = form

    return render(request, "auth_files/login.html", context)



def form_submitted(request):
    title="Form Submitted"

    return render(request,"auth_files/form-submitted.html",{"title":title})


def logout_success(request):
    title="Logged Out"
    messages.success(request, "You are now logged out successfully!")
    return render(request,"auth_files/logout-success.html",{"title":title})