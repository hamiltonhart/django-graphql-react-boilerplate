import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
# from django.db.models import Q

from django.contrib.auth import get_user_model

class UserType(DjangoObjectType):
  class Meta:
    model = get_user_model()

# # Queries

class Query(graphene.ObjectType):
  users = graphene.List(UserType)
  me = graphene.Field(UserType)

  def resolve_users(self, info):
    user = info.context.user
    
    return get_user_model().objects.all()

  def resolve_me(self, info):
    user = info.context.user
    if user.is_anonymous:
      raise GraphQLError("Not Logged In!")

    return user

# # Mutations

class CreateUser(graphene.Mutation):
  user = graphene.Field(UserType)

  class Arguments:
    username = graphene.String(required=True)
    password = graphene.String(required=True)
    email = graphene.String(required=True)

  def mutate(self, info, username, password, email):
    user = get_user_model()(
      username=username,
      email=email
    )
    user.set_password(password)
    user.save()
    return CreateUser(user=user)

class UpdateUser(graphene.Mutation):
  user = graphene.Field(UserType)

  class Arguments:
    id = graphene.Int(required=True)
    username = graphene.String()
    email = graphene.String()

  def mutate(self, info, id, username, email):
    try:
      user = get_user_model().objects.get(pk=id)
    except:
      raise GraphQLError("User does not exist")

    user.username = username
    user.email = email
    user.save()
    return UpdateUser(user=user)


class Mutation(graphene.ObjectType):
  create_user = CreateUser.Field()
  update_user = UpdateUser.Field()