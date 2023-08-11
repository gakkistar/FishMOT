import math
import numpy as np
import cv2
import os

def min_distance(now_pos, next_pos, num):
    result = 0
    idx = 2
    for i in range(num):
        x = math.pow((now_pos[0] - next_pos[i][0]), 2)
        y = math.pow((now_pos[1] - next_pos[i][1]), 2)
        w = math.pow((now_pos[2] - next_pos[i][2]), 2)
        h = math.pow((now_pos[3] - next_pos[i][3]), 2)
        sum = x + y + w + h
        # sum = x + y + h
        if(sum < idx):
            sum, idx = idx, sum
            result = i

    return result


def image2video(path, width, height, path_name):
    # 1.每张图像大小
    size = (width, height)
    print("每张图片的大小为({},{})".format(size[0], size[1]))
    # 2.设置源路径与保存路径
    src_path = './' + path
    sav_path = 'video_{}.mp4'.format(path_name)
    # 3.获取图片总的个数
    all_files = os.listdir(src_path)
    index = len(all_files)
    print("图片总数为:" + str(index) + "张")
    # 4.设置视频写入器
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # MP4格式
    # 完成写入对象的创建，第一个参数是合成之后的视频的名称，第二个参数是可以使用的编码器，第三个参数是帧率即每秒钟展示多少张图片，第四个参数是图片大小信息
    videowrite = cv2.VideoWriter(sav_path, fourcc, 30, size)  # 2是每秒的帧数，size是图片尺寸
    # 5.临时存放图片的数组
    img_array = []

    # 6.读取所有jpg格式的图片 (这里图片命名是0-index.jpg example: 0.jpg 1.jpg ...)
    for filename in [src_path + r'{0}.jpg'.format(i) for i in range(1, index)]:
        img = cv2.imread(filename)
        if img is None:
            print(filename + " is error!")
            continue
        img_array.append(img)
    # 7.合成视频
    for i in range(0, index-1):
        img_array[i] = cv2.resize(img_array[i], (width, height))
        videowrite.write(img_array[i])
        if(i%100==0):
            print('第{}张图片合成成功'.format(i))
    print('------done!!!-------')


def compute_tangle(width, height, pos):
    x_left = width * float(pos[0])  # 左上点的x坐标
    y_left = height * float(pos[1])  # 左上点的y坐标
    width = int(width * float(pos[2]))  # 图片width
    height = int(height * float(pos[3]))  # 图片height
    if(width<20):
        width = width * 1.5
    if (height < 20):
        height = height * 1.5
    x_right = x_left + width
    y_right = y_left + height
    rec = [x_left, y_left, x_right, y_right, width, height]
    return rec


def max_iou(now_pos, next_pos, num, width, height):
    result = 0
    idx = -1
    # width = 3712
    # height = 3712
    now_rec = compute_tangle(width, height, now_pos)
    # f = open(r'iou_12.txt', 'a', encoding='UTF-8')
    for i in range(num):
        next_rec = compute_tangle(width, height, next_pos[i])
        iou = compute_iou(now_rec, next_rec)
        if(iou > idx):
            idx = iou
            result = i
    if(idx==0):
        print('*'*30)
        return result + 10000
        now_rec = compute_tangle(width*2, height*2, now_pos)
        for i in range(num):
            next_rec = compute_tangle(width, height, next_pos[i])
            iou = compute_iou(now_rec, next_rec)
            if (iou > idx):
                idx = iou
                result = i

    return result


def all_max_iou(now_pos, next_pos, num, result, width, height):
    # result = np.zeros((num, 2))
    # width = 3712
    # height = 3712
    for i in range(num):
        idx = -0.01
        # result[i][0] = i
        now_rec = compute_tangle(width, height, now_pos[int(result[i][0])])
        for j in range(num):
            next_rec = compute_tangle(width, height, next_pos[j])
            iou = compute_iou(now_rec, next_rec)
            if(iou > idx):
                idx = iou
                result[i][1] = j
        if(idx==0):
            result[i][1] = j + 10000

    # print(result)
    return result


def all_iou_data(now_pos, next_pos, num, result, width, height, frame):
    # result = np.zeros((num, 2))
    iou_info = {}
    fish_id = {}
    # width = 3712
    # height = 3712
    for i in range(num):
        idx = -0.01
        fish_info = []
        # result[i][0] = i
        now_rec = compute_tangle(width, height, now_pos[int(result[i][0])])
        fish_id[int(result[i][0])] = (now_rec[0], now_rec[1], now_rec[4], now_rec[5])
        for j in range(num):
            next_rec = compute_tangle(width, height, next_pos[j])
            iou = compute_iou(now_rec, next_rec)
            fish_info.append((j, iou))
            if(iou > idx):
                idx = iou
                result[i][1] = j
        if(idx==0):
            result[i][1] = j + 10000

        iou_info[int(result[i][0])] = fish_info
    # print(result)
    # print(fish_id)
    return result, iou_info, fish_id, frame

def compute_iou(rec_1, rec_2):
    '''
    rec_1:左上角(rec_1[0],rec_1[1])    右下角：(rec_1[2],rec_1[3])
    rec_2:左上角(rec_2[0],rec_2[1])    右下角：(rec_2[2],rec_2[3])
    '''

    s_rec1 = (rec_1[2]-rec_1[0])*(rec_1[3]-rec_1[1])   #第一个bbox面积 = 长×宽
    s_rec2 = (rec_2[2]-rec_2[0])*(rec_2[3]-rec_2[1])   #第二个bbox面积 = 长×宽
    sum_s = s_rec1+s_rec2                              #总面积
    left = max(rec_1[0], rec_2[0])                      #并集左上角顶点横坐标
    right = min(rec_1[2], rec_2[2])                     #并集右下角顶点横坐标
    bottom = max(rec_1[1], rec_2[1])                    #并集左上角顶点纵坐标
    top = min(rec_1[3], rec_2[3])                       #并集右下角顶点纵坐标
    if left >= right or top <= bottom:               #不存在并集的情况
        return 0
    else:
        inter = (right-left)*(top-bottom)              #求并集面积
        iou = (inter/(sum_s-inter))*1.0                #计算IOU
        return iou


def dict_to_np(id_dict):
    index = np.zeros((len(id_dict), 2))
    for i in range(len(id_dict)):
        index[i][0] = i
        index[i][1] = id_dict[i]
    return index


def match_fish_id(path, num, write_path, fish_num):
    # fish_num = 8 /       #此处的8是鱼类数量，后期需要修改
    path = path + '/'
    for i in range(1, num):
        filename_txt = 'pos_{}.txt'.format(str(i))
        id_re = np.zeros((fish_num, 6))
        id2_re = np.zeros((fish_num, 6))
        with open(os.path.join(path, filename_txt), "r+", encoding="utf-8", errors="ignore") as f:
            j = 0
            for line in f:
                aa = line.split(" ")
                id_re[j][0] = aa[0]
                id_re[j][1] = aa[1]
                id_re[j][2] = aa[2]
                id_re[j][3] = aa[3]
                id_re[j][4] = aa[4]
                id_re[j][5] = aa[5]
                j += 1
        filename1_txt = 'pos_{}.txt'.format(str(i+1))
        with open(os.path.join(path, filename1_txt), "r+", encoding="utf-8", errors="ignore") as f:
            l = 0
            for line in f:
                aa = line.split(" ")
                id2_re[l][0] = aa[0]
                id2_re[l][1] = aa[1]
                id2_re[l][2] = aa[2]
                id2_re[l][3] = aa[3]
                id2_re[l][4] = aa[4]
                id2_re[l][5] = aa[5]
                l += 1

        file = open(path + 'pos_{}.txt'.format(str(i + 1)), 'w').close()
        file = open(path + 'pos_{}.txt'.format(str(i)), 'w').close()
        # print(id_re)
        # print(id2_re)
        for k in range(len(id_re)):
            for o in range(len(id2_re)):
                if(id2_re[o][0]==id_re[k][1]):
                    # with open(write_path + 'pos_{}.txt'.format(str(i)), 'a') as f:
                    #     f.write(f'{id_re[k][1]},{id_re[k][2]},{id_re[k][3]}\n')
                    with open(path + 'pos_{}.txt'.format(str(i)), 'a') as f:
                        f.write(f'{int(id_re[k][0])} {id_re[k][2]} {id_re[k][3]} {id_re[k][4]} {id_re[k][5]}\n')
                    with open(path + 'pos_{}.txt'.format(str(i+1)), 'a') as f:
                        f.write(f'{int(id_re[k][0])} {id2_re[o][1]} {id2_re[o][2]} {id2_re[o][3]} {id2_re[o][4]} {id2_re[o][5]}\n')




if __name__ == '__main__':
    # width = 1160
    # height = 938
    rec_1 = [0.48319, 0.0788913, 0.0922414, 0.0469083]                     #四个值分别为左上角顶点（x1,y1），右下角坐标（x2,y2）
    rec_2 = [0.465517, 0.0597015, 0.0672414, 0.0127932]
    rec_3 = [0.510345, 0.0772921, 0.0327586, 0.0479744]
    rec_4 = [0.503448, 0.0735608, 0.05, 0.0383795]

    # rec1 = compute_tangle(width, height, rec_1)
    # rec2 = compute_tangle(width, height, rec_2)
    # rec_3 = compute_tangle(width, height, rec_3)
    # rec_4 = compute_tangle(width, height, rec_4)
    # print(rec_1, rec_2)
    # print(rec1, rec2)
    # print(rec_3)
    # print(rec_4)
    # iou = compute_iou(rec1, rec2)
    # print(iou)
    image2video('test/', 3584, 3500)