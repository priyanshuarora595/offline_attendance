from django.apps import AppConfig

class AttendanceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'attendance'
    
    def ready(self):
        from srcs import update_media
        update_media.update()
        