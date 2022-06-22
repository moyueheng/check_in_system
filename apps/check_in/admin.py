from django.contrib import admin

# Register your models here.
import time

from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    actions = ['clear', 'already', ]

    def clear(self, request, queryset):
        queryset.update(is_face_check=False, is_mask_check=False)
        self.message_user(request, '修改成功')

    clear.short_description = '更改为“未签到”'
    clear.type = 'danger'
    def already(self, request, queryset):
        queryset.update(is_face_check=True, is_mask_check=True, time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) )
        self.message_user(request, '修改成功')

    already.short_description = '更改为“已签到”'
    already.type = 'danger'


admin.site.site_header = '签到系统后台'
admin.site.site_title = '人脸识别口罩识别签到系统后台'
admin.site.index_title = '我在后台首页'
