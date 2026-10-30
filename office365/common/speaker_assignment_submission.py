from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.entity import Entity
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata


class SpeakerAssignmentSubmission(Entity):
    @odata(name="assignmentId")
    @property
    def assignment_id(self) -> Optional[str]:
        """Gets the assignmentId property"""
        return self.properties.get("assignmentId", None)

    @odata(name="averageWordsPerMinutePace")
    @property
    def average_words_per_minute_pace(self) -> Optional[int]:
        """Gets the averageWordsPerMinutePace property"""
        return self.properties.get("averageWordsPerMinutePace", None)

    @odata(name="classId")
    @property
    def class_id(self) -> Optional[str]:
        """Gets the classId property"""
        return self.properties.get("classId", None)

    @odata(name="fillerWordsOccurrencesCount")
    @property
    def filler_words_occurrences_count(self) -> Optional[int]:
        """Gets the fillerWordsOccurrencesCount property"""
        return self.properties.get("fillerWordsOccurrencesCount", None)

    @odata(name="incorrectCameraDistanceOccurrencesCount")
    @property
    def incorrect_camera_distance_occurrences_count(self) -> Optional[int]:
        """Gets the incorrectCameraDistanceOccurrencesCount property"""
        return self.properties.get("incorrectCameraDistanceOccurrencesCount", None)

    @odata(name="lengthOfSubmissionInSeconds")
    @property
    def length_of_submission_in_seconds(self) -> Optional[float]:
        """Gets the lengthOfSubmissionInSeconds property"""
        return self.properties.get("lengthOfSubmissionInSeconds", None)

    @odata(name="lostEyeContactOccurrencesCount")
    @property
    def lost_eye_contact_occurrences_count(self) -> Optional[int]:
        """Gets the lostEyeContactOccurrencesCount property"""
        return self.properties.get("lostEyeContactOccurrencesCount", None)

    @odata(name="monotoneOccurrencesCount")
    @property
    def monotone_occurrences_count(self) -> Optional[int]:
        """Gets the monotoneOccurrencesCount property"""
        return self.properties.get("monotoneOccurrencesCount", None)

    @odata(name="nonInclusiveLanguageOccurrencesCount")
    @property
    def non_inclusive_language_occurrences_count(self) -> Optional[int]:
        """Gets the nonInclusiveLanguageOccurrencesCount property"""
        return self.properties.get("nonInclusiveLanguageOccurrencesCount", None)

    @odata(name="obstructedViewOccurrencesCount")
    @property
    def obstructed_view_occurrences_count(self) -> Optional[int]:
        """Gets the obstructedViewOccurrencesCount property"""
        return self.properties.get("obstructedViewOccurrencesCount", None)

    @odata(name="repetitiveLanguageOccurrencesCount")
    @property
    def repetitive_language_occurrences_count(self) -> Optional[int]:
        """Gets the repetitiveLanguageOccurrencesCount property"""
        return self.properties.get("repetitiveLanguageOccurrencesCount", None)

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

    @odata(name="topFillerWords")
    @property
    def top_filler_words(self) -> StringCollection:
        """Gets the topFillerWords property"""
        return self.properties.get("topFillerWords", StringCollection())

    @odata(name="topMispronouncedWords")
    @property
    def top_mispronounced_words(self) -> StringCollection:
        """Gets the topMispronouncedWords property"""
        return self.properties.get("topMispronouncedWords", StringCollection())

    @odata(name="topNonInclusiveWordsAndPhrases")
    @property
    def top_non_inclusive_words_and_phrases(self) -> StringCollection:
        """Gets the topNonInclusiveWordsAndPhrases property"""
        return self.properties.get("topNonInclusiveWordsAndPhrases", StringCollection())

    @odata(name="topRepetitiveWordsAndPhrases")
    @property
    def top_repetitive_words_and_phrases(self) -> StringCollection:
        """Gets the topRepetitiveWordsAndPhrases property"""
        return self.properties.get("topRepetitiveWordsAndPhrases", StringCollection())

    @odata(name="wordsSpokenCount")
    @property
    def words_spoken_count(self) -> Optional[int]:
        """Gets the wordsSpokenCount property"""
        return self.properties.get("wordsSpokenCount", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.SpeakerAssignmentSubmission"
