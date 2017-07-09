from firebase import firebase


class Database:
    @staticmethod
    def start():
        db = firebase.FirebaseApplication('https://dialgarithm.firebaseio.com/', authentication=None)
        result = db.get('/', None)
        print(result)
        # {'error': 'Permission denied.'}

        authentication = firebase.Authentication('THIS_IS_MY_SECRET', 'ozgurvt@gmail.com', extra={'id': 123})
        firebase.authentication = authentication
        print(authentication.extra)
        # {'admin': False, 'debug': False, 'email': 'ozgurvt@gmail.com', 'id': 123, 'provider': 'password'}

        user = authentication.get_user()
        print(user.firebase_auth_token)
        # "eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9.eyJhZG1pbiI6IGZhbHNlLCAiZGVidWciOiBmYWxzZSwgIml
        # hdCI6IDEzNjE5NTAxNzQsICJkIjogeyJkZWJ1ZyI6IGZhbHNlLCAiYWRtaW4iOiBmYWxzZSwgInByb3ZpZGVyIjog
        # InBhc3N3b3JkIiwgImlkIjogNSwgImVtYWlsIjogIm96Z3VydnRAZ21haWwuY29tIn0sICJ2IjogMH0.lq4IRVfvE
        # GQklslOlS4uIBLSSJj88YNrloWXvisRgfQ"

        result = firebase.get('/users', None, {'print': 'pretty'})
        print(result)
        # {'1': 'John Doe', '2': 'Jane Doe'}

Database.start()