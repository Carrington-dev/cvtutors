import json
from django.views.generic import ListView
from django.db.models import Q
from django.forms import formset_factory, modelformset_factory
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from braces.views import CsrfExemptMixin, JsonRequestResponseMixin
from django.urls import reverse
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from learn.forms import CourseForm, ModuleForm, ModuleFormSet
from learn.models import Content, Module
from django.views.generic.base import TemplateResponseMixin, View
from django.contrib import messages
from flexyweb import settings
from panel.models import Course
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth.decorators import login_required
import json
import datetime
import requests
import weasyprint
from django.template.loader import render_to_string
from django.contrib.admin.views.decorators import staff_member_required


class ContentOrderView(CsrfExemptMixin,
                       JsonRequestResponseMixin,
                       View):
    def post(self, request):
        for id, order in self.request_json.items():
            Content.objects.filter(id=id,
                       module__course__trainer=request.user) \
                       .update(order=order)
        return self.render_json_response({'saved': 'OK'})



class CourseCreateView(CreateView):
    model = Course
    template_name = "learn/new_course.html"
    form = CourseForm
    fields = ('name', 'motivation', 'category', 'describe', 'price','image',)

    def form_valid(self, form):
        form.instance.trainer = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return self.object.get_absolute_url()

class ModuleCreateView(TemplateResponseMixin, View):
    model = Module
    template_name = "learn/new_module.html"
    form = ModuleForm
    course = None
    fields = ('course', 'title', 'description', 'order')

    def get_formset(self, data=None):
        return ModuleFormSet(data=data)
 
    def dispatch(self, request, pk):
        self.course = get_object_or_404(Course, id=pk, trainer=request.user)
        return super().dispatch(request)
    
    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response({ 'course': self.course,'formset': formset})

    def form_valid(self, form):
        form.instance.course = self.course
        return super().form_valid(form)
    
    def get_success_url(self):
        return self.object.get_absolute_url()
    
    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect(self.course.get_absolute_url)
        return self.render_to_response({'course': self.course,'formset': formset})

    def get_context_data(self, **kwargs):
        context = super(ModuleUpdateView, self).get_context_data(**kwargs)
        form = self.get_formset()
        context['form'] = form
        return context

def module_create(request, pk):
    course = Course.objects.get(id=pk)
    template_name = "learn/new_module.html"
    form = ModuleForm()
    if request.method == "POST":
        form = ModuleForm(request.POST)
        if form.is_valid():
            p = form.save(commit=False)
            p.course = course
            p.save()
            messages.success(request, "New module added successfully.")
        else:
            messages.error(request, "Error occured.")
            
    else:
        form = form
    return render(request, template_name, {"form":form, "course":course})



class CourseUpdateView(UpdateView):
    model = Course
    form = CourseForm
    # fields = ('course', 'title', 'description', 'order')
    fields = ('name', 'motivation', 'category', 'describe', 'price','image',)
    template_name = "learn/update_course.html"
    # def form_valid(self, form):
    #     form.instance.trainer = self.request.user
    #     return super().form_valid(form)
    
    def get_success_url(self):
        return self.object.get_absolute_url()

class ModuleUpdateView(UpdateView):
    model = Module
    form = ModuleForm
    fields = ('course', 'title', 'description', 'order')
    template_name = "learn/new_course.html"
    # def form_valid(self, form):
    #     form.instance.trainer = self.request.user
    #     return super().form_valid(form)
    
    def get_success_url(self):
        return self.object.get_absolute_url()
    
    
    def get_context_data(self, **kwargs):
        context = super(ModuleUpdateView, self).get_context_data(**kwargs)

        return context

@login_required(login_url="login")
def my_courses(request):
    courses = request.user.enrolled.all()
    context = dict()
    context['courses'] = courses
    context['title'] = "My courses"
    return render(request, "learn/my_courses.html", context)

@login_required(login_url="login")
def my_likes(request):
    courses = request.user.likes.all()
    context = dict()
    context['courses'] = courses
    context['title'] = "My wishlist"
    return render(request, "learn/my_likes.html", context)


def CompleteModule(request, pk):
    
    
    module = get_object_or_404(Module, id=pk)
    course = get_object_or_404(Course, id=module.course.id)

    if module.students_completed.filter(id=request.user.id):

        module.students_completed.remove(request.user)
        messages.success(request,f"You have opted to continue with the module")
    else:
        module.students_completed.add(request.user)
        messages.success(request,f"You have successfully completed this module")
    
        
    # return redirect(course.get_absolute_url())
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def LikeCourseView(request, pk):
    course = get_object_or_404(Course, id=pk)

    if course.student_likes.filter(id=request.user.id):
        course.student_likes.remove(request.user)
        messages.warning(request,f"You have unliked this course")
    else:
        course.student_likes.add(request.user)
        messages.success(request,f"You have liked this course")
    
    # return HttpResponseRedirect(course.get_absolute_url())
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def complete_course(request, pk):
    course = Course.objects.get(pk=pk)
    all_m = course.modules.count()
    liked_m = 0
    for module in course.modules.all():
        if request.user in module.students_completed.all():
            liked_m += 1
    
    if all_m == liked_m:
        course.students_completed.add(request.user)
    else:
        messages.error(request,f"You have not completed all the modules")

    # return HttpResponseRedirect(course.get_absolute_url())
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))






def module_done(request):
    data_body = json.loads(request.body)
    module_id = data_body['module_id']
    # print(data_body)
    context = dict()
    module = get_object_or_404(Module, id=module_id)

    if module.students_completed.filter(id=request.user.id):

        module.students_completed.remove(request.user)
        messages.warning(request,f"You have opted to continue with the module")
        # context['message'] = 'You have opted to continue with the module'
    else:
        module.students_completed.add(request.user)
        # context['message'] = 'You have successfully completed this module'
        messages.success(request,f"You have successfully completed this module")
    
    return JsonResponse(context, safe=False)




@staff_member_required
def generate_certificate(request, pk):
    order = get_object_or_404(Course, id=pk)
    image = settings.STATIC_ROOT + "img/badge.svg"
    now = datetime.datetime.now()
    # print("now = ", now)
     
    html = render_to_string('certificates/certificate.html', {'course': order, 
    'logo':image, 'user':request.user, 'date':now, 'image':image})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=flexytuta_{order.id}.pdf'
    weasyprint.HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(response,
    stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + '/css/certificate.css')])
    return response


class SearchResultsListView(ListView):
    model = Course
    context_object_name = 'courses'
    template_name = 'flexyweb/courses_search.html'
    
    def get_queryset(self): # new
        query = self.request.GET.get('q')
        p = Course.objects.filter(Q(name__icontains=query))
        if p is not None:
            return p
        return []