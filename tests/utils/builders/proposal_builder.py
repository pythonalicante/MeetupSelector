from typing import Iterable

from django.contrib.auth import get_user_model

from meetupselector.proposals.models import Proposal
from meetupselector.talks.models import Talk, Topic

User = get_user_model()


class ProposalBuilder:
    _subject: str = "subject"
    _description: str = "description"
    _topics: Iterable[Topic] = []
    _talks: Iterable[Talk] = []
    _proposed_by: User = None

    def with_subject(self, subject):
        self._subject = subject
        return self

    def with_description(self, description: str) -> "ProposalBuilder":
        self._description = description
        return self

    def with_topics(self, topics: Iterable[Topic]) -> "ProposalBuilder":
        self._topics = topics
        return self

    def with_talks(self, talks: Iterable[Talk]) -> "ProposalBuilder":
        self._talks = talks
        return self

    def with_proposed_by(self, proposed_by: User) -> "ProposalBuilder":
        self._proposed_by = proposed_by
        return self

    def build(self) -> Proposal:
        return Proposal.objects.create(
            subject=self._subject,
            description=self._description,
            proposed_by=self._proposed_by,
            topics=self._topics,
            talks=self._talks,
        )
