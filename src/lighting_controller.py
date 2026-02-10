"""
Mood Lighting Controller Module
Simulates smart light control based on emotions
"""

import time
from typing import Tuple, Optional
from datetime import datetime


class LightingController:
    """Controls mood lighting based on emotions"""
    
    def __init__(self):
        """Initialize lighting controller"""
        self.current_color = (200, 200, 200)  # Neutral white
        self.target_color = (200, 200, 200)
        self.is_on = False
        self.brightness = 0.7
        self.transition_speed = 0.1  # Color transition speed
        self.last_update = time.time()
        self.session_log = []
    
    def set_emotion_color(self, color: Tuple[int, int, int], smooth: bool = True):
        """
        Set lighting color based on emotion
        
        Args:
            color: RGB color tuple
            smooth: Whether to smoothly transition
        """
        if smooth:
            self.target_color = color
        else:
            self.current_color = color
            self.target_color = color
    
    def update(self):
        """Update lighting state (smooth transitions)"""
        current_time = time.time()
        dt = current_time - self.last_update
        
        # Smooth color transition
        if self.current_color != self.target_color:
            r1, g1, b1 = self.current_color
            r2, g2, b2 = self.target_color
            
            # Interpolate
            step = self.transition_speed * dt * 10
            r = int(r1 + (r2 - r1) * step)
            g = int(g1 + (g2 - g1) * step)
            b = int(b1 + (b2 - b1) * step)
            
            # Check if close enough
            if abs(r - r2) < 5 and abs(g - g2) < 5 and abs(b - b2) < 5:
                self.current_color = self.target_color
            else:
                self.current_color = (r, g, b)
        
        self.last_update = current_time
    
    def get_current_color(self) -> Tuple[int, int, int]:
        """Get current lighting color"""
        if not self.is_on:
            return (0, 0, 0)  # Off
        
        # Apply brightness
        r, g, b = self.current_color
        r = int(r * self.brightness)
        g = int(g * self.brightness)
        b = int(b * self.brightness)
        
        return (r, g, b)
    
    def set_brightness(self, brightness: float):
        """Set brightness (0.0 to 1.0)"""
        self.brightness = max(0.0, min(1.0, brightness))
    
    def turn_on(self):
        """Turn lights on"""
        self.is_on = True
        self.log_event("lights_on")
    
    def turn_off(self):
        """Turn lights off"""
        self.is_on = False
        self.log_event("lights_off")
    
    def log_event(self, event_type: str, emotion: str = None, color: Tuple = None):
        """Log lighting event"""
        entry = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'event': event_type,
            'emotion': emotion,
            'color': color
        }
        self.session_log.append(entry)
    
    def get_session_log(self) -> list:
        """Get session log"""
        return self.session_log.copy()
    
    def clear_log(self):
        """Clear session log"""
        self.session_log.clear()





