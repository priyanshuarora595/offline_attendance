from django import template
from attendance.models import StudentData , TeacherData


register = template.Library()


def user_group(group_name):
    data=group_name.objects.values_list('username',flat=True)
    return data
    
    

register.filter('user_group',user_group)
