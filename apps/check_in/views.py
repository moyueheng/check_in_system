from typing import Tuple
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View
from .face import Utils, FaceDet, MaskDet
from .models import Student
# Create your views here.
from contant import CONTANT, MSG
import uuid
def get_face_det():
    students = Student.objects.all()
    know_paths = []
    know_names = []
    for student in students:
        know_paths.append(student.face)
        know_names.append(student.name)
    face_det = FaceDet(know_paths, know_names)
    return face_det

mask_det = MaskDet()

face_det = get_face_det()


class IndexView(View):
    def get(self, request):

        return render(request, template_name='index.html')
        pass


class StudentsView(View):

    def get(self, request):
        students = Student.objects.all()
        ret = []
        for student in students:
            tmp = {
                'student_id' : student.student_id,
                'name' : student.name,
                'status' : (student.is_face_check and student.is_mask_check),
                'is_mask_check' : student.is_mask_check,
                'is_face_check' : student.is_face_check,
            }
            ret.append(tmp)
        return JsonResponse(ret, safe=False)

class FaceIdentifyView(View):
    


    def get(self, request):
        return HttpResponse('人脸识别页面')


    def post(self, request):
        # 获取base64字符串
        base64_str = request.POST.get('data')
        if not base64_str:
            return JsonResponse({
                'code' : CONTANT.NO_IMG,
                'msg'  : MSG[CONTANT.NO_IMG]
            })
        # 转成图片
        unknow_path = f'/data/backup/expLiubo/myh/private/shixun/check_in_system/media/tmp/face_tmp{uuid.uuid1()}.jpg'
        Utils.base2picture(base64_str, unknow_path)
        # 用人脸识别去识别图片
        ret = face_det.who(unknow_path)
        # 给这个人的状态改一下
        print(ret)
        if not ret :
            res_dict = {
                'code' : CONTANT.ON_FACE_INFO,
                'msg' : "截图的时候放入人脸图片"
            }
            return JsonResponse(res_dict)
        try:
            student = Student.objects.get(name =ret['name'])
        except:
            return JsonResponse({
                'code' : CONTANT.ON_FACE_INFO,
                'msg' : MSG[CONTANT.ON_FACE_INFO]
            })
        student.is_face_check = True
        student.save()
        ret['student_id'] = student.student_id
        ret['code'] = CONTANT.OK
        ret['msg'] = MSG[CONTANT.OK]
        res = JsonResponse(ret)
        res.set_cookie('student_id', student.student_id ) # 设置一个cookie，下次发过来就知道是谁在做口罩监测了
        return res


class MaskDetView(View):

    def get(self, request):
        return HttpResponse('口罩监测页面')


    def post(self, request):
        # 获取base64字符串
        base64_str = request.POST.get('data')
        if not base64_str:
            return JsonResponse({
                'code' : CONTANT.NO_IMG,
                'msg'  : MSG[CONTANT.NO_IMG]
            })
        # student_id = request.POST.get('student_id')
        student_id = request.COOKIES.get('student_id')
        if not student_id:
            return JsonResponse(
                {
                    'code' : CONTANT.FACE_FRIST,
                    'msg' : MSG[CONTANT.FACE_FRIST]
                }
            )
        try:
            student = Student.objects.get(student_id = student_id)
        except:
            return JsonResponse({
                'code' : CONTANT.ON_FACE_INFO,
                "msg" : MSG[CONTANT.ON_FACE_INFO]
            })
        # 转成图片
        unknow_path = f'/data/backup/expLiubo/myh/private/shixun/check_in_system/media/tmp/mask_tmp{uuid.uuid1()}.jpg'
        Utils.base2picture(base64_str, unknow_path)
        # 用人脸识别去识别图片
        ret = mask_det.det(unknow_path)
        # {'label': 'NO MASK', 'confidence': 0.9999982118606567, 'top': 66, 'bottom': 149, 'left': 79, 'right': 147}
        # 给这个人的状态改一下
        
        ret['student_id'] = student_id
        ret['name'] = student.name
        ret['code'] = CONTANT.OK
        ret['msg'] = MSG[CONTANT.OK]
        if ret['label'] == 'MASK':
            student.is_mask_check = True
            student.save()
        return JsonResponse(ret)