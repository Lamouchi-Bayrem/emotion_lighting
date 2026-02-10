"""
Emotion Detection Module
Detects facial emotions using DeepFace
"""

import cv2
import numpy as np
from deepface import DeepFace
from typing import Dict, Optional
import warnings
warnings.filterwarnings('ignore')


class EmotionDetector:
    """Detects facial emotions from images"""
    
    # Emotion to color mapping for mood lighting
    EMOTION_COLORS = {
        'happy': (255, 200, 0),      # Warm yellow/orange
        'sad': (100, 150, 255),       # Cool blue
        'angry': (255, 50, 50),       # Red
        'surprise': (255, 255, 100),  # Bright yellow
        'fear': (150, 100, 200),      # Purple
        'disgust': (100, 200, 100),   # Green
        'neutral': (200, 200, 200)   # White/neutral
    }
    
    def __init__(self):
        """Initialize emotion detector"""
        self.last_emotion = None
        self.emotion_history = []
    
    def detect_emotion(self, frame: np.ndarray) -> Optional[Dict]:
        """
        Detect emotion in frame
        
        Args:
            frame: Input frame (BGR format)
            
        Returns:
            dict: Emotion detection results with 'emotion', 'dominant_emotion', 'scores', 'color'
        """
        try:
            # DeepFace expects RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Detect emotion
            result = DeepFace.analyze(
                rgb_frame,
                actions=['emotion'],
                enforce_detection=False,
                silent=True
            )
            
            # Handle both single dict and list results
            if isinstance(result, list):
                result = result[0]
            
            # Get emotion scores
            emotion_scores = result.get('emotion', {})
            dominant_emotion = result.get('dominant_emotion', 'neutral')
            
            # Get color for dominant emotion
            color = self.EMOTION_COLORS.get(dominant_emotion.lower(), (200, 200, 200))
            
            # Update history
            self.last_emotion = dominant_emotion
            self.emotion_history.append({
                'emotion': dominant_emotion,
                'scores': emotion_scores,
                'color': color
            })
            
            # Keep only last 30 entries
            if len(self.emotion_history) > 30:
                self.emotion_history.pop(0)
            
            return {
                'emotion': dominant_emotion,
                'dominant_emotion': dominant_emotion,
                'scores': emotion_scores,
                'color': color,
                'face_detected': True
            }
            
        except Exception as e:
            # No face detected or other error
            return {
                'emotion': 'none',
                'dominant_emotion': 'none',
                'scores': {},
                'color': (128, 128, 128),
                'face_detected': False,
                'error': str(e)
            }
    
    def get_average_emotion(self, window_size: int = 10) -> Optional[Dict]:
        """
        Get average emotion over recent history
        
        Args:
            window_size: Number of recent detections to average
            
        Returns:
            dict: Average emotion scores and dominant emotion
        """
        if not self.emotion_history:
            return None
        
        recent = self.emotion_history[-window_size:]
        
        # Average emotion scores
        all_scores = {}
        for entry in recent:
            for emotion, score in entry['scores'].items():
                all_scores[emotion] = all_scores.get(emotion, 0) + score
        
        # Normalize
        total = sum(all_scores.values())
        if total > 0:
            for emotion in all_scores:
                all_scores[emotion] /= len(recent)
        
        # Find dominant emotion
        dominant = max(all_scores.items(), key=lambda x: x[1])[0] if all_scores else 'neutral'
        color = self.EMOTION_COLORS.get(dominant.lower(), (200, 200, 200))
        
        return {
            'emotion': dominant,
            'scores': all_scores,
            'color': color
        }
    
    def get_color_for_emotion(self, emotion: str) -> tuple:
        """Get RGB color for emotion"""
        return self.EMOTION_COLORS.get(emotion.lower(), (200, 200, 200))
    
    def reset(self):
        """Reset detector state"""
        self.last_emotion = None
        self.emotion_history.clear()





