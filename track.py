import os
import cv2
import shutil
import argparse
import numpy as np
from utils.draw import draw_id_tracklets
from utils.fileType import is_image, is_video, video2image, delete_pos

from compuse_distance import image2video, all_iou_data, match_fish_id
from fish_iou import match_fish, unmatch_fish, save_positions, match_fish_byid, match_fishes, match_fish_po1




def track():
    fish_num, path, module, save_video = args.fish_num, args.path, args.module, args.save_video
    if is_video(path) & save_video:
        print('Preparing')
        video2image(path)

    image_path = path + '/1.jpg'
    imgsi = cv2.imread(image_path)

    height = imgsi.shape[0]
    width = imgsi.shape[1]
    img_total = []
    txt_total = []
    file = os.listdir(path)
    for filename in file:
        first, last = os.path.splitext(filename)
        if last == ".jpg":
            img_total.append(first)
        else:
            txt_total.append(first)
    n = 1
    now_pos = np.loadtxt(path + '/' + '1.txt')
    now_pos = np.delete(now_pos, 0, axis=1)
    fish_num = now_pos.shape[0]
    result = np.zeros((fish_num, 2))
    for i in range(fish_num):
        result[i][1] = i
        result[i][0] = i

    # frame = len(img_total)
    frame = 10
    print(len(img_total))

    for i in range(1, frame + 1):
        id_by_frame = []
        if i in range(1, frame + 1):
            filename_img = str(i) + ".jpg"
            path1 = os.path.join(path, filename_img)
            img = cv2.imread(path1)
            img = cv2.resize(img, (width, height), interpolation=cv2.INTER_CUBIC)  # resize 图像大小，否则roi区域可能会报错
            filename_txt = str(i) + ".txt"

            next_pos = np.loadtxt(path + '/' + filename_txt)
            next_pos = np.delete(next_pos, 0, axis=1)
            if next_pos.shape[0] != fish_num:
                for sub_num in range(0, fish_num - next_pos.shape[0]):
                    tep_num = [[0.001 + (0.01 * (sub_num - 1)), 0.001, 0.001, 0.001, 0.9]]
                    next_pos = np.append(next_pos, tep_num, axis=0)

            index, iou_data, fish_id, miss1_frame = all_iou_data(now_pos, next_pos, fish_num, result, width, height, i)
            dict_iou, miss_frame = match_fish_po1(iou_data, fish_id, miss1_frame)
            id_by_frame.append(dict_iou)
            save_positions(dict_iou, 'pos_inf/pos_{}.txt'.format(i), i - 1)
            error_data = 0
            fs = 0
            for dict in range(len(dict_iou)):
                if dict_iou[dict][1][3] == 4.5:
                    print(dict_iou)
                    true_data = set(())
                    print(dict_iou[dict][0])
                    for m in range(len(dict_iou)):
                        true_data.add(dict_iou[m][0])
                    for m in range(fish_num):
                        fs = fish_num
                        if m not in true_data:
                            print(m)

            for k in range(fs):
                if index[k][1] > 1000:
                    print('this is {}'.format(i))
                    index[k][1] = index[k][1] - 10000
                    error_data = 1
            if error_data == 0:
                for u in range(len(dict_iou)):
                    result[u][0] = u
                    result[u][1] = int(dict_iou[u][0])

            aa = next_pos
            now_pos = aa
            n += 1
        else:
            continue


    match_fish_id('pos_inf', frame, '', fish_num)
    draw_id_tracklets(path, 'pos_inf', frame-1, width, height, fish_num, False)
    image2video('result/', width, height, path)





if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--fish_num', type=int, default=10)
    parser.add_argument('--path', type=str, default='fish_10_frame_500')
    parser.add_argument('--module', type=str, default='bbox', help='bbox, seg, bs')
    parser.add_argument('--save_video', type=bool, default=True)
    parser.add_argument('--draw_box', type=bool, default=False)
    args = parser.parse_args()
    delete_pos()
    track()

