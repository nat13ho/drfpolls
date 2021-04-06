from rest_framework import serializers

from drfpolls.apps.tasks.models import Task, Homework


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'task_name', 'task_text')


class HomeworkSerializer(serializers.ModelSerializer):
    task = TaskSerializer(read_only=True)
    profile = serializers.StringRelatedField(read_only=True)
    homework_status = serializers.SerializerMethodField()

    def validate_file(self, file):
        max_file_size = 2e6
        file_extension = file.name.split('.').pop()
        if file_extension != 'txt':
            raise serializers.ValidationError('Supported file formats: .txt')
        if file.size > max_file_size:
            raise serializers.ValidationError('Max file size is 2MB.')
        return file

    class Meta:
        model = Homework
        fields = ['id', 'task', 'profile', 'file', 'homework_status', 'mark', 'mark_description']
        read_only_fields = ['id', 'task', 'profile', 'homework_status', 'mark', 'mark_description']

    def get_homework_status(self, obj):
        return Homework.Status(obj.homework_status).label
