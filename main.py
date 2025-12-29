import cv2
import time
from src.pose_detector import PoseDetector
from src.visual_effects import VisualEffects

def main():
    # Initialize Camera
    cap = cv2.VideoCapture(0)
    
    # Set camera resolution (HD)
    cap.set(3, 1280)
    cap.set(4, 720)
    
    detector = PoseDetector()
    
    # Get initial frame size
    success, img = cap.read()
    if not success:
        print("Error: Could not access the camera.")
        return
    
    h, w, c = img.shape
    effects = VisualEffects(w, h)
    
    pTime = 0
    
    print("System Started. Press 'q' to exit.")
    
    while True:
        success, img = cap.read()
        if not success:
            break
            
        # Flip image horizontally for mirror effect
        img = cv2.flip(img, 1)
            
        # 1. Find Pose
        # We don't draw default landmarks on the original image yet
        detector.find_pose(img, draw=False) 
        lm_list = detector.find_position(img, draw=False)
        
        # 2. Get Hand Positions (Left Wrist: 15, Right Wrist: 16)
        # Note: Since we flipped the image, Left and Right might be swapped visually if we used original landmarks directly,
        # but MediaPipe coords are relative to the image provided.
        # However, flipping the image BEFORE passing to MediaPipe means Left is user's actual right (mirror).
        # Let's check landmarks. 
        # If I flip the image, the pixel at (0,0) is now the top-right of the original scene.
        # MediaPipe processes the flipped image. So "Left Wrist" (15) is the left wrist in the FLIPPED image.
        # Which corresponds to the user's RIGHT hand if they are facing the camera.
        # This is standard mirror behavior.
        
        left_wrist = None
        right_wrist = None
        
        if len(lm_list) != 0:
            # 15 is left wrist, 16 is right wrist
            left_wrist = (lm_list[15][1], lm_list[15][2])
            right_wrist = (lm_list[16][1], lm_list[16][2])
            
        # 3. Check Interactions
        state = detector.is_hand_raised()
        
        # 4. Update Visual Effects
        effects.update_trails(left_wrist, right_wrist)
        effects.update_particles()
        
        # 5. Draw Everything
        
        # A. Apply Background Effects (Screen Color Change)
        img = effects.apply_background_effect(img, state)
        
        # B. Draw Trails and Particles
        img = effects.draw_effects(img)
        
        # C. Draw Skeleton (Optional: Make it look cool)
        if detector.results.pose_landmarks:
            # Draw connections with custom style if possible, or use default
            detector.mp_draw.draw_landmarks(
                img, 
                detector.results.pose_landmarks, 
                detector.mp_pose.POSE_CONNECTIONS,
                detector.mp_draw.DrawingSpec(color=(0,255,0), thickness=2, circle_radius=2),
                detector.mp_draw.DrawingSpec(color=(0,0,255), thickness=2, circle_radius=2)
            )

        # 6. FPS Calculation
        cTime = time.time()
        fps = 1 / (cTime - pTime) if (cTime - pTime) > 0 else 0
        pTime = cTime
        
        cv2.putText(img, f"FPS: {int(fps)}", (10, 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
        
        cv2.imshow("AI Pose Interaction Demo", img)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
