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
        id_ = graphene.ID(required=False)

    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls, root, info, name, id_=None):
        # If ID is present then update existing item
        if id_ is not None:
            category_ = Category.objects.get(id=id_)
            category_.name = name
            category_.save()
            return CategoryMutation(category=category_)
        #If ID is not present then add a new one
        category_ = Category(name=name)
        category_.save()
        # for deleting simply use category_.delete()
        return CategoryMutation(category=category_)

class QuizMutation(graphene.Mutation):
    class Arguments:
        title = graphene.String()
        category = graphene.ID()

    quiz = graphene.Field(QuizType)

    @classmethod
    def mutate(cls, root, info, title, category):
        quiz = Quiz(title=title,category_id=category)
        quiz.save()
        return QuizMutation(quiz=quiz)

# another way to take input from users
class QuestionInput(graphene.InputObjectType):
    title = graphene.String(required=True)
    quiz_id = graphene.ID(required=True)

class QuestionMutation(graphene.Mutation):
    class Arguments:
        question_data = QuestionInput(required=True)

    question = graphene.Field(QuestionType)

    @classmethod
    def mutate(cls, root, info, question_data):
        question_ = Question(**question_data)
        question_.save()
        return QuestionMutation(question=question_)

class Mutation(graphene.ObjectType):
    add_category = CategoryMutation.Field()
    add_quiz = QuizMutation.Field()
    add_question = QuestionMutation.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)