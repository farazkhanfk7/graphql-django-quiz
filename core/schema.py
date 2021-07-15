import graphene
from graphene.types.mutation import Mutation
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
        fields = ("question","answer_text","is_right")


class Query(graphene.ObjectType):
    
    # all_quiz = DjangoListField(QuizType) this works as well but with objects.get() / single
    all_quiz = graphene.List(QuizType, id=graphene.Int())
    all_answer = graphene.List(AnswerType, id=graphene.Int())
    all_question = graphene.List(QuestionType, id=graphene.Int())

    def resolve_all_quiz(root, info, id):
        return Quiz.objects.filter(id=id)

    def resolve_all_question(root, info, id):
        return Question.objects.filter(id=id)
    
    def resolve_all_answer(root, info, id):
        return Answer.objects.filter(question=id)

    # def resolve_all_question(root, info):
    #     return Question.objects.all()

class CategoryMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)

    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls, root, info, name):
        category = Category(name=name)
        category.save()
        return CategoryMutation(category=category)


class Mutation(graphene.ObjectType):
    add_category = CategoryMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)