"""ProposalBase implementations for the PyCon SG project."""
from django.db import models

from south.modelsinspector import add_introspection_rules
from symposion.proposals.models import ProposalBase


add_introspection_rules([], ["^timezones\.fields\.TimeZoneField"])


class Proposal(ProposalBase):

    AUDIENCE_LEVEL_NOVICE = 1
    AUDIENCE_LEVEL_EXPERIENCED = 2
    AUDIENCE_LEVEL_INTERMEDIATE = 3
    AUDIENCE_LEVEL_ALL = 4

    AUDIENCE_LEVELS = [
        (AUDIENCE_LEVEL_NOVICE, 'Novice'),
        (AUDIENCE_LEVEL_INTERMEDIATE, 'Intermediate'),
        (AUDIENCE_LEVEL_EXPERIENCED, 'Experienced'),
        (AUDIENCE_LEVEL_ALL, 'All'),
    ]

    audience_level = models.IntegerField(choices=AUDIENCE_LEVELS)

    recording_release = models.BooleanField(
        default=True,
        help_text=(
            'By submitting your talk proposal, you agree to give permission to'
            ' the conference organizers to record, edit, and release audio'
            ' and/or video of your presentation. If you do not agree to this,'
            ' please uncheck this box.')
    )

    class Meta:
        abstract = True


class TalkProposal(Proposal):
    proposal_type = 'Talk'

    class Meta:
        verbose_name = 'talk proposal'


class TutorialProposal(Proposal):
    proposal_type = 'Tutorial'

    class Meta:
        verbose_name = 'tutorial proposal'
