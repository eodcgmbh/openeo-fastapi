# Table of Contents

* [openeo\_fastapi.client.auth](#openeo_fastapi.client.auth)
  * [User](#openeo_fastapi.client.auth.User)
    * [Config](#openeo_fastapi.client.auth.User.Config)
    * [get\_orm](#openeo_fastapi.client.auth.User.get_orm)
  * [Authenticator](#openeo_fastapi.client.auth.Authenticator)
    * [validate](#openeo_fastapi.client.auth.Authenticator.validate)
  * [AuthMethod](#openeo_fastapi.client.auth.AuthMethod)
  * [AuthToken](#openeo_fastapi.client.auth.AuthToken)
    * [from\_token](#openeo_fastapi.client.auth.AuthToken.from_token)
  * [IssuerHandler](#openeo_fastapi.client.auth.IssuerHandler)
    * [validate\_token](#openeo_fastapi.client.auth.IssuerHandler.validate_token)

<a id="openeo_fastapi.client.auth"></a>

# openeo\_fastapi.client.auth

Class and model to define the framework and partial application logic for interacting with Jobs.

Classes:
    - User: Framework for defining and extending the logic for working with BatchJobs.
    - Authenticator: Class holding the abstract validation method used for authentication for API endpoints.
    - AuthMethod: Enum defining the available auth methods.
    - AuthToken: Pydantic model for breaking and validating an OpenEO Token into it's consituent parts.
    - IssuerHandler: Class for handling the AuthToken and validating against the revelant token Issuer and AuthMethod.

<a id="openeo_fastapi.client.auth.User"></a>

## User Objects

```python
class User(BaseModel)
```

Pydantic model manipulating users.

<a id="openeo_fastapi.client.auth.User.Config"></a>

## Config Objects

```python
class Config()
```

Pydantic model class config.

<a id="openeo_fastapi.client.auth.User.get_orm"></a>

#### get\_orm

```python
@classmethod
def get_orm(cls)
```

Get the ORM model for this pydantic model.

<a id="openeo_fastapi.client.auth.Authenticator"></a>

## Authenticator Objects

```python
class Authenticator(ABC)
```

Basic class to hold the validation call to be used by the api endpoints requiring authentication.

<a id="openeo_fastapi.client.auth.Authenticator.validate"></a>

#### validate

```python
@abstractmethod
def validate(authorization: str = Header())
```

Validate the authorisation header and create a new user. This method can be overwritten as needed.

**Arguments**:

- `authorization` _str_ - The authorisation header content from the request headers.
  

**Returns**:

- `User` - The authenticated user.

<a id="openeo_fastapi.client.auth.AuthMethod"></a>

## AuthMethod Objects

```python
class AuthMethod(Enum)
```

Enum defining known auth methods.

<a id="openeo_fastapi.client.auth.AuthToken"></a>

## AuthToken Objects

```python
class AuthToken(BaseModel)
```

The AuthToken breaks down the OpenEO token into its consituent parts to be used for validation.

<a id="openeo_fastapi.client.auth.AuthToken.from_token"></a>

#### from\_token

```python
@classmethod
def from_token(cls, token: str)
```

Takes the openeo format token, splits it into the component parts, and returns an Auth token.

<a id="openeo_fastapi.client.auth.IssuerHandler"></a>

## IssuerHandler Objects

```python
class IssuerHandler(BaseModel)
```

General token handler for querying provided tokens against issuers.

<a id="openeo_fastapi.client.auth.IssuerHandler.validate_token"></a>

#### validate\_token

```python
def validate_token(token: str)
```

Try to validate the token against the give OIDC provider.

**Arguments**:

- `token` _str_ - The OpenEO token to be parsed and validated against the oidc provider.
  

**Raises**:

- `HTTPException` - Raises an exception with relevant status code and descriptive message of failure.
  

**Returns**:

  The JSON as dictionary from _validate_oidc_token.

