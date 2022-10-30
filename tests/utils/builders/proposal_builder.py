from typing import Iterable

from django.contrib.auth import get_user_model

from meetupselector.proposals.models import Proposal
from meetupselector.talks.models import Topic

User = get_user_model()


class ProposalBuilder:
    _subject: str = "subject"
    _description: str = "description"
    _topics: Iterable[Topic] = []
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

    def with_proposed_by(self, proposed_by: User) -> "ProposalBuilder":
        self._proposed_by = proposed_by
        return self

    def build(self) -> Proposal:
        proposal = Proposal.objects.create(
            subject=self._subject,
            description=self._description,
            proposed_by=self._proposed_by,
        )
        if self._topics:
            for topic in self._topics:
                proposal.topics.add(topic)
        return proposal
