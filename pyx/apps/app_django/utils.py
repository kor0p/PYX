from django.template import Template, Context


def render_string(string, context=None):
    return Template(string).render(Context(context))


def tag_to_view(tag):
    return lambda *a, **k: render_string(tag())
