import cv2
import time
import math
import numpy as np
import HandTrackingModule as htm

pTime = 0
cap = cv2.VideoCapture(0)
detector = htm.handDetector()


start_time = None
countdown_done = False
drawing_points = []
locked_hand_label = None
drawing_mode = True
prev_pinch_pos = None

def save_drawing_as_png(points, width, height, filename="my_sign.png"):
  canvas = np.zeros((height, width, 4), dtype=np.uint8)
  if len(points) > 1:
    for i in range(1, len(points)):
      cv2.line(canvas, points[i-1], points[i], (255, 255, 255, 255), 5)
  cv2.imwrite(filename, canvas)
  
while True:
  success, img = cap.read()
  if not success:
    break
  height, width, _ = img.shape

  img = detector.findHands(img, draw=False)

  for i in range(2):
    lmList, label = detector.findPosition(img, handNo=i, draw=False)
    if len(lmList) != 0:
      if locked_hand_label is None:
        locked_hand_label = label
      if label == locked_hand_label:

        index_tip = lmList[8]
        cx, cy = index_tip[1], index_tip[2]

        if start_time is None:
          start_time = time.time()

        elapsed = time.time() - start_time

        if not countdown_done:
          remaining = int(3 - elapsed)
          if remaining > 0:
            cv2.putText(img, str(remaining), (cx, cy - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
          else:
            countdown_done = True
        else:
          if drawing_mode:
            if 0 <= cx < width and 0 <= cy < height:
              drawing_points.append((cx, cy))
          else:
            thumb_tip = lmList[4]
            tx, ty = thumb_tip[1], thumb_tip[2]

            distance = math.hypot(cx - tx, cy - ty)
            pinch_threshold = 40

            if distance < pinch_threshold:
              pinch_pos = ((cx + tx) // 2, (cy + ty) // 2)

              if prev_pinch_pos is not None:
                dx = pinch_pos[0] - prev_pinch_pos[0]
                dy = pinch_pos[1] - prev_pinch_pos[1]

                new_points = []
                for (x, y) in drawing_points:
                  new_x = x + dx
                  new_y = y + dy
                  new_x = max(0, min(new_x, width - 1))
                  new_y = max(0, min(new_y, height - 1))
                  new_points.append((new_x, new_y))
                drawing_points = new_points

              prev_pinch_pos = pinch_pos
            else:
              prev_pinch_pos = None

        break

  if len(drawing_points) > 1:
    for i in range(1, len(drawing_points)):
      cv2.line(img, drawing_points[i - 1], drawing_points[i], (255, 255, 255), 3)

  cTime = time.time()
  fps = 1 / (cTime - pTime) if (cTime - pTime) > 0 else 0
  pTime = cTime
  cv2.putText(img, str(int(fps)), (10, 70),cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

  cv2.imshow("Image", img)

  key = cv2.waitKey(1) & 0xFF
  if key == ord('q'):
    break
  elif key == ord('d'):
    drawing_mode = not drawing_mode
    prev_pinch_pos = None
  elif key == ord('s'):
    if len(drawing_points) > 1:
      save_drawing_as_png(drawing_points, width, height)

cap.release()
cv2.destroyAllWindows()
