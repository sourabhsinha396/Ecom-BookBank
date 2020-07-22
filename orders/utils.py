from django.utils.text import slugify
import random
'''
random_string_generator is located here:
http://joincfe.com/blog/random-string-generator-in-python/
'''
def random_string_generator():
    randon_integer = random.randint(2424,2899384)
    return str(randon_integer)


def unique_slug_generator(instance):
    """
    This is for a Django project for order id
    """
    order_new_id = random_string_generator().upper()

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(order_id = order_new_id).exists()
    if qs_exists:
        return unique_slug_generator(instance)
    return order_new_id
