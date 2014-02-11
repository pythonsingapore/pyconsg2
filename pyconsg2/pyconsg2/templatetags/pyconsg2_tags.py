"""Templatetags for the pyconsg2 project."""
from django import template
from django.template import Template
from django.template.defaultfilters import safe

from classytags.arguments import Argument, MultiValueArgument
from cms.templatetags.cms_tags import Placeholder, PlaceholderOptions


register = template.Library()


@register.assignment_tag
def inspect(obj):
    import ipdb; ipdb.set_trace() # BREAKPOINT
    return obj


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
        output_template = Template(safe(output))
        output_rendered = output_template.render(context)
        if varname:
            context[varname] = output_rendered
            return ''
        return output_rendered
register.tag(PlaceholderAs)
