from learn.models import Module


def all_modules(request):
    if request.user.is_authenticated:
        return {'all_modules':request.user.modules_completed.all()}
    # else:
    return {'all_modules':[]}