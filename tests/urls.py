from django.urls import path, include

urlpatterns = [
    path('graphql/', include('tenc_graphene.urls')),
]
