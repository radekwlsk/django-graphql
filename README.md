# 10C Graphene

Django app for 10c-django-template adding Django-Graphene with some initial work and easy configuration

## Quick start

1. Add `graphene_django` and `tenc_graphene` to your INSTALLED_APPS setting like this:
```python
    INSTALLED_APPS = [
        ...
        'graphene_django',
        'tenc_graphene',
    ]
```
2. Include the `tenc_graphene` URLconf in your project `urls.py` like this:
```python
    path('graphql/', include('tenc_graphene.urls')),
```
3. Create `schema.py` file in your project root directory like this:
```python
import graphene
from tenc_graphql.schema import TencGrapheneQuery


class Query(
    TencGrapheneQuery,
    graphene.ObjectType,
):
    # This class will inherit from multiple Queries as we begin to add more apps to our project.
    # (you need to define the Query class in schema.py in the users app first)
    pass


schema = graphene.Schema(query=Query)

```
4. Set `GRAPHENE` config in settings providing schema path like this:
```python
GRAPHENE = {
    'SCHEMA': '<your_app>.schema.schema'
}
```
5. Start the development server and visit `http://127.0.0.1:8000/graphql/`
   to access GraphQL UI (if enabled in settings).
 
 
## Customizing behaviour using settings

You can customize `tenc_graphene` behavior through settings variables in `settings.py` like this:

```python
TENC_GRAPHENE = {
    'PROTECTED_URL': False,
    'URL_PATH': '',
    'URL_NAME': 'graphql',
    'DEFAULT_USER_TYPE': True,
    'DEFAULT_USER_EXCLUDE': [],
}
``` 

Which are the default settings.

- `PROTECTED_URL` - boolean, adds `LoginRequiredMixin` functionality to `GraphQLView` if set to `True`, requiring 
authentication before access to `graphql/`
- `URL_PATH` - path where GraphQL API should be available, remember it is relative to whatever you set in `urls.py`,
- `URL_NAME` - name for the GraphQL API endpoint, `graphql` by default,
- `DEFAULT_USER_TYPE` - boolean, adds `tenc_garphql.schema.UserQuery` with `user` and `allUsers` fields in root Query 
to access user model returned by `django.contrib.auth.get_user_model()` using `graphene_django.DjangoObjectType` for 
auto fields discovery, if set to `False` you need to define some fields on `Query` in `schema.py` or extend it with 
`Query` of an app.
- `DEFAULT_USER_EXCLUDE` - list or tuple of fields from user model to exclude from API, they will not be accessible and 
will raise an error in GraphQL query (similar to `exclude` in DRF's `Serializer`); `password` is always included for 
security reasons, even if not explicitly provided in the setting.
