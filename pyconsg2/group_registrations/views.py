"""Views for the group_registrations app."""
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.utils.decorators import method_decorator
from django.views.generic import FormView
from django.shortcuts import redirect

from . import forms


class GroupRegistrationsView(FormView):
    """View that allows to add a user as part of a group registration."""
    template_name = 'group_registrations/group_registrations_view.html'
    form_class = forms.GroupRegistrationsForm

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise Http404
        return super(GroupRegistrationsView, self).dispatch(
            request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        return redirect('group_registrations')
