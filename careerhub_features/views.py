from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import Question, UserQuestion, Resume, Roadmap
from .serializers import QuestionSerializer, UserQuestionSerializer, ResumeSerializer, RoadmapSerializer

# Create your views here.

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Question.objects.all()
        topic = self.request.query_params.get('topic', None)
        if topic:
            queryset = queryset.filter(topic=topic)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        questions = []
        
        for question in queryset:
            user_question = UserQuestion.objects.filter(
                user=request.user,
                question=question
            ).first()
            
            question_data = QuestionSerializer(question).data
            question_data['is_done'] = user_question.is_done if user_question else False
            questions.append(question_data)
            
        return Response(questions)

    @action(detail=True, methods=['POST'])
    def toggle_done(self, request, pk=None):
        question = self.get_object()
        user_question, created = UserQuestion.objects.get_or_create(
            user=request.user,
            question=question
        )
        
        user_question.is_done = not user_question.is_done
        if user_question.is_done:
            user_question.completed_at = timezone.now()
        else:
            user_question.completed_at = None
        user_question.save()
        
        return Response({
            'is_done': user_question.is_done,
            'completed_at': user_question.completed_at
        })

class ResumeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Resume.objects.all()
        pick = self.request.query_params.get('pick', None)
        if pick:
            queryset = queryset.filter(pick=pick)
        return queryset

class RoadmapViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Roadmap.objects.all()
    serializer_class = RoadmapSerializer
    permission_classes = [IsAuthenticated]
