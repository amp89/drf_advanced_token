# drf_advanced_token

Installation:
`pip install --upgrade django-drf-advanced-token`


More advanced features for the built in Django Rest Framework token authentication system.

Adds:
- request.user set based on token
- Login route makes a new token for users that have not logged in yet
- Routes to check the token validity, and change the token
- Logout route to invalidtate the token on the backend (logs the user out everywhere they are logged in)

To use this, you must be using token auth and (at least) these in your protected views:
- `authentication_classes = [authentication.TokenAuthentication]`
- `permission_classes = (permissions.IsAuthenticated,)`


(they can be imported with `from rest_framework import authentication, permissions`)

Current only tested with:
- `Django==2.2.7`
- `djangorestframework==3.10.3`


What does this do?

1. Adds middleware to set request.user based on the rest_framework.authtoken app
2. Has `/login/` route `POST`: Accepts `{"username":<username here>, "password":<password here>}`, returns `{"token":<token>}`
3. Has `/token/` route `GET` returns `200` if token is valid, `401` if not valid. `PUT` deletes the old token, and returns a new token `{"token":<token>}`
4. Has `/logut/` route to delete token on backend
5. Set bearer prefix in `settings.BEARER_PREFIX` (defaults to "Token")
6. Once it is set up, just use it like normal `rest_framework.authtoken` auth!

Quick start
-----------

1. Install `django` and `djangorestframework`, make sure rest_framework and rest_framework.auth_token are in your INSTALLED_APPS

2. Add `"drf_advanced_token"` to your `INSTALLED_APPS` setting like this:
```python
 INSTALLED_APPS = [
   ...
   'rest_framework',
   'rest_framework.authtoken',   
   'drf_advanced_token',
 ]
```

3. Add `'drf_advanced_token.middleware.auth.ProcessToken'` to your `MIDDLEWARE`
```python
MIDDLEWARE = [
    ...    
    'drf_advanced_token.middleware.auth.ProcessToken',    
]
```

4. Include the drf_advanced_token URLconf in your project urls.py like this::
```python
urlpatterns = [
    ...
    path('auth/', include('drf_advanced_token.urls')), 
]
```


5. Run `python manage.py migrate` to migrate the rest_framework tables.

6. Start the development server and create a user

7. POST to `http://localhost:8000/auth/login/` with JSON paramters `{"username":<your username here>, "password":<your password here>}`, and headers `{"Content-Type":"application/json", "Accept":"application/json"}`.  The response should be a `200` with `{"token":<your token here>}`, just like the normal DRF token auth.

8. Verify your token with a `GET` to `http://localhost:8000/auth/token/` with headers `{"Content-Type":"application/json", "Accept":"application/json", "Authorization": "Token <your token from the login response here>"}`.  The response will be a blank `200` if it is successful, and a `401` if unsuccessful.

9. To change your token, `PUT` to `http://localhost:8000/auth/token/` with headers `{"Content-Type":"application/json", "Accept":"application/json", "Authorization": "Token <your token from the login response here>"}`,  The response should be a `200` with `{"token":<your token here>}`, just like the normal DRF token auth.  The old token will no longer work.

10. To logout (delete the token on the backend), `GET` to `http://localhost:8000/auth/logout/` with headers `{"Content-Type":"application/json", "Accept":"application/json", "Authorization": "Token <your token from the login response here>"}`,   The response will be a blank `200` if it is successful, and a `401` if unsuccessful.  No token will work until the next login.

11.  This will now work for all views with the correct drf authentication and permission classes.  If you did not change the token prefex, just include `{"Authorization": "Token <your token>"}` with your requests, just as you would with the regualr rest_framework.authtoken authentication system.

Example View:

```
class SomeView(APIView):
    authentication_classes = [authentication.TokenAuthentication]    
    permission_classes = (permissions.IsAuthenticated,)    
    def get(self, request, *args, **kwargs): 
        ...
```


12.  To clear all tokens (logout all users): `python manage.py  revoke_all_tokens --force`
