import os

import pandas as pd
import time
class trial_data:
    def __init__(self):

        self.data = {'method': [], 'scene': [], 'objectword': [], 'x_eye': [], 'y_eye':[],
                     'x_im':[], 'y_im':[], 'best_index':[], 'current_index':[],
                     'best_sharpness':[], 'current_sharpness':[], 'gt_index':[], 'gt_sharpness':[],
                     'gt_x': [], 'gt_y': [], 'time': [], 'completed':[]}

    def addDataPoint(self, method, scene, objectword,
                     x_eye, y_eye, x_im, y_im, best_index, current_index,
                     best_sharpness, current_sharpness, gt_index,
                     gt_sharpness, gt_x, gt_y, completed):
        self.data["method"].append(method)
        self.data["scene"].append(scene)
        self.data["objectword"].append(objectword)
        self.data["x_eye"].append(x_eye)
        self.data["y_eye"].append(y_eye)
        self.data["x_im"].append(x_im)
        self.data["y_im"].append(y_im)
        self.data["best_index"].append(best_index)
        self.data["current_index"].append(current_index)
        self.data["best_sharpness"].append(best_sharpness)
        self.data["current_sharpness"].append(current_sharpness)
        self.data["gt_index"].append(gt_index)
        self.data["gt_sharpness"].append(gt_sharpness)
        self.data["gt_x"].append(gt_x)
        self.data["gt_y"].append(gt_y)
        self.data["completed"].append(completed)
        self.data["time"].append(time.time())

    def trial_data_out(self, fileoutname):
        df = pd.DataFrame(data=self.data)
        os.makedirs('trial_data', exist_ok=True)
        df.to_csv('trial_data/{}'.format(fileoutname))






