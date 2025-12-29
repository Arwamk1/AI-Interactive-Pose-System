import cv2
import numpy as np
from collections import deque
import random

class VisualEffects:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.left_hand_trail = deque(maxlen=30)
        self.right_hand_trail = deque(maxlen=30)
        self.particles = [] # List of particles [x, y, vx, vy, life, color]
    
    def update_trails(self, left_wrist, right_wrist):
        self.left_hand_trail.appendleft(left_wrist)
        self.right_hand_trail.appendleft(right_wrist)
        
        # Spawn particles if moving
        if len(self.left_hand_trail) > 1:
            prev = self.left_hand_trail[1]
            curr = self.left_hand_trail[0]
            if prev and curr:
                dist = np.linalg.norm(np.array(prev) - np.array(curr))
                if dist > 5:
                    self._spawn_particles(curr, (255, 0, 255))
        
        if len(self.right_hand_trail) > 1:
            prev = self.right_hand_trail[1]
            curr = self.right_hand_trail[0]
            if prev and curr:
                dist = np.linalg.norm(np.array(prev) - np.array(curr))
                if dist > 5:
                    self._spawn_particles(curr, (0, 255, 255))

    def _spawn_particles(self, pos, color):
        for _ in range(5):
            x, y = pos
            vx = random.uniform(-5, 5)
            vy = random.uniform(-5, 5)
            life = random.randint(10, 30)
            self.particles.append([x, y, vx, vy, life, color])

    def update_particles(self):
        for p in self.particles:
            p[0] += p[2] # x += vx
            p[1] += p[3] # y += vy
            p[4] -= 1    # life -= 1
        
        # Remove dead particles
        self.particles = [p for p in self.particles if p[4] > 0]

    def draw_effects(self, img):
        # Draw trails
        self._draw_trail(img, self.left_hand_trail, (255, 0, 255))
        self._draw_trail(img, self.right_hand_trail, (0, 255, 255))
        
        # Draw particles
        for p in self.particles:
            cv2.circle(img, (int(p[0]), int(p[1])), 3, p[5], -1)
            
        return img

    def _draw_trail(self, img, trail, color):
        for i in range(1, len(trail)):
            if trail[i - 1] is None or trail[i] is None:
                continue
            thickness = int(np.sqrt(30 / float(i + 1)) * 3)
            cv2.line(img, trail[i - 1], trail[i], color, thickness)

    def apply_background_effect(self, img, state):
        if not state:
            return img
            
        overlay = img.copy()
        alpha = 0.4
        color = (0, 0, 0)
        
        if state == 'Left':
            color = (0, 0, 255) # Red tint
            cv2.putText(img, "Left Hand Raised!", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
        elif state == 'Right':
            color = (255, 0, 0) # Blue tint
            cv2.putText(img, "Right Hand Raised!", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
        elif state == 'Both':
            color = (0, 255, 0) # Green tint
            cv2.putText(img, "Both Hands Raised! POWER UP!", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
            
        cv2.rectangle(overlay, (0, 0), (self.width, self.height), color, -1)
        cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)
            
        return img
