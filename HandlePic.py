import matplotlib.pyplot as plt # plt 用于显示图片
import matplotlib.image as mpimg # mpimg 用于读取图片
import numpy as np


#读取 显示图像
lena = mpimg.imread('123.png') # 读取和代码处于同一目录下的 lena.png
# 此时 lena 就已经是一个 np.array 了，可以对它进行任意处理
lena.shape #(512, 512, 3)

plt.imshow(lena) # 显示图片
plt.axis('off') # 不显示坐标轴
plt.show()



# 显示图片的第一个通道
# lena_1 = lena[:, :, 0]
# plt.imshow('lena_1')
# plt.show()
# # 此时会发现显示的是热量图，不是我们预想的灰度图，可以添加 cmap 参数，有如下几种添加方法：
# plt.imshow('lena_1', cmap='Greys_r')
# plt.show()
#
# img = plt.imshow('lena_1')
# img.set_cmap('gray') # 'hot' 是热量图
# plt.show()




#将 RGB 转为灰度图
def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.299, 0.587, 0.114])

gray = rgb2gray(lena)
# 也可以用 plt.imshow(gray, cmap = plt.get_cmap('gray'))
plt.imshow(gray, cmap='Greys_r')
plt.axis('off')
plt.show()



#对图像进行放缩
# from scipy import misc
# lena_new_sz = misc.imresize(lena, 0.5) # 第二个参数如果是整数，则为百分比，如果是tuple，则为输出图像的尺寸
# plt.imshow(lena_new_sz)
# plt.axis('off')
# plt.show()


# 保存图像
#保存 matplotlib 画出的图像
plt.imshow(lena)
plt.axis('off')
plt.savefig('lena_new_sz.png')

#将 array 保存为图像
from scipy import misc
misc.imsave('lena_new_sz.png', lena)
# 直接保存 array
np.save('lena_new_sz', lena) # 会在保存的名字后面自动加上.npy
img = np.load('lena_new_sz.npy') # 读取前面保存的数组