import numpy as np
import cv2
import scipy

read_path='data/'

img_width, img_height = 1500, 843

imgEx='.jpg'
focusDisArr=np.load('focusDisArr.npy')

list_of_img=[]

scene = ['Scene1', 'Scene3', 'Scene4', 'Scene5', 'Scene6', 'Scene6', 'Scene7', 'Scene8', 'Scene9', 'Scene9', 'Scene10','Scene9', 'Scene10']
frame_num = [2, 25, 13, 1, 38, 64, 50, 1, 66, 1,1, 89]
for sc in range(len(scene)):
    print(scene[sc])
    list_of_img=[]
    i = frame_num[sc]
    for j in range(0,len(focusDisArr)):
        temp_image = cv2.imread(read_path+scene[sc]+'/IMAGE_'+str(i).zfill(2)+'_'+focusDisArr[j]+imgEx,-1)
        temp_image_resized=cv2.resize(temp_image,(img_width, img_height))[:,:,::-1]
        list_of_img.append(temp_image_resized)

    img_all = np.asarray(list_of_img)

    #calculaate sharpness info
    sharpnessStack = np.empty((img_all.shape[0:3]))
    for i, img in enumerate(img_all):
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_gray = img_gray.astype(np.float64)
        x = scipy.ndimage.sobel(img_gray, axis=0)
        y = scipy.ndimage.sobel(img_gray, axis=1)
        sharpnessStack[i] = np.sqrt(x ** 2 + y ** 2)

    convFilter = np.ones((100, 100))
    convolvedSharpnessStack = np.empty(
        (img_all.shape[0], img_all.shape[1] - convFilter.shape[0] + 1, img_all.shape[2] - convFilter.shape[1] + 1))
    for i, sharpnessIm in enumerate(sharpnessStack):
        convolvedSharpnessStack[i] = scipy.signal.convolve2d(sharpnessIm, convFilter, mode='valid')
        print(i)

    maxSharpnessMap = np.argmax(convolvedSharpnessStack, axis=0)
    np.save(f'Scene{sc+1}_max_sharpness_map.npy', maxSharpnessMap)
    np.save(f'Scene{sc+1}_sharpness_map.npy', convolvedSharpnessStack)

    np.save(f'Scene{sc+1}_images'.format(frame_num[sc]),img_all)