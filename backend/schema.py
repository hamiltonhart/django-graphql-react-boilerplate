# import graphene
# import todo_list.schema

# class Query(todo_list.schema.Query, graphene.ObjectType):
#     # This class will inherit from multiple Queries
#     # as we begin to add more apps to our project
#     pass

# class Mutation(todo_list.schema.Mutation, graphene.ObjectType):
#     pass

# schema = graphene.Schema(query=Query, mutation=Mutation)



import graphene
import graphql_jwt
import users.schema

class Query(users.schema.Query, graphene.ObjectType):
    pass

class Mutation(users.schema.Mutation, graphene.ObjectType):
    # The three lines below are added for graphql_jwt.
    # Notes on exactly how to configure this can be found at: https://github.com/flavors/django-graphql-jwt
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)



# ! Below is for the app folder schema file. Use for imports and structure.

# import graphene
# from graphene_django import DjangoObjectType
# from graphql import GraphQLError
# from django.db.models import Q

# # from .models import Track, Like
# # from users.schema import UserType

# class TrackType(DjangoObjectType):
#   class Meta:
#     model = Track

# class LikeType(DjangoObjectType):
#   class Meta:
#     model = Like

# # Queries

# class Query(graphene.ObjectType):
#   tracks = graphene.List(TrackType, search=graphene.String())
#   likes = graphene.List(LikeType)

#   def resolve_tracks(self, info, search=None):
#     if search:
#       filter = (
#         Q(title__icontains=search) |
#         Q(description__icontains=search) |
#         Q(url__icontains=search) |
#         Q(posted_by__username__icontains=search)
#       )
#       return Track.objects.filter(filter)
    
#     return Track.objects.all()

#   def resolve_likes(self, info):
#     return Like.objects.all()

# # Mutations

# class CreateTrack(graphene.Mutation):
#   track = graphene.Field(TrackType)

#   class Arguments:
#     title = graphene.String()
#     description = graphene.String()
#     url = graphene.String()

#   # def mutate(self, info, **kwargs):
#   #   kwargs.get('title')
#   #   kwargs.get('description')
#   #   kwargs.get('url')

#   def mutate(self, info, title, description, url):
#     user = info.context.user
#     if user.is_anonymous:
#       raise GraphQLError('Login to add a track')
#     track = Track(title=title, description=description, url=url, posted_by=user)
#     track.save()
#     return CreateTrack(track=track)

# class UpdateTrack(graphene.Mutation):
#   track = graphene.Field(TrackType)

#   class Arguments:
#     track_id = graphene.Int(required=True)
#     title = graphene.String()
#     description = graphene.String()
#     url = graphene.String()

#   def mutate(self, info, track_id, title, description, url):
#     user = info.context.user
#     track = Track.objects.get(id=track_id)
#     if track.posted_by != user:
#       raise GraphQLError('You do not own this track')
    
#     track.title = title
#     track.description = description
#     track.url = url
#     track.save()

#     return UpdateTrack(track=track)
      

# class DeleteTrack(graphene.Mutation):
#   track_id = graphene.Int()

#   class Arguments:
#     track_id = graphene.Int(required=True)

#   def mutate(self, info, track_id):
#     user = info.context.user
#     track = Track.objects.get(id=track_id)

#     if track.posted_by != user:
#       raise GraphQLError("Not permitted to delete this track")
    
#     track.delete()
#     return DeleteTrack(track_id=track_id)

# class CreateLike(graphene.Mutation):
#   user = graphene.Field(UserType)
#   track = graphene.Field(TrackType)

#   class Arguments:
#     track_id = graphene.Int(required=True)

#   def mutate(self, info, track_id):
#     user = info.context.user
#     if user.is_anonymous:
#       raise GraphQLError('Login to like tracks.')
    
#     track = Track.objects.get(id=track_id)
#     if not track:
#       raise GraphQLError("Cannot find track with given track ID.")
    
#     Like.objects.create(
#       user=user,
#       track=track
#     )

#     return CreateLike(user=user, track=track)


# class Mutation(graphene.ObjectType):
#   create_track = CreateTrack.Field()
#   update_track = UpdateTrack.Field()
#   delete_track = DeleteTrack.Field()
#   create_like = CreateLike.Field()