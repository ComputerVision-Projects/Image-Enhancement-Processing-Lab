from PIL import Image 
import numpy as np 
import cv2 as cv
class EdgeDetectors:

    def __init__(self,image):

        self.image=image 
        


    def apply_filter(self,img,detector_type):
        pad_image=self.image_padding(img) 
        if detector_type==0:
           return self.sobel_detector(pad_image)
        
        elif detector_type==1:
            return self.roberts_detector(pad_image)
        
        elif detector_type==2:
            return self.perwitt_detector(pad_image)
        
        else:
            return self.canny_detector(img)
            
      

    def image_padding(self,img):
        
        self.image=img

        image_height,image_width=img.shape 
        top_pad=1
        bottom_pad=1
        right_pad=1
        left_pad=1

        pad_color=0

        new_image_height=image_height+top_pad+bottom_pad
        new_image_width=image_width+right_pad+left_pad

        self.padded_image = np.zeros((new_image_height, new_image_width), dtype=img.dtype)  # No extra dimension


        self.padded_image[top_pad:top_pad+image_height,left_pad:left_pad+image_width]=img
        return self.padded_image


    def sobel_detector(self,padded_image):
        x_dir_kernal=np.array([
            [-1,0,1],
            [-2,0,2],
            [-1,0,1]
            ])
        
        y_dir_kernal=np.array(
            [[-1,-2,-1],
             [0,0,0],
             [1,2,1]]
             )
        
        height,width=self.image.shape

        output_image_x_dir = np.zeros((height, width), dtype=np.uint8)
        output_image_y_dir = np.zeros((height, width), dtype=np.uint8)
        output_image_edges = np.zeros((height, width), dtype=np.uint8)

        for i in range(height):
            for j in range(width): 

                roi=padded_image[i:i+3,j:j+3]

                result_x_dir=np.sum(roi*x_dir_kernal)
                result_y_dir=np.sum(roi*y_dir_kernal)

                gradient_magintude = np.sqrt(result_x_dir**2 + result_y_dir**2)  




                output_image_x_dir[i,j]=np.clip(result_x_dir,0,255)
                output_image_y_dir[i,j]=np.clip(result_y_dir,0,255)
                output_image_edges[i,j]=np.clip(gradient_magintude,0,255)

        return output_image_edges        







    def roberts_detector(self,padded_image):
        x_dir_kernal=np.array( 
                            [[ 0, 0, 0 ],
                             [ 0, 1, 0 ],
                             [ 0, 0,-1 ]] 
                             )
        
        y_dir_kernal=np.array( 
                            [[ 0, 0, 0 ],
                             [ 0, 0, 1 ],
                             [ 0,-1, 0 ]] 
                             )
        

        height,width=self.image.shape
        output_image_x_dir = np.zeros((height, width), dtype=np.uint8)
        output_image_y_dir = np.zeros((height, width), dtype=np.uint8)
        output_image_edges = np.zeros((height, width), dtype=np.uint8)
        for i in range(height):
            for j in range(width): 

                roi=padded_image[i:i+3,j:j+3]

                result_x_dir=np.sum(roi*x_dir_kernal)
                result_y_dir=np.sum(roi*y_dir_kernal)

                gradient_magintude = np.sqrt(result_x_dir**2 + result_y_dir**2) 




                output_image_x_dir[i,j]=np.clip(result_x_dir,0,255)
                output_image_y_dir[i,j]=np.clip(result_y_dir,0,255)
                output_image_edges[i,j]=np.clip(gradient_magintude,0,255)

        return output_image_edges   

    def perwitt_detector(self,padded_image):
        x_dir_kernal=np.array([
            [-1,0,1],
            [-1,0,1],
            [-1,0,1]
            ])
        y_dir_kernal=np.array(
            [[-1,-1,-1],
             [0,0,0],
             [1,1,1]]
             )
        height,width=self.image.shape
        output_image_x_dir = np.zeros((height, width), dtype=np.uint8)
        output_image_y_dir = np.zeros((height, width), dtype=np.uint8)
        output_image_edges = np.zeros((height, width), dtype=np.uint8)
        for i in range(height):
            for j in range(width): 

                roi=padded_image[i:i+3,j:j+3]

                result_x_dir=np.sum(roi*x_dir_kernal)
                result_y_dir=np.sum(roi*y_dir_kernal)

                gradient_magintude = np.sqrt(result_x_dir**2 + result_y_dir**2) 




                output_image_x_dir[i,j]=np.clip(result_x_dir,0,255)
                output_image_y_dir[i,j]=np.clip(result_y_dir,0,255)
                output_image_edges[i,j]=np.clip(gradient_magintude,0,255)

        return output_image_edges

    def canny_detector(self,image):

        image_median=np.median(image)
        low_thershold=min(0,0.5*image_median)
        high_thershold=max(255,1.5*image_median)

        image_edges=cv.Canny(image,low_thershold,high_thershold)     

        return image_edges 