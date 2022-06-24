# 基于人脸识别，口罩识别的签到系统
<p align="center"> <a href="https://www.djangoproject.com/" target="_blank" rel="noreferrer"> 
<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/django/django-original.svg" alt="django" width="40" height="40"/> </a>  <a href="https://pandas.pydata.org/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/2ae2a900d2f041da66e950e4d48052658d850630/icons/pandas/pandas-original.svg" alt="pandas" width="40" height="40"/> </a> <a href="https://pytorch.org/" target="_blank" rel="noreferrer"> <img src="https://www.vectorlogo.zone/logos/pytorch/pytorch-icon.svg" alt="pytorch" width="40" height="40"/> </a> <a href="https://www.tensorflow.org" target="_blank" rel="noreferrer"> <img src="https://www.vectorlogo.zone/logos/tensorflow/tensorflow-icon.svg" alt="tensorflow" width="40" height="40"/> </a> <a href="https://vuejs.org/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/vuejs/vuejs-original-wordmark.svg" alt="vuejs" width="40" height="40"/> </a> </p>

# 简介：
## 后端
- django 3.2
- simpleUI 
[simpleUI官网](https://simpleui.72wo.com/docs/simpleui/QUICK.htm)

## 前端
为本人前端不行，所以代码东拼西凑，凑的一个前端页面，前端代码有点乱
- VUE
- elementUI
- axios
- jQuery

## 环境
- ubuntu 20.04
- cuda11.2

# demo
[后台地址](https://checkin.coderxiaomo.top/admin)
账号：admin
密码：qsczsewsx123

[前台地址](https://checkin.coderxiaomo.top)

# 部分效果截图

## 前台
![](https://s2.loli.net/2022/06/24/HTxnj8oKOuRzUhE.png)
## 后台
![](https://s2.loli.net/2022/06/24/XKbxDjvIqY4h5p1.png)

# 食用方法
## 配置环境
细节请读者自行修改，我是基于自己的环境配置的，是基于conda的虚拟环境
- ubuntu 20.04
- cuda11.2
### 口罩识别环境
```sh
# 口罩检测环境
conda install paddlepaddle-gpu==2.3.0 cudatoolkit=11.2 -c https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/Paddle/ -c conda-forge 
pip install paddlehub==2.1.0


```

### 人脸识别环境
```sh
apt install cmake
pip3 install face_recognition
```
### django环境
```
pip install -r requirements.txt
```

### 数据库迁移
```
python manage.py makemigrations
python manage.py migrate
```
## 静态文件迁移
```
python manage.py collectstatic 
```
## 运行项目
```
python manage.py runserver 
```
这时候你就能在本地的 128.0.0.1:8000查看效果了

# 人脸识别
## face_recognition（使用中）

[face_recognition](https://github.com/ageitgey/face_recognition)

# 口罩监测

## FaceMaskDetection
待测试
[FaceMaskDetection](https://github.com/AIZOOTech/FaceMaskDetection)


## Face-Mask-Detection
待测试
[Face-Mask-Detection](https://github.com/chandrikadeb7/Face-Mask-Detection)

## ~~飞桨（使用中）~~
效果太差了，但是模型的体积很小，目前就在使用这个

https://github.com/PaddlePaddle/PaddleHub/blob/release/v2.2/docs/docs_ch/get_start/installation.rst
