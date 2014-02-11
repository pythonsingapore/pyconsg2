"""Templatetags for the pyconsg2 project."""
from django import template
from django.template import Template

from classytags.arguments import Argument, MultiValueArgument
from cms.templatetags.cms_tags import Placeholder, PlaceholderOptions


register = template.Library()


@register.assignment_tag
def inspect(obj):
    import ipdb; ipdb.set_trace() # BREAKPOINT
    return obj


@register.assignment_tag(takes_context=True)
def render_template(context, template_string):
    """
    Returns the given content string as a rendered Django template.

    :param template_string: A string that follows the Django template syntax.

    """
    template = Template(template_string)
    return template.render(context)


class PlaceholderAs(Placeholder):
    name = 'placeholder_as'
    options = PlaceholderOptions(
        Argument('name', resolve=False),
        MultiValueArgument('extra_bits', required=False, resolve=False),
        'as',
        Argument('varname', resolve=False),
        blocks=[
            ('endplaceholder', 'nodelist'),
        ],
    )

    def render_tag(self, context, name, extra_bits, varname):
        output = super(PlaceholderAs, self).render_tag(
            context, name, extra_bits)
        if varname:
            context[varname] = output
            return ''
        return output
register.tag(PlaceholderAs)
