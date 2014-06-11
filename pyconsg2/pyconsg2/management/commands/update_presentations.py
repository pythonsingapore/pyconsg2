"""
Custom admin command that updates presentations based on their proposals.

This is necessary because when a speaker makes changes to a proposal, they
are not automatically copied into the presentation.

"""
from django.core.management.base import BaseCommand
from symposion.schedule.models import Presentation


class Command(BaseCommand):
    help = 'Copies changes from proposal into presentation.'

    def handle(self, *args, **options):
        found_any_change = False
        for presentation in Presentation.objects.all():
            found_change = False
            proposal = presentation.proposal_base
            if presentation.title <> proposal.title:
                found_change = True
                presentation.title = proposal.title
            if presentation.description.raw <> proposal.description:
                found_change = True
                presentation.description = proposal.description
            if presentation.abstract.raw <> proposal.abstract.raw:
                found_change = True
                presentation.abstract = proposal.abstract
            if presentation.speaker <> proposal.speaker:
                found_change = True
                presentation.speaker = proposal.speaker
            if found_change:
                found_any_change = True
                self.stdout.write('Updating %s by %s' % (
                    presentation.title, presentation.speaker))
                presentation.save()

        if not found_any_change:
            self.stdout.write('All presentations are up to date.')

