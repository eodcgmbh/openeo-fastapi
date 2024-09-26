# Table of Contents

* [openeo\_fastapi.client.settings](#openeo_fastapi.client.settings)
  * [AppSettings](#openeo_fastapi.client.settings.AppSettings)
    * [API\_DNS](#openeo_fastapi.client.settings.AppSettings.API_DNS)
    * [API\_TLS](#openeo_fastapi.client.settings.AppSettings.API_TLS)
    * [API\_TITLE](#openeo_fastapi.client.settings.AppSettings.API_TITLE)
    * [API\_DESCRIPTION](#openeo_fastapi.client.settings.AppSettings.API_DESCRIPTION)
    * [OPENEO\_VERSION](#openeo_fastapi.client.settings.AppSettings.OPENEO_VERSION)
    * [OPENEO\_PREFIX](#openeo_fastapi.client.settings.AppSettings.OPENEO_PREFIX)
    * [OIDC\_URL](#openeo_fastapi.client.settings.AppSettings.OIDC_URL)
    * [OIDC\_ORGANISATION](#openeo_fastapi.client.settings.AppSettings.OIDC_ORGANISATION)
    * [OIDC\_POLICIES](#openeo_fastapi.client.settings.AppSettings.OIDC_POLICIES)
    * [STAC\_VERSION](#openeo_fastapi.client.settings.AppSettings.STAC_VERSION)
    * [STAC\_API\_URL](#openeo_fastapi.client.settings.AppSettings.STAC_API_URL)
    * [STAC\_COLLECTIONS\_WHITELIST](#openeo_fastapi.client.settings.AppSettings.STAC_COLLECTIONS_WHITELIST)
    * [ensure\_endswith\_slash](#openeo_fastapi.client.settings.AppSettings.ensure_endswith_slash)
    * [split\_oidc\_policies\_str\_to\_list](#openeo_fastapi.client.settings.AppSettings.split_oidc_policies_str_to_list)
    * [Config](#openeo_fastapi.client.settings.AppSettings.Config)

<a id="openeo_fastapi.client.settings"></a>

# openeo\_fastapi.client.settings

Defining the settings to be used at the application layer of the API.

<a id="openeo_fastapi.client.settings.AppSettings"></a>

## AppSettings Objects

```python
class AppSettings(BaseSettings)
```

The application settings that need to be defined when the app is initialised.

<a id="openeo_fastapi.client.settings.AppSettings.API_DNS"></a>

#### API\_DNS

The domain name hosting the API.

<a id="openeo_fastapi.client.settings.AppSettings.API_TLS"></a>

#### API\_TLS

Whether the API http scheme should be http or https.

<a id="openeo_fastapi.client.settings.AppSettings.API_TITLE"></a>

#### API\_TITLE

The API title to be provided to FastAPI.

<a id="openeo_fastapi.client.settings.AppSettings.API_DESCRIPTION"></a>

#### API\_DESCRIPTION

The API description to be provided to FastAPI.

<a id="openeo_fastapi.client.settings.AppSettings.OPENEO_VERSION"></a>

#### OPENEO\_VERSION

The OpenEO Api specification version supported in this deployment of the API.

<a id="openeo_fastapi.client.settings.AppSettings.OPENEO_PREFIX"></a>

#### OPENEO\_PREFIX

The OpenEO prefix to be used when creating the endpoint urls.

<a id="openeo_fastapi.client.settings.AppSettings.OIDC_URL"></a>

#### OIDC\_URL

The policies to be used for authenticated users with the backend, if not set, any usser with a valid token from the issuer is accepted.

<a id="openeo_fastapi.client.settings.AppSettings.OIDC_ORGANISATION"></a>

#### OIDC\_ORGANISATION

The abbreviation of the OIDC provider's organisation name, e.g. egi.

<a id="openeo_fastapi.client.settings.AppSettings.OIDC_POLICIES"></a>

#### OIDC\_POLICIES

The OIDC policies to check against when authorizing a user. If not provided, all users with a valid token from the issuer will be admitted.

"&&" Is used to denote the addition of another policy.
Policies in the list should be structures as "key, value".
The key referers to some value that is expected to be found in the OIDC userinfo request.
The value referes to some value that is then checked for presence in the values found at the key location.

**Example**:

```
{
    "email": user@test.org,
    "groups" : [ "/staff" ]
}

A valid policy to allow members from the group staff would be, "groups, /staff". This would be the value provided to OIDC_POLICIES.

If you wanted to include users from another group called "/trial", the updated value to OIDC_POLICIES would be, "groups, /staff && groups, /trial"
```

<a id="openeo_fastapi.client.settings.AppSettings.STAC_VERSION"></a>

#### STAC\_VERSION

The STAC Version that is being supported by this deployments data discovery endpoints.

<a id="openeo_fastapi.client.settings.AppSettings.STAC_API_URL"></a>

#### STAC\_API\_URL

The STAC URL of the catalogue that the application deployment will proxy to.

<a id="openeo_fastapi.client.settings.AppSettings.STAC_COLLECTIONS_WHITELIST"></a>

#### STAC\_COLLECTIONS\_WHITELIST

The collection ids to filter by when proxying to the Stac catalogue.

<a id="openeo_fastapi.client.settings.AppSettings.ensure_endswith_slash"></a>

#### ensure\_endswith\_slash

```python
@validator("STAC_API_URL")
def ensure_endswith_slash(cls, v: str) -> str
```

Ensure the STAC_API_URL ends with a trailing slash.

<a id="openeo_fastapi.client.settings.AppSettings.split_oidc_policies_str_to_list"></a>

#### split\_oidc\_policies\_str\_to\_list

```python
@validator("OIDC_POLICIES", pre=True)
def split_oidc_policies_str_to_list(cls, v: str) -> str
```

Ensure the OIDC_POLICIES are split and formatted correctly.

<a id="openeo_fastapi.client.settings.AppSettings.Config"></a>

## Config Objects

```python
class Config()
```

Pydantic model class config.

<a id="openeo_fastapi.client.settings.AppSettings.Config.parse_env_var"></a>

#### parse\_env\_var

```python
@classmethod
def parse_env_var(cls, field_name: str, raw_val: str) -> Any
```

Parse any variables and handle and csv lists into python list type.
