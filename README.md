# FishMOT
## Fish multi-target tracking based on yolo
## Please wait for the paper to be published for all codes

---
Bilibili video address [Fish multi-target tracking](https://www.bilibili.com/video/BV1Ap4y1n7XW/)<br>
![2023-09-04 105901](https://github.com/gakkistar/FishMOT/assets/92698686/c2079038-846e-4ac9-a2c9-a33fa31a83d6)

Bilibili video address [100 and 10 fish tracking videos](https://www.bilibili.com/video/BV1SV411T7r9/)

## Performance
---
The tracking results of 10 fish in a 300-frame video using 10 different methods.
<img width="710" alt="截屏2023-09-04 09 04 10" src="https://github.com/gakkistar/FishMOT/assets/92698686/0024af03-f073-42e2-ab55-b76b1d4ac352">

---
The tracking results of 100 fish in a 300-frame video using 10 different methods.
<img width="713" alt="截屏2023-09-04 09 04 19" src="https://github.com/gakkistar/FishMOT/assets/92698686/ca87e720-0b35-4ee4-a211-d00bf7bd6384">

---
The tracking results obtained by 10 and 100 fish in a 300-frame video using 3 algorithms.
<img width="629" alt="截屏2023-09-04 09 04 30" src="https://github.com/gakkistar/FishMOT/assets/92698686/c214d095-9608-48e9-9d92-171faab47213">

## overview

---
![image](https://github.com/gakkistar/FishMOT/assets/92698686/a5a7c3eb-1928-4f63-9270-b662bc5d3ff7)



## Training detection model View yolov7

---
YOLOv7 Training dataset preparationx

YOLOv7 Training<br>
&nbsp;&nbsp;&nbsp;&nbsp;[Yolov7 training process](https://github.com/WongKinYiu/yolov7)

Use of FishMOT:<br>
&nbsp;&nbsp;&nbsp;&nbsp;Use yolo first to get results
```commandline
python tack.py --fish_num 10 --path fish_10
```
    
