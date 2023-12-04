import markdown
from django import template
from my_auth.models import NewUser
from django.utils.safestring import mark_safe

from panel.models import Course

register = template.Library()


@register.filter(name='markdown')
def markdown(value):
    return mark_safe(markdown(value, extensions=['markdown.extensions.fenced_code']))
# def markdown_format(text):
#     return mark_safe(markdown.markdown(text))


# @register.inclusion_tag('tutors.html', takes_context=True)
# def show_tutors(context):
#     tutors = NewUser.objects.filter(is_teacher = True)[:3]
#     context['quantity'] = tutors
#     return context


@register.inclusion_tag('my_auth/tutor.html')
def show_tutors():
    tutors = NewUser.objects.filter(is_teacher=True)[:3]
    return {'tutors': tutors}


@register.inclusion_tag('my_auth/rec_courses.html')
def show_recommened_courses(course_id):
    course = Course.objects.get(id=course_id)
    courses = course.similar_courses.all()[:4]
    if not courses:
        courses = Course.objects.filter(category=course.category)[:8]
    return {'rcourses': courses}