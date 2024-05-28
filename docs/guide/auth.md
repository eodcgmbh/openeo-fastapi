## Overwriting the authentication.

The authentication function for this repo has been set using the predefined validator function in the Authenticator class. The following example will demonstrate how to provide your own auth function for a given endpoint.

## How to overwrite the auth.

You can either inherit the authenticator class and overwrite the validate function, or provide an entirely new function. In either case, it's worth noting that the return value for any provided authentication function currently needs to be of type User. If you want to additionally change the return type you may have to overwrite the endpoint entirely.

        client = OpenEOCore(
            ...
        )

        api = OpenEOApi(client=client, app=FastAPI())

        def cool_new_auth():
            return User(user_id=specific_uuid, oidc_sub="the-only-user")

        core_api.override_authentication(cool_new_auth)

Now any endpoints that originally used the Authenticator.validate function, will now use cool_new_auth instead.
