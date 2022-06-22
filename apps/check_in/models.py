from turtle import mode
from django.db import models

# Create your models here.
def face_path(instance, filename):
    return 'student_faces/{}'.format(filename)

class Student(models.Model):

    student_id = models.CharField('学号', max_length=50, primary_key=True)
    name = models.CharField('姓名',max_length=50 )
    time = models.DateTimeField('签到时间' ,auto_now=True, null=True)
    face = models.ImageField('人脸图片',upload_to=face_path, null=False, blank=True)
    is_face_check = models.BooleanField('人脸识别是否通过', default=False)
    is_mask_check = models.BooleanField('人脸识别是否通过', default=False)

    def __str__(self):
        status = (self.is_face_check and self.is_mask_check)
        if status:
            return f"{self.student_id} - {self.name} - 已签到 - 签到时间：{str(self.time)} "
        else:
            return f"{self.student_id} - {self.name} - 未签到"
