import graphene
from tenc_graphene.schema import TencGrapheneQuery


class Query(
    TencGrapheneQuery,
    graphene.ObjectType,
):
    # This class will inherit from multiple Queries as we begin to add more apps to our project.
    # (you need to define the Query class in schema.py in the users app first)
    pass


schema = graphene.Schema(query=Query)
