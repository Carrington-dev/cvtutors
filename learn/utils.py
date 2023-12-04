from learn.models import Module
from panel.models import Course


def is_enrolled_in(request, course_id):
    course = Course.objects.get(pk=course_id)

    
    progress = 0
    if course.modules.all():
        p = 0
        all_m = course.modules.count()
        for i in course.modules.all():
            if request.user in i.students_completed.all():
                p += 1
        
        ps  = p / all_m * 100

        progress = round(ps, 2)
    return progress

def markdone_format(request, id):
    m = Module.objects.get(pk=id)
    if request.user in m.students_completed.all():
        return True    
    return False