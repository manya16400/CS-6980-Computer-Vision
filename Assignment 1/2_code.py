import math
import cv2

# function to display the coordinates of
# of the points clicked on the image
def click_event(event, x, y, flags, params):
 
    # checking for left mouse clicks
    if event == cv2.EVENT_LBUTTONDOWN:
 
        # displaying the coordinates
        # on the Shell
        x_im_points.append(x)
        y_im_points.append(y)
        print(x, ',', y)
 
        # displaying the coordinates
        # on the image window
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img, str(x) + ',' +
                    str(y), (x,y), font,
                    1, (255, 0, 0), 2)
        cv2.imshow('image', img)
        
#focal length values obtained after camera calibration in Part A Q1
fx = 2984.2
fy = 2980.4

#distance between object and camera (in pixels)
z = 27*38

# reading the image
img = cv2.imread('02_data/16647607724546.jpeg', 1)

# displaying the image
cv2.imshow('image', img)

#initializng image points list
x_im_points = []
y_im_points = []
print("The two (x,y) image points for the length of cuboid are (Image coordinates): ")
cv2.setMouseCallback('image', click_event)

cv2.waitKey(0)
cv2.destroyAllWindows()

#Euclidian distance (length of cuboid) from image points
print("\nLength of cuboid using image points: ",math.dist([x_im_points[0],y_im_points[0]], [x_im_points[1],y_im_points[1]]))

#initializing world points list
x_w_points = [0]*len(x_im_points)
y_w_points = [0]*len(y_im_points)

print("\nCorresponding world coordinates of the image points are: ")
#computing world points
for i in range(len(x_im_points)):
    x_w_points[i] = (fx*x_im_points[i])/z
    y_w_points[i] = (fy*y_im_points[i])/z
    print(x_w_points[i], ',',y_w_points[i])   
