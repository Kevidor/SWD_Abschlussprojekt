import cv2
import numpy as np
from mechanism import Mechanism
from mechanism_components import Joint, Link, Rotor

class ImageRecognizer:
    def __init__(self, img_path:str = None):
        if not img_path == None:
            self.img = cv2.imread(img_path)
        else:
            self.img = img_path
        self.circle_pos = []
        self.line_pos = []
        self.link_assignment = {}
        self.joint_assignment = []

    def load_img(self, img_path:str):
        self.img_path = cv2.imread(img_path)

    def show_image(self, img, title: str = "Image"):
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
    
    def recognize_circles(self, debug: bool = False):
        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 15)

        circles = cv2.HoughCircles(gray,
                                cv2.HOUGH_GRADIENT,
                                dp=0.9, minDist=30, 
                                param1=50, param2=30, 
                                minRadius=35, maxRadius=60
                                )

        if circles is not None:
            img_temp = np.copy(self.img)
            circles = np.uint16(np.around(circles))
            for circle in circles[0, :]:
                x, y, r = circle
                self.circle_pos.append((int(x), int(y)))

                # Draw the circle
                cv2.circle(img_temp, (x, y), r, (255, 0, 255), 3)
                cv2.circle(img_temp, (x, y), 2, (255, 255, 255), 3)

        if debug:
            print(f"Circle_positions:\n{self.circle_pos}")
            self.show_image(img_temp, "Circles")

    def recognize_lines(self, debug: bool = False):
        def skeletonize(img):
            """
            Morphological Skeletonization
            """
            skeleton = np.zeros(img.shape, np.uint8)
            kernel = np.ones((3,3), np.uint8)
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
        
        def rect_to_line(rect):
            center, size, angle = rect
            width, height = size

            half_width = width / 2
            half_height = height / 2
            angle_rad = np.deg2rad(angle)

            if width > height:
                # Line along the width
                x_start = int(center[0] - half_width * np.cos(angle_rad))
                y_start = int(center[1] - half_width * np.sin(angle_rad))
                x_end = int(center[0] + half_width * np.cos(angle_rad))
                y_end = int(center[1] + half_width * np.sin(angle_rad))
            else:
                # Line along the height
                x_start = int(center[0] - half_height * np.sin(angle_rad))
                y_start = int(center[1] + half_height * np.cos(angle_rad))
                x_end = int(center[0] + half_height * np.sin(angle_rad))
                y_end = int(center[1] - half_height * np.cos(angle_rad))

            return (x_start, y_start), (x_end, y_end)
        
        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 15)

        _, binary = cv2.threshold(gray, 80, 255, cv2.THRESH_BINARY_INV)

        kernel = np.ones((5, 5), np.uint8)
        binary = cv2.dilate(binary, kernel)

        kernel = np.ones((3, 3), np.uint8)
        binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel, iterations=5)

        binary = skeletonize(binary)

        lines = cv2.HoughLinesP(binary, 1, np.pi / 180, threshold=10, minLineLength=60, maxLineGap=15)
        line_image = np.zeros_like(self.img)
        for line in lines:
            for x1, y1, x2, y2 in line:
                cv2.line(line_image, (x1, y1), (x2, y2), (255, 255, 255), 2)

        line_image = cv2.cvtColor(line_image, cv2.COLOR_BGR2GRAY)
        line_image = cv2.adaptiveThreshold(line_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

        contours, _ = cv2.findContours(line_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        img_temp = np.copy(self.img)
        for contour in contours:
            rect = cv2.minAreaRect(contour)
            self.line_pos.append(rect_to_line(rect))

            box = cv2.boxPoints(rect)
            box = np.int32(box)

            img_temp = cv2.drawContours(img_temp, [box], 0, (0, 0, 255), 2)
            img_temp = cv2.line(img_temp, self.line_pos[-1][0], self.line_pos[-1][1], (0, 255, 255), 2)
        
        if debug:
            print(f"Line_positions:\n{self.line_pos}")
            self.show_image(img_temp, "Lines:")

    def assign_links(self, radius: int = 10):
        link_assignments = {}
        joint_assignments = []

        for line in self.line_pos:
            link_assignments[line] = [None, None]

        for circle in self.circle_pos:
            circle_x, circle_y = circle
            assigned_to_line = False

            for line in self.line_pos:
                (start_x, start_y), (end_x, end_y) = line
                
                distance_start = np.sqrt((circle_x - start_x) ** 2 + (circle_y - start_y) ** 2)
                distance_end = np.sqrt((circle_x - end_x) ** 2 + (circle_y - end_y) ** 2)
                
                if distance_start < radius:
                    link_assignments[line][0] = (circle_x, circle_y)
                    assigned_to_line = True
                elif distance_end < radius:
                    link_assignments[line][1] = (circle_x, circle_y)
                    assigned_to_line = True

            if not assigned_to_line:
                joint_assignments.append((circle_x, circle_y))

        self.link_assignment = link_assignments
        self.joint_assignment = joint_assignments
    
    def create_Joints(self):
        pass

    def create_Links(self):
        pass

if __name__ == "__main__":
    image_recognizer = ImageRecognizer("photo_image.jpeg")
    mekanism = Mechanism()

    image_recognizer.show_image(image_recognizer.img)
    image_recognizer.recognize_circles(True)
    image_recognizer.recognize_lines(True)
    image_recognizer.assign_links(60)

    print(f"\nLink_Assignment: {image_recognizer.link_assignment}")
    print(f"\nJoint_Assignment: {image_recognizer.joint_assignment}")

    img = np.copy(image_recognizer.img)
    for line, assignments in image_recognizer.link_assignment.items():
        (start_x, start_y), (end_x, end_y) = line
        cv2.line(img, (start_x, start_y), (end_x, end_y), (255, 0, 0), 2)  # Blue lines
        
        # Draw assigned circles
        if assignments[0] is not None:
            cv2.circle(img, assignments[0], 5, (0, 0, 255), -1)  # Red for first assignment
        if assignments[1] is not None:
            cv2.circle(img, assignments[1], 5, (0, 0, 255), -1)  # Red for second assignment
    
    # Draw joint assignments
    for joint in image_recognizer.joint_assignment:
        cv2.circle(img, joint, 5, (255, 255, 0), -1)  # Yellow for joint assignments

    image_recognizer.show_image(img, "Check")
