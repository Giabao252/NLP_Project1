from dataclasses import dataclass
from typing import Optional, List
import json

@dataclass
class HomographAnalysis:
    word: str
    sense1: str
    sense2: str
    sense1_age: int
    sense2_age: int
    humor_explanation: str
    is_appropriate: bool
    confidence: float

class JokeAnalyzer:
    def __init__(self, age_of_acquisition_db: dict):
        """
        age_of_acquisition_db: {"word": {"sense": "meaning", "aoa": age}}
        """
        self.aoa_db = age_of_acquisition_db
    
    def analyze_joke(self, text: str, target_age: int) -> Optional[HomographAnalysis]:
        """
        Main entry point. Returns None if no homograph detected.
        """
        homographs = self.detect_homographs(text)
        
        if not homographs:
            return None
        
        # For simplicity, analyze the most prominent homograph
        homograph = homographs[0]
        
        meanings = self.fetch_meanings(homograph)
        humor = self.explain_humor(text, homograph, meanings)
        is_appropriate = self.check_appropriateness(meanings, target_age)
        
        return HomographAnalysis(
            word=homograph,
            sense1=meanings[0],
            sense2=meanings[1],
            sense1_age=self.aoa_db.get(homograph, {}).get("sense1_aoa", 0),
            sense2_age=self.aoa_db.get(homograph, {}).get("sense2_aoa", 0),
            humor_explanation=humor,
            is_appropriate=is_appropriate,
            confidence=0.85  # placeholder
        )
    
    def detect_homographs(self, text: str) -> List[str]:
        """Find words with multiple meanings in the text."""
        words = text.lower().split()
        candidates = [w for w in words if w in self.aoa_db]
        return candidates
    
    def fetch_meanings(self, word: str) -> tuple:
        """Return two primary senses of the homograph."""
        entry = self.aoa_db.get(word, {})
        return (entry.get("sense1"), entry.get("sense2"))
    
    def explain_humor(self, text: str, word: str, meanings: tuple) -> str:
        """Explain how the word creates humor."""
        # This is where you'd use an LLM or rule-based logic
        return f"The word '{word}' creates ambiguity between: {meanings[0]} and {meanings[1]}"
    
    def check_appropriateness(self, meanings: tuple, target_age: int) -> bool:
        """Determine if both meanings are acquired by target_age."""
        # Implement based on your age-of-acquisition data
        return True