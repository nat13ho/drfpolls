from django.contrib import admin

from apps.polls.models import (Category, Question, Answer,
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
    autocomplete_fields = ('question',)

    def get_test(self, obj: Choice):
        return obj.question.test

    get_test.short_description = 'test'


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'choice', 'question', 'get_test')
    list_display_links = ('id', 'user')
    search_fields = ('choice', 'question')
    autocomplete_fields = ('choice', 'question')

    def get_test(self, obj: Answer):
        return obj.question.test

    get_test.short_description = 'test'


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'avg_test_mark', 'avg_homework_mark')
    list_display_links = ('id', 'user')
    search_fields = ('user',)


class ProfileTestAdmin(admin.ModelAdmin):
    list_display = ('id', 'test', 'profile', 'created_at', 'mark')
    list_display_links = ('id', 'test')
    autocomplete_fields = ('test', 'profile')


class TestAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


admin.site.register(Category)
admin.site.register(Test, TestAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(ProfileTest, ProfileTestAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(Answer, AnswerAdmin)
