import markdown
from django import template
from my_auth.models import NewUser
from django.utils.safestring import mark_safe
from panel.models import Product, ProductFeature

register = template.Library()


@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))




@register.inclusion_tag('cart/feature.html')
def show_features(id):
    present = []
    absent = []
    product = Product.objects.get(id=id)
    # print(product.product)
    if product.product is not None:
        product_m = product.product
        features = product_m.main_features.all()
        for feat in features:
            if product in feat.is_active.all():
                present.append(feat)
            else:
                absent.append(feat)
    
    return {'present': present, 'absent': absent,}