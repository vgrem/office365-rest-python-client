from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.education.readingcoachstorytype import ReadingCoachStoryType
from office365.entity import Entity
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata


class ReadingCoachPassage(Entity):
    @odata(name="isReadingCompleted")
    @property
    def is_reading_completed(self) -> Optional[bool]:
        """Gets the isReadingCompleted property"""
        return self.properties.get("isReadingCompleted", None)

    @odata(name="languageTag")
    @property
    def language_tag(self) -> Optional[str]:
        """Gets the languageTag property"""
        return self.properties.get("languageTag", None)

    @odata(name="practicedAtDateTime")
    @property
    def practiced_at_date_time(self) -> Optional[datetime]:
        """Gets the practicedAtDateTime property"""
        return self.properties.get("practicedAtDateTime", datetime.min)

    @odata(name="practiceWords")
    @property
    def practice_words(self) -> StringCollection:
        """Gets the practiceWords property"""
        return self.properties.get("practiceWords", StringCollection())

    @odata(name="storyType")
    @property
    def story_type(self) -> ReadingCoachStoryType:
        """Gets the storyType property"""
        return self.properties.get("storyType", ReadingCoachStoryType.aiGenerated)

    @odata(name="studentId")
    @property
    def student_id(self) -> Optional[str]:
        """Gets the studentId property"""
        return self.properties.get("studentId", None)

    @odata(name="timeSpentReadingInSeconds")
    @property
    def time_spent_reading_in_seconds(self) -> Optional[float]:
        """Gets the timeSpentReadingInSeconds property"""
        return self.properties.get("timeSpentReadingInSeconds", None)

    @odata(name="wordsAccuracyPercentage")
    @property
    def words_accuracy_percentage(self) -> Optional[float]:
        """Gets the wordsAccuracyPercentage property"""
        return self.properties.get("wordsAccuracyPercentage", None)

    @odata(name="wordsPerMinute")
    @property
    def words_per_minute(self) -> Optional[float]:
        """Gets the wordsPerMinute property"""
        return self.properties.get("wordsPerMinute", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ReadingCoachPassage"
