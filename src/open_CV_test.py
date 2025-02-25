import cv2
import numpy as np

def show_image(img, title: str = "Image"):
    # Resize for display
    scale_percent = 50  # Resize to 50% of the original size
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    resized_img = cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)

    while True:
        cv2.imshow(title, resized_img)
        if cv2.waitKey(1) == 27 or cv2.getWindowProperty(title, cv2.WND_PROP_VISIBLE) < 1:
            cv2.destroyAllWindows()
            break

def skeletonize(img):
    """ Morphological Skeletonization using OpenCV """
    skeleton = np.zeros(img.shape, np.uint8)  # Empty image for output
    kernel = np.ones((3,3), np.uint8)  # Structuring element
    temp = np.copy(img)
    
    while True:
        eroded = cv2.erode(temp, kernel)
        temp_opened = cv2.dilate(eroded, kernel)
        temp_skeleton = cv2.subtract(temp, temp_opened)
        skeleton = cv2.bitwise_or(skeleton, temp_skeleton)
        temp = eroded.copy()
        if cv2.countNonZero(temp) == 0:
            break
            
    return skeleton

# Load the image
img = cv2.imread("photo_image.jpeg")

# Convert to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply GaussianBlur
#gray = cv2.GaussianBlur(gray, (9, 9), 120)
gray = cv2.medianBlur(gray, 15)
show_image(gray, "gray")

#binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
_, binary = cv2.threshold(gray, 80, 255, cv2.THRESH_BINARY_INV)
show_image(binary, "threshold1")

kernel = np.ones((5, 5), np.uint8)
binary = cv2.dilate(binary, kernel)
show_image(binary, "dilate")

kernel = np.ones((3, 3), np.uint8)
binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel, iterations=5)
show_image(binary, "close")

binary = skeletonize(binary)
show_image(binary, "skeletonize")

# Detect circles
circles = cv2.HoughCircles(
    gray,
    cv2.HOUGH_GRADIENT, dp=0.8, minDist=30,
    param1=50, param2=30, minRadius=5, maxRadius=40
)

# Draw detected circles
if circles is not None:
    circles = np.uint16(np.around(circles))
    for circle in circles[0, :]:
        x, y, r = circle
        cv2.circle(img, (x, y), r, (255, 0, 255), 3)
        cv2.circle(img, (x, y), 2, (255, 255, 255), 3)
    
    print(f"Circles: {circles}")

# Assuming 'edges' is your edge-detected image
lines = cv2.HoughLinesP(binary, 1, np.pi / 180, threshold=10, minLineLength=60, maxLineGap=15)

# Create a blank image to draw lines
line_image = np.zeros_like(img)
show_image(line_image, "Black")

# Draw detected lines on the blank image
for line in lines:
    for x1, y1, x2, y2 in line:
        cv2.line(line_image, (x1, y1), (x2, y2), (255, 255, 255), 2)  # Draw in white
show_image(line_image, "Lines on Black")

# Convert to grayscale and apply thresholding
gray_lines = cv2.cvtColor(line_image, cv2.COLOR_BGR2GRAY)
thresh_lines = cv2.adaptiveThreshold(gray_lines, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

# Find contours of the lines
contours, _ = cv2.findContours(thresh_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Draw contours on the original image
for contour in contours:
    # Get the minimum area rectangle for each contour
    rect = cv2.minAreaRect(contour)
    print(rect)
    box = cv2.boxPoints(rect)  # Get the four corners of the rectangle
    box = np.int32(box)  # Convert to integer points  # Convert to integer points

    # Draw the rotated rectangle on the original image
    img = cv2.drawContours(img, [box], 0, (0, 0, 255), 2)  # Draw in red
# Show the final image with rotated rectangles
show_image(img)
