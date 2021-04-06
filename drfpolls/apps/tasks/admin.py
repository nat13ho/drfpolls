from django.contrib import admin

from drfpolls.apps.tasks.models import Homework, Task


class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'task_name', 'task_text')
    list_display_links = ('id', 'task_name')
    search_fields = ('task_name', 'task_text')


class HomeworkAdmin(admin.ModelAdmin):
    list_display = ('id', 'profile', 'task', 'get_status', 'mark')
    list_display_links = ('id', 'profile')

    def get_status(self, obj: Homework):
        return obj.homework_status

    get_status.short_description = 'Status'


admin.site.register(Task, TaskAdmin)
admin.site.register(Homework, HomeworkAdmin)
