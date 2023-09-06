import os
import cv2
import shutil

def video2image():
    # 读取视频文件
    video = cv2.VideoCapture("video.mp4")

    # 初始化帧计数器
    frame_count = 0

    # 循环遍历视频的每一帧
    while video.isOpened():
        # 读取当前帧
        success, frame = video.read()
        # 如果读取成功，继续处理
        if success:
            # 生成图片文件名，格式为frame_0000.jpg, frame_0001.jpg, ...
            # image_name = f"frame_{frame_count:04d}.jpg"
            image_name = '{}.jpg'.format(frame_count)
            # 将当前帧保存为图片文件
            cv2.imwrite(image_name, frame)
            # 打印保存成功的信息
            print(f"Saved {image_name}")
            # 增加帧计数器
            frame_count += 1
        # 如果读取失败，退出循环
        else:
            break
    # 释放视频资源
    video.release()

def is_image(file):
    # 定义一个图片格式的列表
    image_extensions = [".jpg", ".jpeg", ".png", ".bmp", ".gif"]
    # 获取文件的扩展名
    extension = os.path.splitext(file)[1].lower()
    # 如果扩展名在图片格式的列表中，返回True，否则返回False
    return extension in image_extensions

# 定义一个函数，判断文件的扩展名是否为视频格式
def is_video(file):
    # 定义一个视频格式的列表
    video_extensions = [".mp4", ".avi", ".mov", ".mkv", ".flv"]
    # 获取文件的扩展名
    extension = os.path.splitext(file)[1].lower()
    # 如果扩展名在视频格式的列表中，返回True，否则返回False
    return extension in video_extensions


def delete_all_files(folder_path):
    if os.path.isdir(folder_path):
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            if os.path.isfile(item_path):
                os.remove(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
        shutil.rmtree(folder_path)
        return True
    else:
        return False



def delete_pos():
    delete_all_files('./pos_inf/')
    os.mkdir('./pos_inf')
