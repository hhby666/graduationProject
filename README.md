# 本科毕设: 基于深度学习的人脸识别签到系统

## 介绍

使用[face_recognition库](https://github.com/ageitgey/face_recognition)进行人脸识别，使用MySQL进行数据库搭建，使用PyQt5进行界面开发。

## 目录结构

> ├─qt
> │  └─ui
> ├─resources
> └─tool

qt下存放界面逻辑代码，ui中存放PyQt5界面代码

resources中存放资源文件

tool中存放工具类

## 安装运行

使用pip下载依赖

```cmd
pip install -r requirements.txt
```

打开mysql连接执行resources中的sql脚本完成建库，修改tool目录下的config配置为自己的邮箱和数据库。

运行main.py即可运行。