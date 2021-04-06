from django.contrib import admin

from drfpolls.apps.polls.models import (Category, Question, Answer,
                                        Choice, Test, ProfileTest, Profile)


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'question_text', 'max_points', 'category', 'test')
    list_display_links = ('id', 'question_text')
    search_fields = ('question_text', 'get_category')
    list_filter = ('category',)


class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'choice_text', 'is_correct', 'question', 'get_test')
    list_display_links = ('id', 'choice_text')
    search_fields = ('choice_text', 'question')

    def get_test(self, obj: Choice):
        return obj.question.test

    get_test.short_description = 'Test'


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'choice', 'question')
    list_display_links = ('id', 'user')
    search_fields = ('choice', 'question')


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'avg_test_mark', 'avg_homework_mark')
    list_display_links = ('id', 'user')
    search_fields = ('user',)


class ProfileTestTestAdmin(admin.ModelAdmin):
    list_display = ('id', 'test', 'profile', 'created_at', 'mark')
    list_display_links = ('id', 'test')


admin.site.register(Test)
admin.site.register(Category)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(ProfileTest, ProfileTestTestAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(Answer, AnswerAdmin)
