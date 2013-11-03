"""Settings for the ``symposion`` app."""

CONFERENCE_ID = 1
SYMPOSION_PAGE_REGEX = r'(([\w-]{1,})(/[\w-]{1,})*)/'
PROPOSAL_FORMS = {
    'tutorial': 'proposals_pyconsg.forms.TutorialProposalForm',
    'talk': 'proposals_pyconsg.forms.TalkProposalForm',
}
