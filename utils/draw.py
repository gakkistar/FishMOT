import os
import cv2
import shutil
import numpy as np
from PIL import Image, ImageFont, ImageDraw

def draw_id_tracklets(img_path, txt_path, frame, width, height, fish_num, box):
    img_path = './' + img_path
    txt_path = './' + txt_path
    for i in range(1, frame - 1):
        img = cv2.imread(img_path + '/{}.jpg'.format(str(i)))
        print(img)
        # cv2.imshow('a', img)
        # cv2.waitKey()
        img = cv2.resize(img, (width, height), interpolation=cv2.INTER_CUBIC)
        bg = img
        chalk = ImageFont.truetype('Chalkduster.ttf', 26)
        img_pil = Image.fromarray(bg)
        draw = ImageDraw.Draw(img_pil)
        id_pos = np.zeros((fish_num, 3))

        pos_inf = np.loadtxt(txt_path + '/pos_{}.txt'.format(str(i + 1)))
        for k in range(0, pos_inf.shape[0]):

            fish_id = int(pos_inf[k][0]) + 1
            pos_x = float(pos_inf[k][1])
            pos_y = float(pos_inf[k][2])
            box_width = float(pos_inf[k][3])
            box_height = float(pos_inf[k][4])

            x_left = pos_x - 0.5 * box_width
            x_right = pos_x + 0.5 * box_width
            y_left = pos_y - 0.5 * box_height
            y_right = pos_y + 0.5 * box_height
            if box:
                draw.rectangle([(x_left, y_left), (x_right, y_right)], fill=None, outline="black", width=3)
            color_r = 0
            color_g = 0
            color_b = 0

            draw.text((pos_x - box_width, pos_y - box_height), str(fish_id), font=chalk, fill=(100, 100, 30))
            for txt in range(i - 10, i):
                if txt >= 1:
                    his_pos = np.loadtxt(txt_path + '/pos_{}.txt'.format(str(txt)))
                    for j in range(0, his_pos.shape[0]):
                        his_x = float(his_pos[j][1])
                        his_y = float(his_pos[j][2])
                        his_width = float(his_pos[j][3])
                        his_height = float(his_pos[j][4])

                        draw.text((his_x, his_y - 23), str('.'), font=chalk, fill=(100, 100, 30))
                        # draw.text((his_x-0.5*his_width, his_y-0.5*his_height), str('.'), font=chalk, fill=(100, 100, 30))
                        # draw.point((float(his_pos[j][1]), float(his_pos[j][2])), '#FF0000')

        bg = np.array(img_pil)
        cv2.imwrite('./result/{}.jpg'.format(i), bg)

