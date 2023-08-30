# import os
# import sys
# import cv2
# import numpy as np
# import warnings
# from matplotlib import pyplot
# # from model.mymodel import CARB_CNN
# # from data_preprocess.data_ela import convert_to_ela_image
# from torchvision import transforms
# import torch
# from PIL import Image
# import tqdm
#
#
# class Infer:
#     def __init__(self, checkpoint=None):
#         self.checkpoint = checkpoint
#         self.img_size = (224, 224)
#         self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
#         self.init_model()
#
#         # """----定义类的属性----"""
#         # self.path = None
#         # self.flag = None
#         # self.conf = None
#
#
#     def init_model(self):
#         # self.model = CARB_CNN(self.img_size).to(self.device)
#         self.model = torch.mode(torch.tensor([0,0]))
#         self.model.eval()
#
#         if self.checkpoint:
#             self.model.load_state_dict(
#                 torch.load(self.checkpoint))
#         else:
#             return "can not load checkpoint , please check"
#
#     def infer_dir(self, imgs_dir):
#         imgs_ls = [[os.path.join(imgs_dir, path), 0, 0] for path in os.listdir(imgs_dir)]
#         imgs_ls = np.array(imgs_ls)
#         conf, pred_label = [],[]
#         for img_path in tqdm.tqdm(imgs_ls[:, 0]):
#             path, flag, confident = self.infer_image(img_path)
#             conf.append(confident)
#             pred_label.append(flag)
#
#         conf = np.array(conf)
#         imgs_ls[:, 1] = np.array(pred_label)
#         imgs_ls[:, 2] = conf
#         return imgs_ls
#
#
#     def infer_image(self, img_path):
#         """
#
#         :param img_path: 输入是图片的地址
#         :return:
#         """
#         transform = transforms.Compose([
#             transforms.Resize(self.img_size),
#             transforms.ToTensor()  # gpu中的数据类
#         ])
#         ela_image = transform(row_ela_image).to(self.device)
#         ela_image = torch.unsqueeze(ela_image, 0)  #  【3,224,224】  -》【1,3,224,224】
#         with torch.no_grad():
#             predict = self.model(ela_image)   # float 类型 【0-1】之间   sigmoid函数
#             pred = predict.cpu().detach().numpy().round()  # 四舍五入  》0.5 的就为 fake  ，小于就是real
#
#         flag = 'fake' if pred.item() == 1 else 'real'
#         predict = predict.squeeze().cpu().detach().numpy()
#
#         # """每次运行刷新类的属性来传递信号"""
#         # self.path = img_path
#         # self.flag = flag
#         # self.conf = predict
#
#         return [img_path, flag, predict]
#
#
# if __name__ == "__main__":
#     # Au 真， Tp， Sp，假   输出是假的概率
#     mod = Infer('checkpoint/epoch-56.pth')
#     predict = mod.infer_dir(r"F:\archive\CASIA1\Sp")
#     print(predict[:,1])
#     print(predict[:,2])
