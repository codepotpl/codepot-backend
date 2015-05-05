from django.template import Context
from django.template.loader import get_template

def get_rendered_template(tmpl_name, tmpl_ctx={}):
    return (get_template(tmpl_name)).render(Context(tmpl_ctx))