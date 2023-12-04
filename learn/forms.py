from django.forms import ModelForm, ValidationError, formset_factory, inlineformset_factory
from learn.models import Module
from panel.models import Course
from PIL import Image

class CourseForm(ModelForm):
    """Course definition."""

    # TODO: Define form fields here
    class Meta:
        fields = ('name', 'motivation', 'category', 'describe', 'price','image',)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'placeholder': 'Enter your course time'})
        self.fields['motivation'].widget.attrs.update({'placeholder': 'Enter your last name'})
        self.fields['trainer'].widget.attrs.update({'placeholder': 'Choose yourself'})
        self.fields['price'].widget.attrs.update({'placeholder': 'Enter your course price'})
        self.fields['image'].widget.attrs.update({'id': 'course_thumb'})
		
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
    

    def clean_image(self):
        image = self.cleaned_data['image']
        try:
            img = Image.open(image)
            print(img)
            if img.height < 533:
                raise ValidationError("Your image is too small")
            if img.width < 800:
                raise ValidationError("Your image is too small")
        except:
            return None
        raise ValidationError('No thumbnail uploaded for this course')

class ModuleForm(ModelForm):
    """Course definition."""

    # TODO: Define form fields here
    class Meta:
        model = Module
        # fields = ('title', 'description', 'order')
        fields = ('course', 'title', 'description', 'order')
    
    def __init__(self,   *args, **kwargs):
        # self.course = course
        super().__init__(*args, **kwargs)
        # self.fields['course'].widget.attrs.update({'placeholder': 'Enter your course time'})
        self.fields['title'].widget.attrs.update({'placeholder': 'Enter your module title'})
        self.fields['description'].widget.attrs.update({'placeholder': 'Enter your mdule description'})
        self.fields['order'].widget.attrs.update({'placeholder': 'Enter your module order'})
		
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

# ModuleFormSet = inlineformset_factory(Course, Module, fields=('course', 'title', 'description', 'order'),
#         extra=2, can_delete=True)
ModuleFormSet = formset_factory(ModelForm, extra=2)
    