from skimage import transform
import sys
import numpy as np
import dlib
import cv2

def rect_to_bb(rect):
     x = rect.left()
     y = rect.top()
     w = rect.right() - x
     h = rect.bottom() - y
     return (x, y, w, h)

def shape_to_np(shape, dtype="int"):
     coords = np.zeros((68, 2), dtype=dtype)
     for i in range(0, 68):
        coords[i] = (shape.part(i).x, shape.part(i).y)
     return coords


def resize(image, width=1200):
     r = width * 1.0 / image.shape[1]
     dim = (width, int(image.shape[0] * r))
     resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
     return resized


print(len(sys.argv))
if len(sys.argv) < 2:
    print ("Usage: %s <image file>" % sys.argv[0])
    sys.exit(1)
image_file = sys.argv[1]
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")


image = cv2.imread(image_file)
image = resize(image, width=600)

#对图像进行放缩
from scipy import misc
# image = misc.imresize(image, 0.5) # 第二个参数如果是整数，则为百分比，如果是tuple，则为输出图像的尺寸
# image = transform.resize(image,(208,208))
# plt.imshow(lena_new_sz)
# plt.axis('off')
# plt.show()





gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
rects = detector(gray, 1)

for (i, rect) in enumerate(rects):
     shape = predictor(gray, rect)
     shape = shape_to_np(shape)
     (x, y, w, h) = rect_to_bb(rect)
     cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
     cv2.putText(image, "Face #{}".format(i + 1), (x - 10, y - 10),
     cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
     for (x, y) in shape:
        cv2.circle(image, (x, y), 2, (0, 0, 255), -1)
cv2.imshow("Output", image)
key = cv2.waitKey()
msg = '{} is pressed.'.format(chr(key) if key < 256 else key)
print(msg)