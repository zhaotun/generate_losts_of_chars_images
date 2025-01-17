# generate losts of chars images
Python code that can generate a large number of specified character images, which can be used in fields such as character recognition, to quickly expand the training dataset.

<div align="center">
  <img src="https://github.com/zhaotun/generate_losts_of_chars_images/blob/main/generated_files/images/biaoji-fenhejishu_1_2.jpg" alt="Description" width=50% height=50% />
</div>


This python code is used to draw chars on background images to generate corresponding synthetic images, while simultaneously creating annotation files in YOLO format.
It can be widely applied in fields such as character recognition, can automatically generate any number of training images and their corresponding annotation files,  quickly expanding the train dataset.

[配电房数字式仪表读数识别算法开发](https://zhuanlan.zhihu.com/p/18636177926)


**If you find it useful, please give me a star. Thank you!**


### Key features:

* freely specify the list of characters to be generated, the length of the characters, the number of characters, and the number of images to be generated, based on actual requirements.

* freely specify the list of fonts based on actual requirements.

* freely specify the directory of background images based on actual requirements.

* freely specify the color of the generated characters based on actual requirements.

### 1. install
pip install -r requirements.txt
### 2. run
python generate_chars_images.py

and then, generated images will be saved in generated_files/images, generated labels  will be saved in generated_files/labels. 

just enjoy！


### 3. other explames of generated images
<div align="center">
  <img src="https://github.com/zhaotun/generate_losts_of_chars_images/blob/main/generated_files/images/biaoji-fenhejishu_40_5.jpg" alt="Description" width=50% height=50% />
  <img src="https://github.com/zhaotun/generate_losts_of_chars_images/blob/main/generated_files/images/biaoji-fenhejishu_91_4.jpg" alt="Description" width=50% height=50% />
</div>

