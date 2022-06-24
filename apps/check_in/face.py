"""

python人脸识别测试

"""
import uuid
import face_recognition
import os
from os.path import join as pjoin
from tqdm import tqdm
import base64
import paddlehub as hub
import cv2


class Utils():
    # base64转换成图片
    @staticmethod
    def base2picture(base64_str, putout_path):
        # 分割字符串
        res = base64_str.split(',')[1] # 一定要去掉 data:image/jpg:base64,
        # 使用base64进行解码
        img_data = base64.b64decode(res)
        # 写到图片文件中
        with open(putout_path, 'wb') as f: 
            f.write(img_data)
            f.close()

    @staticmethod
    def draw_box(img_path, left, top, right, bottom, save_path):
        # 分割字符串
        img = cv2.imread(img_path)
        # img => 图片数据;
        # left_top => (最左,最上) 是个tuple;
        # right_bottom => [最右,最下] 是个tuple;
        # (0, 0, 255) => rgb 颜色;
        # 3 => 粗细程度
        cv2.rectangle(img, (left,top), (right, bottom) , (0, 0, 255), 3)
        cv2.imwrite(save_path, img)


class MaskDet():
    """口罩监测

    Returns:
        _type_: _description_
    """
    def __init__(self) -> None:
        self.mask_detector = hub.Module(name="pyramidbox_lite_server_mask")
        
    def det(self, img_path):
        """监测单张图片是否带口罩

        Args:
            img_path (str): 图片路径

        Returns:
            dict: {'label': 'NO MASK', 'confidence': 0.9999982118606567, 'top': 66, 'bottom': 149, 'left': 79, 'right': 147}
        """
        result = self.mask_detector.face_detection(paths = [img_path])[0]['data'][0]
        top = result['top']
        bottom = result['bottom']
        left = result['left']
        right = result['right']
        Utils.draw_box(img_path, left, top, right, bottom, f'/data/backup/expLiubo/myh/private/shixun/check_in_system/media/tmp/mask_box{uuid.uuid1()}.jpg')
        return result

class FaceDet():
    """人脸识别类
    """
    __instanc = None
    __flag = False

    def __init__(self, know_paths = [], know_names = []) -> None:
        if not FaceDet.__flag:
            FaceDet.__flag = True 
            # 保证只初始化一次
            print('已知人脸初始化中。。。。')
            self.face_encodings = self.__get_face_encodings(know_paths)
            self.know_paths = know_paths
            self.know_names = know_names
            print('已知人脸初始化完成')
            
        
    def __new__(cls, *args, **kwargs):
        """重写new，一定要携带 *args, **kwargs，
        Returns:
            _type_: _description_
        """
        if cls.__instanc is None:
            cls.__instanc = super().__new__(cls) # 这里只需要传 cls
        return cls.__instanc
    
    def remove(self, know_names):
        for i, know_name in enumerate(know_names):
            if know_name in self.know_names:
                del self.know_names[i]
                del self.face_encodings[i]
                del self.know_paths[i]

    def refresh(self, know_paths, know_names):
        for know_path, know_name in zip(know_paths, know_names):
            if know_name not in self.know_names:
                self.know_names.append(know_name)
                self.face_encodings.append(self.__get_face_encoding(know_path))
                self.know_paths.append(know_path)


    def who(self, unknown_path):
        """我是谁

        Args:
            unknown_path (str): 未知图片路径

        Returns:
            dict: {
                'name':''
                'score':''
            }
        """
        image_to_test_encoding = self.__get_face_encoding(unknown_path)
        if image_to_test_encoding is None:
            return None
        face_distances = face_recognition.face_distance(self.face_encodings, image_to_test_encoding)
        # 找到距离最小，且距离最小的小于0.5我们就认为成功了
        for i, face_distance in enumerate(face_distances):
            print(f'测试图片与{self.know_names[i]}的距离为{face_distance}')
        index = face_distances.argmin()
        min_distances = min(face_distances)
        if min_distances > 0.5:
            name = '外来人员，不允许签到'
            score = 0
        else:
            name = self.know_names[index]
            score = 1 - min_distances
        return {
            'name' : name,
            'score' : score
        }

    def __get_face_encodings(self, know_paths):
        face_encodings = []
        for know_path in tqdm(know_paths):
            face_encodings.append(self.__get_face_encoding(know_path))
        return face_encodings
    
    def __get_face_encoding(self, face_path):
        """获取人脸编码

        Args:
            face_path (str): 人脸路径

        Returns:
            face_encoding: face_encoding
            如果没有人脸会返回None
        """
        # 1. 读取图片
        img = face_recognition.load_image_file(face_path)
        # 2. 找到人脸的位置
        face_loc = face_recognition.face_locations(img)
        # 3. 返回人脸位置的编码
        faces = face_recognition.face_encodings(img)
        if not faces:
            return None
        face_encoding = face_recognition.face_encodings(img)[0]
        return face_encoding
