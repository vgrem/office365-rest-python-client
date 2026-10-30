from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.education.challenging_word import ChallengingWord
from office365.entity import Entity
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.odata_property import odata


class ReadingAssignmentSubmission(Entity):
    @odata(name="accuracyScore")
    @property
    def accuracy_score(self) -> Optional[float]:
        """Gets the accuracyScore property"""
        return self.properties.get("accuracyScore", None)

    @odata(name="action")
    @property
    def action(self) -> Optional[str]:
        """Gets the action property"""
        return self.properties.get("action", None)

    @odata(name="assignmentId")
    @property
    def assignment_id(self) -> Optional[str]:
        """Gets the assignmentId property"""
        return self.properties.get("assignmentId", None)

    @odata(name="challengingWords")
    @property
    def challenging_words(self) -> ClientValueCollection[ChallengingWord]:
        """Gets the challengingWords property"""
        return self.properties.get("challengingWords", ClientValueCollection[ChallengingWord](ChallengingWord))

    @odata(name="classId")
    @property
    def class_id(self) -> Optional[str]:
        """Gets the classId property"""
        return self.properties.get("classId", None)

    @odata(name="insertions")
    @property
    def insertions(self) -> Optional[int]:
        """Gets the insertions property"""
        return self.properties.get("insertions", None)

    @odata(name="mispronunciations")
    @property
    def mispronunciations(self) -> Optional[int]:
        """Gets the mispronunciations property"""
        return self.properties.get("mispronunciations", None)

    @odata(name="missedExclamationMarks")
    @property
    def missed_exclamation_marks(self) -> Optional[int]:
        """Gets the missedExclamationMarks property"""
        return self.properties.get("missedExclamationMarks", None)

    @odata(name="missedPeriods")
    @property
    def missed_periods(self) -> Optional[int]:
        """Gets the missedPeriods property"""
        return self.properties.get("missedPeriods", None)

    @odata(name="missedQuestionMarks")
    @property
    def missed_question_marks(self) -> Optional[int]:
        """Gets the missedQuestionMarks property"""
        return self.properties.get("missedQuestionMarks", None)

    @odata(name="missedShorts")
    @property
    def missed_shorts(self) -> Optional[int]:
        """Gets the missedShorts property"""
        return self.properties.get("missedShorts", None)

    @odata(name="monotoneScore")
    @property
    def monotone_score(self) -> Optional[float]:
        """Gets the monotoneScore property"""
        return self.properties.get("monotoneScore", None)

    @odata(name="omissions")
    @property
    def omissions(self) -> Optional[int]:
        """Gets the omissions property"""
        return self.properties.get("omissions", None)

    @odata(name="repetitions")
    @property
    def repetitions(self) -> Optional[int]:
        """Gets the repetitions property"""
        return self.properties.get("repetitions", None)

    @odata(name="selfCorrections")
    @property
    def self_corrections(self) -> Optional[int]:
        """Gets the selfCorrections property"""
        return self.properties.get("selfCorrections", None)

    @odata(name="studentId")
    @property
    def student_id(self) -> Optional[str]:
        """Gets the studentId property"""
        return self.properties.get("studentId", None)

    @odata(name="submissionDateTime")
    @property
    def submission_date_time(self) -> Optional[datetime]:
        """Gets the submissionDateTime property"""
        return self.properties.get("submissionDateTime", datetime.min)

    @odata(name="submissionId")
    @property
    def submission_id(self) -> Optional[str]:
        """Gets the submissionId property"""
        return self.properties.get("submissionId", None)

    @odata(name="unexpectedPauses")
    @property
    def unexpected_pauses(self) -> Optional[int]:
        """Gets the unexpectedPauses property"""
        return self.properties.get("unexpectedPauses", None)

    @odata(name="wordCount")
    @property
    def word_count(self) -> Optional[int]:
        """Gets the wordCount property"""
        return self.properties.get("wordCount", None)

    @odata(name="wordsPerMinute")
    @property
    def words_per_minute(self) -> Optional[float]:
        """Gets the wordsPerMinute property"""
        return self.properties.get("wordsPerMinute", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ReadingAssignmentSubmission"
