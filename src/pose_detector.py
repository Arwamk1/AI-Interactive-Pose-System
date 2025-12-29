import mediapipe as mp
import cv2
import math

class PoseDetector:
    def __init__(self, mode=False, complexity=1, smooth=True, segmentation=False, smooth_segmentation=True, detection_con=0.5, track_con=0.5):
        self.mode = mode
        self.complexity = complexity
        self.smooth = smooth
        self.segmentation = segmentation
        self.smooth_segmentation = smooth_segmentation
        self.detection_con = detection_con
        self.track_con = track_con

        self.mp_draw = mp.solutions.drawing_utils
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            static_image_mode=self.mode,
            model_complexity=self.complexity,
            smooth_landmarks=self.smooth,
            enable_segmentation=self.segmentation,
            smooth_segmentation=self.smooth_segmentation,
            min_detection_confidence=self.detection_con,
            min_tracking_confidence=self.track_con
        )
        self.results = None
        self.lm_list = []

    def find_pose(self, img, draw=True):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(img_rgb)
        if self.results.pose_landmarks:
            if draw:
                self.mp_draw.draw_landmarks(img, self.results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)
        return img

    def find_position(self, img, draw=True):
        self.lm_list = []
        if self.results and self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lm_list.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
        return self.lm_list

    def is_hand_raised(self):
        """
        Checks if either hand is raised above the shoulders.
        Returns: 'Left', 'Right', 'Both', or None
        """
        if len(self.lm_list) < 33:
            return None

        # Landmarks:
        # 11: left_shoulder, 12: right_shoulder
        # 15: left_wrist, 16: right_wrist
        
        left_shoulder_y = self.lm_list[11][2]
        right_shoulder_y = self.lm_list[12][2]
        left_wrist_y = self.lm_list[15][2]
        right_wrist_y = self.lm_list[16][2]

        left_raised = left_wrist_y < left_shoulder_y
        right_raised = right_wrist_y < right_shoulder_y

        if left_raised and right_raised:
            return 'Both'
        elif left_raised:
            return 'Left'
        elif right_raised:
            return 'Right'
        return None
