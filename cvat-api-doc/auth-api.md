<div class="col-12 col-md-9 col-xl-8 ps-md-5" role="main">

1.  [Home](https://docs.cvat.ai/docs/)
2.  [Developers](https://docs.cvat.ai/docs/api_sdk/)
3.  [SDK](https://docs.cvat.ai/docs/api_sdk/sdk/)
4.  [API Reference](https://docs.cvat.ai/docs/api_sdk/sdk/reference/)
5.  [APIs](https://docs.cvat.ai/docs/api_sdk/sdk/reference/apis/)
6.  AuthApi

<div class="td-content">

# AuthApi class reference

<div class="article-meta">

</div>

All URIs are relative to *http://localhost*

| Method | HTTP request | Description |
|----|----|----|
| [**create_access_tokens**](../auth-api#create_access_tokens) | **POST** /api/auth/access_tokens | Create a token |
| [**create_login**](../auth-api#create_login) | **POST** /api/auth/login |  |
| [**create_logout**](../auth-api#create_logout) | **POST** /api/auth/logout |  |
| [**create_password_change**](../auth-api#create_password_change) | **POST** /api/auth/password/change |  |
| [**create_password_reset**](../auth-api#create_password_reset) | **POST** /api/auth/password/reset |  |
| [**create_password_reset_confirm**](../auth-api#create_password_reset_confirm) | **POST** /api/auth/password/reset/confirm |  |
| [**create_register**](../auth-api#create_register) | **POST** /api/auth/register |  |
| [**destroy_access_tokens**](../auth-api#destroy_access_tokens) | **DELETE** /api/auth/access_tokens/{id} | Revoke token |
| [**list_access_tokens**](../auth-api#list_access_tokens) | **GET** /api/auth/access_tokens | List tokens |
| [**partial_update_access_tokens**](../auth-api#partial_update_access_tokens) | **PATCH** /api/auth/access_tokens/{id} | Update a token |
| [**retrieve_access_tokens**](../auth-api#retrieve_access_tokens) | **GET** /api/auth/access_tokens/{id} | Get token details |
| [**retrieve_access_tokens_self**](../auth-api#retrieve_access_tokens_self) | **GET** /api/auth/access_tokens/self | Get current token details |
| [**retrieve_rules**](../auth-api#retrieve_rules) | **GET** /api/auth/rules |  |

## **create_access_tokens**

> create_access_tokens( access_token_write_request, \*\*kwargs )

Create a token

### Example

<div class="highlight">

```
from pprint import pprint

from cvat_sdk.api_client import Configuration, ApiClient, exceptions
from cvat_sdk.api_client.models import *

# Set up an API client
# Read Configuration class docs for more info about parameters and authentication methods
configuration = Configuration(
    host = "http://localhost",
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD',
)

with ApiClient(configuration) as api_client:
    access_token_write_request = AccessTokenWriteRequest(
        name="name_example",
        expiry_date=dateutil_parser('1970-01-01T00:00:00.00Z'),
        read_only=True,
    ) # AccessTokenWriteRequest | 

    try:
        (data, response) = api_client.auth_api.create_access_tokens(
            access_token_write_request,)
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling AuthApi.create_access_tokens(): %s\n" % e)
```

</div>

### Parameters

| Name | Type | Description | Notes |
|----|----|----|----|
| **access_token_write_request** | [**AccessTokenWriteRequest**](../../models/access-token-write-request) |  |  |

There are also optional kwargs that control the function invocation
behavior. [Read more
here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type: `Tuple[AccessTokenRead, urllib3.HTTPResponse]`.

Returns a tuple with 2 values: `(parsed_response, raw_response)`.

The first value is a model parsed from the response data. The second
value is the raw response, which can be useful to get response
parameters, such as status code, headers, or raw response data. Read
more about invocation parameters and returned values
[here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Authentication

accessTokenAuth, basicAuth, csrfAuth, csrfHeaderAuth, sessionAuth,
tokenAuth

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/vnd.cvat+json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **201**     |             | \-               |

## **create_login**

> create_login( login_serializer_ex_request, \*\*kwargs )

Check the credentials and return the REST Token if the credentials are
valid and authenticated. If email verification is enabled and the user
has the unverified email, an email with a confirmation link will be
sent. Calls Django Auth login method to register User ID in Django
session framework. Accept the following POST parameters: username,
email, password Return the REST Framework Token Object’s key.

### Example

<div class="highlight">

```
from pprint import pprint

from cvat_sdk.api_client import Configuration, ApiClient, exceptions
from cvat_sdk.api_client.models import *

# Set up an API client
# Read Configuration class docs for more info about parameters and authentication methods
configuration = Configuration(
    host = "http://localhost",
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD',
)

with ApiClient(configuration) as api_client:
    login_serializer_ex_request = LoginSerializerExRequest(
        username="username_example",
        email="email_example",
        password="password_example",
    ) # LoginSerializerExRequest | 

    try:
        (data, response) = api_client.auth_api.create_login(
            login_serializer_ex_request,)
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling AuthApi.create_login(): %s\n" % e)
```

</div>

### Parameters

| Name | Type | Description | Notes |
|----|----|----|----|
| **login_serializer_ex_request** | [**LoginSerializerExRequest**](../../models/login-serializer-ex-request) |  |  |

There are also optional kwargs that control the function invocation
behavior. [Read more
here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type: `Tuple[Token, urllib3.HTTPResponse]`.

Returns a tuple with 2 values: `(parsed_response, raw_response)`.

The first value is a model parsed from the response data. The second
value is the raw response, which can be useful to get response
parameters, such as status code, headers, or raw response data. Read
more about invocation parameters and returned values
[here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Authentication

accessTokenAuth, basicAuth, csrfAuth, csrfHeaderAuth, sessionAuth,
tokenAuth

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/vnd.cvat+json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200**     |             | \-               |

## **create_logout**

> create_logout( \*\*kwargs )

Calls Django logout method and delete the Token object assigned to the
current User object. Accepts/Returns nothing.

### Example

<div class="highlight">

```
from pprint import pprint

from cvat_sdk.api_client import Configuration, ApiClient, exceptions
from cvat_sdk.api_client.models import *

# Set up an API client
# Read Configuration class docs for more info about parameters and authentication methods
configuration = Configuration(
    host = "http://localhost",
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD',
)

with ApiClient(configuration) as api_client:

    try:
        (data, response) = api_client.auth_api.create_logout()
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling AuthApi.create_logout(): %s\n" % e)
```

</div>

### Parameters

This endpoint does not need any parameter.

There are also optional kwargs that control the function invocation
behavior. [Read more
here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type: `Tuple[RestAuthDetail, urllib3.HTTPResponse]`.

Returns a tuple with 2 values: `(parsed_response, raw_response)`.

The first value is a model parsed from the response data. The second
value is the raw response, which can be useful to get response
parameters, such as status code, headers, or raw response data. Read
more about invocation parameters and returned values
[here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Authentication

accessTokenAuth, basicAuth, csrfAuth, csrfHeaderAuth, sessionAuth,
tokenAuth

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/vnd.cvat+json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200**     |             | \-               |

## **create_password_change**

> create_password_change( password_change_request, \*\*kwargs )

Calls Django Auth SetPasswordForm save method. Accepts the following
POST parameters: new_password1, new_password2 Returns the success/fail
message.

### Example

<div class="highlight">

```
from pprint import pprint

from cvat_sdk.api_client import Configuration, ApiClient, exceptions
from cvat_sdk.api_client.models import *

# Set up an API client
# Read Configuration class docs for more info about parameters and authentication methods
configuration = Configuration(
    host = "http://localhost",
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD',
)

with ApiClient(configuration) as api_client:
    password_change_request = PasswordChangeRequest(
        old_password="old_password_example",
        new_password1="new_password1_example",
        new_password2="new_password2_example",
    ) # PasswordChangeRequest | 

    try:
        (data, response) = api_client.auth_api.create_password_change(
            password_change_request,)
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling AuthApi.create_password_change(): %s\n" % e)
```

</div>

### Parameters

| Name | Type | Description | Notes |
|----|----|----|----|
| **password_change_request** | [**PasswordChangeRequest**](../../models/password-change-request) |  |  |

There are also optional kwargs that control the function invocation
behavior. [Read more
here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type: `Tuple[RestAuthDetail, urllib3.HTTPResponse]`.

Returns a tuple with 2 values: `(parsed_response, raw_response)`.

The first value is a model parsed from the response data. The second
value is the raw response, which can be useful to get response
parameters, such as status code, headers, or raw response data. Read
more about invocation parameters and returned values
[here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Authentication

basicAuth, csrfAuth, csrfHeaderAuth, sessionAuth, tokenAuth

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/vnd.cvat+json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200**     |             | \-               |

## **create_password_reset**

> create_password_reset( password_reset_serializer_ex_request,
> \*\*kwargs )

Calls Django Auth PasswordResetForm save method. Accepts the following
POST parameters: email Returns the success/fail message.

### Example

<div class="highlight">

```
from pprint import pprint

from cvat_sdk.api_client import Configuration, ApiClient, exceptions
from cvat_sdk.api_client.models import *

# Set up an API client
# Read Configuration class docs for more info about parameters and authentication methods
configuration = Configuration(
    host = "http://localhost",
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD',
)

with ApiClient(configuration) as api_client:
    password_reset_serializer_ex_request = PasswordResetSerializerExRequest(
        email="email_example",
    ) # PasswordResetSerializerExRequest | 

    try:
        (data, response) = api_client.auth_api.create_password_reset(
            password_reset_serializer_ex_request,)
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling AuthApi.create_password_reset(): %s\n" % e)
```

</div>

### Parameters

| Name | Type | Description | Notes |
|----|----|----|----|
| **password_reset_serializer_ex_request** | [**PasswordResetSerializerExRequest**](../../models/password-reset-serializer-ex-request) |  |  |

There are also optional kwargs that control the function invocation
behavior. [Read more
here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type: `Tuple[RestAuthDetail, urllib3.HTTPResponse]`.

Returns a tuple with 2 values: `(parsed_response, raw_response)`.

The first value is a model parsed from the response data. The second
value is the raw response, which can be useful to get response
parameters, such as status code, headers, or raw response data. Read
more about invocation parameters and returned values
[here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Authentication

accessTokenAuth, basicAuth, csrfAuth, csrfHeaderAuth, sessionAuth,
tokenAuth

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/vnd.cvat+json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200**     |             | \-               |

## **create_password_reset_confirm**

> create_password_reset_confirm( password_reset_confirm_request,
> \*\*kwargs )

Password reset e-mail link is confirmed, therefore this resets the
user’s password. Accepts the following POST parameters: token, uid,
new_password1, new_password2 Returns the success/fail message.

### Example

<div class="highlight">

```
from pprint import pprint

from cvat_sdk.api_client import Configuration, ApiClient, exceptions
from cvat_sdk.api_client.models import *

# Set up an API client
# Read Configuration class docs for more info about parameters and authentication methods
configuration = Configuration(
    host = "http://localhost",
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD',
)

with ApiClient(configuration) as api_client:
    password_reset_confirm_request = PasswordResetConfirmRequest(
        new_password1="new_password1_example",
        new_password2="new_password2_example",
        uid="uid_example",
        token="token_example",
    ) # PasswordResetConfirmRequest | 

    try:
        (data, response) = api_client.auth_api.create_password_reset_confirm(
            password_reset_confirm_request,)
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling AuthApi.create_password_reset_confirm(): %s\n" % e)
```

</div>

### Parameters

| Name | Type | Description | Notes |
|----|----|----|----|
| **password_reset_confirm_request** | [**PasswordResetConfirmRequest**](../../models/password-reset-confirm-request) |  |  |

There are also optional kwargs that control the function invocation
behavior. [Read more
here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type: `Tuple[RestAuthDetail, urllib3.HTTPResponse]`.

Returns a tuple with 2 values: `(parsed_response, raw_response)`.

The first value is a model parsed from the response data. The second
value is the raw response, which can be useful to get response
parameters, such as status code, headers, or raw response data. Read
more about invocation parameters and returned values
[here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Authentication

accessTokenAuth, basicAuth, csrfAuth, csrfHeaderAuth, sessionAuth,
tokenAuth

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/vnd.cvat+json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200**     |             | \-               |

## **create_register**

> create_register( register_serializer_ex_request, \*\*kwargs )

### Example

<div class="highlight">

```
from pprint import pprint

from cvat_sdk.api_client import Configuration, ApiClient, exceptions
from cvat_sdk.api_client.models import *

# Set up an API client
# Read Configuration class docs for more info about parameters and authentication methods
configuration = Configuration(
    host = "http://localhost",
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD',
)

with ApiClient(configuration) as api_client:
    register_serializer_ex_request = RegisterSerializerExRequest(
        username="username_example",
        email="email_example",
        password1="password1_example",
        password2="password2_example",
        first_name="first_name_example",
        last_name="last_name_example",
    ) # RegisterSerializerExRequest | 

    try:
        (data, response) = api_client.auth_api.create_register(
            register_serializer_ex_request,)
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling AuthApi.create_register(): %s\n" % e)
```

</div>

### Parameters

| Name | Type | Description | Notes |
|----|----|----|----|
| **register_serializer_ex_request** | [**RegisterSerializerExRequest**](../../models/register-serializer-ex-request) |  |  |

There are also optional kwargs that control the function invocation
behavior. [Read more
here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type: `Tuple[RegisterSerializerEx, urllib3.HTTPResponse]`.

Returns a tuple with 2 values: `(parsed_response, raw_response)`.

The first value is a model parsed from the response data. The second
value is the raw response, which can be useful to get response
parameters, such as status code, headers, or raw response data. Read
more about invocation parameters and returned values
[here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Authentication

accessTokenAuth, basicAuth, csrfAuth, csrfHeaderAuth, sessionAuth,
tokenAuth

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/vnd.cvat+json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **201**     |             | \-               |

## **destroy_access_tokens**

> destroy_access_tokens( id, \*\*kwargs )

Revoke token

### Example

<div class="highlight">

```
from pprint import pprint

from cvat_sdk.api_client import Configuration, ApiClient, exceptions
from cvat_sdk.api_client.models import *

# Set up an API client
# Read Configuration class docs for more info about parameters and authentication methods
configuration = Configuration(
    host = "http://localhost",
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD',
)

with ApiClient(configuration) as api_client:
    id = 1 # int | A unique integer value identifying this API Access Token.

    try:
        api_client.auth_api.destroy_access_tokens(
            id,)
    except exceptions.ApiException as e:
        print("Exception when calling AuthApi.destroy_access_tokens(): %s\n" % e)
```

</div>

### Parameters

| Name | Type | Description | Notes |
|----|----|----|----|
| **id** | **int** | A unique integer value identifying this API Access Token. |  |

There are also optional kwargs that control the function invocation
behavior. [Read more
here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type: `Tuple[None, urllib3.HTTPResponse]`.

Returns a tuple with 2 values: `(None, raw_response)`.

This endpoint does not have any return value, so `None` is always
returned as the first value. The second value is the raw response, which
can be useful to get response parameters, such as status code, headers,
or raw response data. Read more about invocation parameters and returned
values
[here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Authentication

accessTokenAuth, basicAuth, csrfAuth, csrfHeaderAuth, sessionAuth,
tokenAuth

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: Not defined

### HTTP response details

| Status code | Description                        | Response headers |
|-------------|------------------------------------|------------------|
| **204**     | The token was successfully revoked | \-               |

## **list_access_tokens**

> list_access_tokens( filter=None, name=None, page=None, page_size=None,
> search=None, sort=None, \*\*kwargs )

List tokens

### Example

<div class="highlight">

```
from pprint import pprint

from cvat_sdk.api_client import Configuration, ApiClient, exceptions
from cvat_sdk.api_client.models import *

# Set up an API client
# Read Configuration class docs for more info about parameters and authentication methods
configuration = Configuration(
    host = "http://localhost",
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD',
)

with ApiClient(configuration) as api_client:
    filter = "filter_example" # str |  JSON Logic filter. This filter can be used to perform complex filtering by grouping rules.  For example, using such a filter you can get all resources created by you:      - {\"and\":[{\"==\":[{\"var\":\"owner\"},\"<user>\"]}]}  Details about the syntax used can be found at the link: https://jsonlogic.com/   Available filter_fields: ['name', 'id', 'created_date', 'updated_date', 'expiry_date', 'last_used_date', 'read_only']. (optional)
    name = "name_example" # str | A simple equality filter for the name field (optional)
    page = 1 # int | A page number within the paginated result set. (optional)
    page_size = 1 # int | Number of results to return per page. (optional)
    search = "search_example" # str | A search term. Available search_fields: ('name',) (optional)
    sort = "sort_example" # str | Which field to use when ordering the results. Available ordering_fields: ['name', 'id', 'created_date', 'updated_date', 'expiry_date', 'last_used_date', 'read_only'] (optional)

    try:
        (data, response) = api_client.auth_api.list_access_tokens(
            filter=filter,
            name=name,
            page=page,
            page_size=page_size,
            search=search,
            sort=sort,
        )
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling AuthApi.list_access_tokens(): %s\n" % e)
```

</div>

### Parameters

| Name | Type | Description | Notes |
|----|----|----|----|
| **filter** | **str** | JSON Logic filter. This filter can be used to perform complex filtering by grouping rules. For example, using such a filter you can get all resources created by you: - {"and":\[{"==":\[{"var":"owner"},""\]}\]} Details about the syntax used can be found at the link: <https://jsonlogic.com/> Available filter_fields: \[’name’, ‘id’, ‘created_date’, ‘updated_date’, ’expiry_date’, ’last_used_date’, ‘read_only’\]. | \[optional\] |
| **name** | **str** | A simple equality filter for the name field | \[optional\] |
| **page** | **int** | A page number within the paginated result set. | \[optional\] |
| **page_size** | **int** | Number of results to return per page. | \[optional\] |
| **search** | **str** | A search term. Available search_fields: (’name’,) | \[optional\] |
| **sort** | **str** | Which field to use when ordering the results. Available ordering_fields: \[’name’, ‘id’, ‘created_date’, ‘updated_date’, ’expiry_date’, ’last_used_date’, ‘read_only’\] | \[optional\] |

There are also optional kwargs that control the function invocation
behavior. [Read more
here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type:
`Tuple[PaginatedAccessTokenReadList, urllib3.HTTPResponse]`.

Returns a tuple with 2 values: `(parsed_response, raw_response)`.

The first value is a model parsed from the response data. The second
value is the raw response, which can be useful to get response
parameters, such as status code, headers, or raw response data. Read
more about invocation parameters and returned values
[here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Authentication

accessTokenAuth, basicAuth, csrfAuth, csrfHeaderAuth, sessionAuth,
tokenAuth

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/vnd.cvat+json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200**     |             | \-               |

## **partial_update_access_tokens**

> partial_update_access_tokens( id,
> patched_access_token_write_request=None, \*\*kwargs )

Update a token

### Example

<div class="highlight">

```
from pprint import pprint

from cvat_sdk.api_client import Configuration, ApiClient, exceptions
from cvat_sdk.api_client.models import *

# Set up an API client
# Read Configuration class docs for more info about parameters and authentication methods
configuration = Configuration(
    host = "http://localhost",
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD',
)

with ApiClient(configuration) as api_client:
    id = 1 # int | A unique integer value identifying this API Access Token.
    patched_access_token_write_request = PatchedAccessTokenWriteRequest(
        name="name_example",
        expiry_date=dateutil_parser('1970-01-01T00:00:00.00Z'),
        read_only=True,
    ) # PatchedAccessTokenWriteRequest |  (optional)

    try:
        (data, response) = api_client.auth_api.partial_update_access_tokens(
            id,
            patched_access_token_write_request=patched_access_token_write_request,
        )
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling AuthApi.partial_update_access_tokens(): %s\n" % e)
```

</div>

### Parameters

| Name | Type | Description | Notes |
|----|----|----|----|
| **id** | **int** | A unique integer value identifying this API Access Token. |  |
| **patched_access_token_write_request** | [**PatchedAccessTokenWriteRequest**](../../models/patched-access-token-write-request) |  | \[optional\] |

There are also optional kwargs that control the function invocation
behavior. [Read more
here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type: `Tuple[AccessTokenRead, urllib3.HTTPResponse]`.

Returns a tuple with 2 values: `(parsed_response, raw_response)`.

The first value is a model parsed from the response data. The second
value is the raw response, which can be useful to get response
parameters, such as status code, headers, or raw response data. Read
more about invocation parameters and returned values
[here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Authentication

accessTokenAuth, basicAuth, csrfAuth, csrfHeaderAuth, sessionAuth,
tokenAuth

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/vnd.cvat+json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200**     |             | \-               |

## **retrieve_access_tokens**

> retrieve_access_tokens( id, \*\*kwargs )

Get token details

### Example

<div class="highlight">

```
from pprint import pprint

from cvat_sdk.api_client import Configuration, ApiClient, exceptions
from cvat_sdk.api_client.models import *

# Set up an API client
# Read Configuration class docs for more info about parameters and authentication methods
configuration = Configuration(
    host = "http://localhost",
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD',
)

with ApiClient(configuration) as api_client:
    id = 1 # int | A unique integer value identifying this API Access Token.

    try:
        (data, response) = api_client.auth_api.retrieve_access_tokens(
            id,)
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling AuthApi.retrieve_access_tokens(): %s\n" % e)
```

</div>

### Parameters

| Name | Type | Description | Notes |
|----|----|----|----|
| **id** | **int** | A unique integer value identifying this API Access Token. |  |

There are also optional kwargs that control the function invocation
behavior. [Read more
here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type: `Tuple[AccessTokenRead, urllib3.HTTPResponse]`.

Returns a tuple with 2 values: `(parsed_response, raw_response)`.

The first value is a model parsed from the response data. The second
value is the raw response, which can be useful to get response
parameters, such as status code, headers, or raw response data. Read
more about invocation parameters and returned values
[here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Authentication

accessTokenAuth, basicAuth, csrfAuth, csrfHeaderAuth, sessionAuth,
tokenAuth

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/vnd.cvat+json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200**     |             | \-               |

## **retrieve_access_tokens_self**

> retrieve_access_tokens_self( \*\*kwargs )

Get current token details

Get details of the token used for the current request. This endpoint is
only allowed if the request is performed using an access token.

### Example

<div class="highlight">

```
from pprint import pprint

from cvat_sdk.api_client import Configuration, ApiClient, exceptions
from cvat_sdk.api_client.models import *

# Set up an API client
# Read Configuration class docs for more info about parameters and authentication methods
configuration = Configuration(
    host = "http://localhost",
)

with ApiClient(configuration) as api_client:

    try:
        (data, response) = api_client.auth_api.retrieve_access_tokens_self()
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling AuthApi.retrieve_access_tokens_self(): %s\n" % e)
```

</div>

### Parameters

This endpoint does not need any parameter.

There are also optional kwargs that control the function invocation
behavior. [Read more
here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type: `Tuple[AccessTokenRead, urllib3.HTTPResponse]`.

Returns a tuple with 2 values: `(parsed_response, raw_response)`.

The first value is a model parsed from the response data. The second
value is the raw response, which can be useful to get response
parameters, such as status code, headers, or raw response data. Read
more about invocation parameters and returned values
[here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Authentication

accessTokenAuth

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/vnd.cvat+json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200**     |             | \-               |

## **retrieve_rules**

> retrieve_rules( \*\*kwargs )

### Example

<div class="highlight">

```
from pprint import pprint

from cvat_sdk.api_client import Configuration, ApiClient, exceptions
from cvat_sdk.api_client.models import *

# Set up an API client
# Read Configuration class docs for more info about parameters and authentication methods
configuration = Configuration(
    host = "http://localhost",)

with ApiClient(configuration) as api_client:

    try:
        api_client.auth_api.retrieve_rules()
    except exceptions.ApiException as e:
        print("Exception when calling AuthApi.retrieve_rules(): %s\n" % e)
```

</div>

### Parameters

This endpoint does not need any parameter.

There are also optional kwargs that control the function invocation
behavior. [Read more
here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type: `Tuple[None, urllib3.HTTPResponse]`.

Returns a tuple with 2 values: `(None, raw_response)`.

This endpoint does not have any return value, so `None` is always
returned as the first value. The second value is the raw response, which
can be useful to get response parameters, such as status code, headers,
or raw response data. Read more about invocation parameters and returned
values
[here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Authentication

No authentication required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: Not defined

### HTTP response details

| Status code | Description      | Response headers |
|-------------|------------------|------------------|
| **200**     | No response body | \-               |

</div>

</div>
