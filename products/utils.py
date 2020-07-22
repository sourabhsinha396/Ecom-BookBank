from django.utils.text import slugify
import random
'''
random_string_generator is located here:
http://joincfe.com/blog/random-string-generator-in-python/
'''
def random_string_generator():
    randon_integer = random.randint(2424,2899384)
    return str(randon_integer)


def unique_slug_generator(instance, new_slug=None):
    """
    This is for a Django project and it assumes your instance
    has a model with a slug field and a title character (char) field.
    """
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
                    slug=slug,
                    randstr=random_string_generator()
                )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug
