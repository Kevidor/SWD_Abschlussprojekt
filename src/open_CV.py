import cv2
import numpy as np

def show_image(img):
    # Resize for display
    scale_percent = 50  # Resize to 50% of the original size
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    resized_img = cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)

    while True:
        cv2.imshow("Image", resized_img)
        if cv2.waitKey(1) == 27 or cv2.getWindowProperty("Image", cv2.WND_PROP_VISIBLE) < 1:
            cv2.destroyAllWindows()
            break

# Load the image
img = cv2.imread("photo_image.jpg")

# Convert to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply GaussianBlur
#gray = cv2.GaussianBlur(gray, (9, 9), 120)
blurred = cv2.medianBlur(gray, 21)

show_image(blurred)

#binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
binary = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                               cv2.THRESH_BINARY_INV, 15, 5)
show_image(binary)

kernel = np.ones((7, 7), np.uint8)
binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel, iterations=2)
show_image(binary)

kernel = np.ones((3, 3), np.uint8)
binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel, iterations=2)
show_image(binary)

binary = cv2.dilate(binary, kernel, iterations=1)
show_image(binary)

# Detect circles
circles = cv2.HoughCircles(
    gray,
    cv2.HOUGH_GRADIENT, dp=0.8, minDist=30,
    param1=50, param2=30, minRadius=5, maxRadius=40
)
print("Circles:")
print(circles)

# Draw detected circles
if circles is not None:
    circles = np.uint16(np.around(circles))
    for circle in circles[0, :]:
        x, y, r = circle
        cv2.circle(img, (x, y), r, (255, 0, 255), 3)
        cv2.circle(img, (x, y), 2, (255, 255, 255), 3)
        #print(f"{x}, {y}")

# Edge Detection
edges = cv2.Canny(binary, 50, 150, apertureSize=3)
show_image(edges)

# Assuming 'edges' is your edge-detected image
lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=10, minLineLength=200, maxLineGap=40)
print("Lines:")
print(lines)

# Draw the merged centerlines
for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(img, (x1, y1), (x2, y2), (255, 255, 0), 2)

show_image(img)