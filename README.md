# Traditional-Chinese-Vertical-Recognition
基于百度OCR的中文古文繁体竖体识别


####################################
请勿用于商业用途！！！
####################################

注意：imgs_save 中保存的是临时图片，默认100张后清空
注意：生成的文件 和记录保存在word_save 中，请不要删除csv文件，此为工程的记录

需要更改的值
关于setting文件 参数说明

{
  "API_KEY": ["Cup0QivPUY7qdFfZ8G1sTBoL", "aoOUWMQA6htzw6se1eqvKosd"],
  "SECRET_KEY": ["LAuvWngbow5Ok4p0CrWm2SUWmxap2jOM", "jOySMyhnFC84MwnZLIkk7GWrDCrsZusn"],
  "imgs_dir": "E:\\张悠然\\2023-2-13\\嘉道卷\\0206",
  "acc_loc": false,
  "task_name": "06",
  "word_save": "word_save",
  "img_temp": "img_temp",
  "dpi" : 300,
  "sort_way": "string"
}

图片大小限制  高精度 10M  标准 4M


API_KEY  填入申请的api
SECRET_KEY 填入对应的密码
imgs_dir :  照片所在文件夹的绝对地址
acc_loc： bool类型， 选择是高精度（True）(每个账户每月500张)，还是普通精度（False）
task_name : 同一个task name会记录已经完成的照片，可以中断后继续。任意起名即可
dpi : 保存图片的清晰度，默认300.
sort_way: 两种  string 或者  int  按照图片的string来排序，或者按照整数类型排序
