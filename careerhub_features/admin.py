from django.contrib import admin
from .models import Question, UserQuestion, Resume, Roadmap

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'topic', 'created_at')
    list_filter = ('topic',)
    search_fields = ('title', 'topic')

@admin.register(UserQuestion)
class UserQuestionAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'is_done', 'completed_at')
    list_filter = ('is_done', 'user', 'question__topic')
    search_fields = ('user__username', 'question__title')

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('title', 'pick', 'authorname', 'created_at')
    list_filter = ('pick', 'authorname')
    search_fields = ('title', 'description', 'authorname')
    ordering = ('-created_at',)

@admin.register(Roadmap)
class RoadmapAdmin(admin.ModelAdmin):
    list_display = ('fieldname', 'created_at')
    search_fields = ('fieldname',)
    ordering = ('-created_at',)
