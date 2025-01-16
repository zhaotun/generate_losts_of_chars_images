'''

本代码用于在背景图片中绘制数字或字符串以生成相应的合成图片，并同步生成对应的yolo格式标注文件。
可广泛用于字符识别等相关领域，能够自动生成任意数量的字符识别训练图片及其标注文件，快速扩充数据集。
主要特点有：
1、可根据实际需要自由指定待生成的字符列表、字符串长度、字符串数量、生成的图片数量等；
2、可根据实际需要自由指定字体列表；
3、可根据实际需要自由指定背景图片目录；
4、可根据实际需要自由指定生成字符的颜色；
5、如果代码对你有用，请给我一颗小星星；

'''

#载入必要的模块
import pygame
import random
import glob
import os,sys
import cv2
from pathlib import Path
import numpy as np

str_len  = 6     # 每个字符串的长度，按需修改
num_str  = 10    # 每张图片生成的字符串数量，按需修改
num_imgs = 10    # 期望生成的图片数量，按需修改

# 生成的字符列表，按需修改
chars_list = ['0','1','2','3','4','5','6','7','8','9']# ,'a','B','#','.']

# 字体列表，按需修改
my_fonts = ["fonts/alarm clock.ttf","fonts/digital-7.ttf","fonts/DS-DIGI.ttf","fonts/Technology-Italic.ttf","fonts/Technology.ttf"]

# 背景图片目录列表，按需修改
background_img_paths = ['background_images_01','background_images_02']

# 生成文件保存目录，按需修改
generated_path = "generated_files"

    
# 特定字符颜色，按需修改
RED    = ( random.randint(254,255), random.randint(50,100), random.randint(0,6) )
GREEN  = ( random.randint(45,55), random.randint(254,255), random.randint(0,15) )
BLACK  = ( random.randint(0,5), random.randint(0,5), random.randint(0,5) )
WHITE  = ( random.randint(250,255), random.randint(250,255), random.randint(250,255) )
YELLOW = ( random.randint(254,255), random.randint(254,255), random.randint(10,255) )

# 随机字符颜色
random_color =( random.randrange(0,255,2), random.randrange(0,255,2), random.randrange(0,255,2)  )

# 字符颜色列表，按需修改
COLORS = [RED, GREEN ]

# 从 char_list 中随机取出 char_num 个字符组成字符串
def create_chars(char_list, char_num):
    text = ''
    for i in range(char_num):
        text = text + random.choice(char_list)
    return text

#转换为yolo需要的标注格式
def convert(size, box_xxyy):
    dw = 1 / size[0]
    dh = 1 / size[1]    
    xmin,xmax,ymin,ymax = box_xxyy[0],box_xxyy[1],box_xxyy[2],box_xxyy[3]
    center_x = ((xmin + xmax) / 2) * dw
    center_y = ((ymin + ymax) / 2) * dh
    bbox_width = (xmax-xmin) * dw
    bbox_height = (ymax-ymin) * dh
    return (center_x,center_y,bbox_width,bbox_height)

# 生成字符串图片
def create_text_img(char_list, char_num, color=(255,0,0)):

    font_color = color
    font_size  = random.randint(40,250)# 字体大小
    text = create_chars(char_list, char_num)# 生成字符串
    print('text = ',text)

    font  = pygame.font.Font( random.choice(my_fonts) ,font_size)
    text_img = font.render(text,True,font_color)#透明背景
    
    metrics = font.metrics(text)
    height  = font.get_height()

    char_boxes = []
    x = 0
    for j, (minx, maxx, miny, maxy, advance) in enumerate(metrics):
        y = 0 
        char_boxes.append( (x,y,advance, height, text[j]) ) 
        x += advance

    return text,text_img,char_boxes


if __name__ == '__main__':
    
    pygame.init() 
    
    image_files = []
    for path in background_img_paths:
        for file in Path(path).rglob('*.jpg'):
            image_files.append(file)
    print('len(image_files) = ',len(image_files))
    
    # 生成图片保存目录
    dst_img_path = generated_path + "/images/"
    if not Path(dst_img_path).exists():
        Path(dst_img_path).mkdir(parents=True, exist_ok=True) 

    # 生成标注文件保存目录
    dst_label_path = generated_path + "/labels/"
    if not Path(dst_label_path).exists():
        Path(dst_label_path).mkdir(parents=True, exist_ok=True) 
        
    for i in range(num_imgs):
        file = random.choice(image_files)
        print('--file = ',file)
        img = cv2.imdecode(np.fromfile( str(file) ,dtype=np.uint8),-1) # 可读取中文路径，功能同cv2.imread 
        img_height, img_width,  _  = img.shape
        
        background = pygame.image.load( file )#加载背景图片

        txt_name = dst_label_path + str(file.stem) + '_' + str(i) + '.txt'
        txt_file = open(txt_name, 'w')
        
        line = ''
        pos_list = []
        for j in range(num_str):#每张图片生成的字符组数

            text, text_img, char_boxes = create_text_img(chars_list, str_len, random.choice(COLORS))#生成数字串

            width  = text_img.get_width()
            height = text_img.get_height()
            max_X = img_width  - 10 - width
            max_y = img_height - 10 - height
            if max_X<0 or max_y<0:
                continue
            
            tmp_x = random.randint(0,max_X)
            tmp_y = random.randint(0,max_y)
            tmp_rect = pygame.Rect(tmp_x,tmp_y,width,height)

            indices = tmp_rect.collidelistall( pos_list ) # tmp_rect是否与pos_list中的所有rect相交
            if len(indices) == 0:
                pos_X = tmp_x
                pos_Y = tmp_y
                pos_list.append((pos_X,pos_Y,width,height))
                textpos=( pos_X , pos_Y )
                background.blit(text_img,textpos)#将生成的数字添加到背景图片中
                
                for j, (x, y, w, h, char) in enumerate(char_boxes):
                    x1,x2,y1,y2 = x+ pos_X, x+ pos_X + w, y+ pos_Y, y+ pos_Y + h
                    box_xxyy = (x1,x2,y1,y2) 
                    
                    box_yolo = convert((img_width,img_height), box_xxyy)
                    label = str(chars_list.index( char ))
                    line += '{} {} {} {} {}'.format(label,box_yolo[0],box_yolo[1],box_yolo[2],box_yolo[3]) + '\n'

        txt_file.write(line)
        
        #保存最终图片
        new_image = dst_img_path +  str(file.stem) + '_' + str(i) + '.jpg'
        pygame.image.save(background,  new_image )
