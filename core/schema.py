import graphene
from graphene_django import DjangoObjectType
from graphene_django import DjangoListField
from .models import Category,Quiz,Question,Answer

class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ("id","name")

class QuizType(DjangoObjectType):
    class Meta:
        model = Quiz
        fields = ("id","title","category","question")

class QuestionType(DjangoObjectType):
    class Meta:
        model = Question
        fields = ("title","quiz")

class AnswerType(DjangoObjectType):
    class Meta:
        model = Answer
        fields = ("question","answer")


class Query(graphene.ObjectType):
    quiz = graphene.String()

    def resolve_quiz(root, info):
        return f"First question"


schema = graphene.Schema(query=Query)