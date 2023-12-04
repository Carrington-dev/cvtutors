import markdown
from django import template
from learn.models import Module
from my_auth.models import NewUser
from django.utils.safestring import mark_safe

from panel.models import Course

register = template.Library()

@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))

@register.inclusion_tag('learn/is_enrolled.html', takes_context=True)
def is_enrolled_in(context, course_id):
    request = context['request']
    course = Course.objects.get(pk=course_id)
    is_enrolled = False
    if request.user in course.enrollments.all():
        is_enrolled = True
    
    progress = 0
    if course.modules.all():
        p = 0
        all_m = course.modules.count()
        for i in course.modules.all():
            if request.user in i.students_completed.all():
                p += 1
        
        ps  = p / all_m * 100

        progress = round(ps, 2)
    
    return {'is_enrolled': is_enrolled, "course":course, "progress": progress}


@register.inclusion_tag('learn/done_icons.html', takes_context=True)
def is_module_done(context, id):
    request = context['request']
    m = Module.objects.get(pk=id)
    is_enrolled = False
    if request.user in m.students_completed.all():
        is_enrolled = True    
    return {'is_enrolled': is_enrolled, 'module': m}

@register.inclusion_tag('learn/done_buttons.html', takes_context=True)
def is_module_done_btn(context, id):
    request = context['request']
    m = Module.objects.get(pk=id)
    is_enrolled = False
    if request.user in m.students_completed.all():
        is_enrolled = True    
    return {'is_enrolled': is_enrolled}
