<div class="col-12 col-md-9 col-xl-8 ps-md-5" role="main">

1.  [Home](https://docs.cvat.ai/docs/)
2.  [Developers](https://docs.cvat.ai/docs/api_sdk/)
3.  [SDK](https://docs.cvat.ai/docs/api_sdk/sdk/)
4.  [API Reference](https://docs.cvat.ai/docs/api_sdk/sdk/reference/)
5.  [APIs](https://docs.cvat.ai/docs/api_sdk/sdk/reference/apis/)
6.  UsersApi

<div class="td-content">

# UsersApi class reference

<div class="article-meta">

</div>

All URIs are relative to *http://localhost*

| Method | HTTP request | Description |
|----|----|----|
| [**destroy**](../users-api#destroy) | **DELETE** /api/users/{id} | Delete a user |
| [**list**](../users-api#list) | **GET** /api/users | List users |
| [**partial_update**](../users-api#partial_update) | **PATCH** /api/users/{id} | Update a user |
| [**retrieve**](../users-api#retrieve) | **GET** /api/users/{id} | Get user details |
| [**retrieve_self**](../users-api#retrieve_self) | **GET** /api/users/self | Get details of the current user |

## **destroy**

> destroy( id, \*\*kwargs )

Delete a user

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
    id = 1 # int | A unique integer value identifying this user.

    try:
        api_client.users_api.destroy(
            id,)
    except exceptions.ApiException as e:
        print("Exception when calling UsersApi.destroy(): %s\n" % e)
```

</div>

### Parameters

| Name   | Type    | Description                                   | Notes |
|--------|---------|-----------------------------------------------|-------|
| **id** | **int** | A unique integer value identifying this user. |       |

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

| Status code | Description               | Response headers |
|-------------|---------------------------|------------------|
| **204**     | The user has been deleted | \-               |

## **list**

> list( x_organization=None, filter=None, first_name=None,
> is_active=None, last_name=None, org=None, org_id=None, page=None,
> page_size=None, search=None, sort=None, username=None, \*\*kwargs )

List users

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
    x_organization = "X-Organization_example" # str | Organization unique slug (optional)
    filter = "filter_example" # str |  JSON Logic filter. This filter can be used to perform complex filtering by grouping rules.  For example, using such a filter you can get all resources created by you:      - {\"and\":[{\"==\":[{\"var\":\"owner\"},\"<user>\"]}]}  Details about the syntax used can be found at the link: https://jsonlogic.com/   Available filter_fields: ['username', 'first_name', 'last_name', 'id', 'is_active']. (optional)
    first_name = "first_name_example" # str | A simple equality filter for the first_name field (optional)
    is_active = True # bool | A simple equality filter for the is_active field (optional)
    last_name = "last_name_example" # str | A simple equality filter for the last_name field (optional)
    org = "org_example" # str | Organization unique slug (optional)
    org_id = 1 # int | Organization identifier (optional)
    page = 1 # int | A page number within the paginated result set. (optional)
    page_size = 1 # int | Number of results to return per page. (optional)
    search = "search_example" # str | A search term. Available search_fields: ('username', 'first_name', 'last_name') (optional)
    sort = "sort_example" # str | Which field to use when ordering the results. Available ordering_fields: ['username', 'first_name', 'last_name', 'id', 'is_active'] (optional)
    username = "username_example" # str | A simple equality filter for the username field (optional)

    try:
        (data, response) = api_client.users_api.list(
            x_organization=x_organization,
            filter=filter,
            first_name=first_name,
            is_active=is_active,
            last_name=last_name,
            org=org,
            org_id=org_id,
            page=page,
            page_size=page_size,
            search=search,
            sort=sort,
            username=username,
        )
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling UsersApi.list(): %s\n" % e)
```

</div>

### Parameters

| Name | Type | Description | Notes |
|----|----|----|----|
| **x_organization** | **str** | Organization unique slug | \[optional\] |
| **filter** | **str** | JSON Logic filter. This filter can be used to perform complex filtering by grouping rules. For example, using such a filter you can get all resources created by you: - {"and":\[{"==":\[{"var":"owner"},""\]}\]} Details about the syntax used can be found at the link: <https://jsonlogic.com/> Available filter_fields: \[‘username’, ‘first_name’, ’last_name’, ‘id’, ‘is_active’\]. | \[optional\] |
| **first_name** | **str** | A simple equality filter for the first_name field | \[optional\] |
| **is_active** | **bool** | A simple equality filter for the is_active field | \[optional\] |
| **last_name** | **str** | A simple equality filter for the last_name field | \[optional\] |
| **org** | **str** | Organization unique slug | \[optional\] |
| **org_id** | **int** | Organization identifier | \[optional\] |
| **page** | **int** | A page number within the paginated result set. | \[optional\] |
| **page_size** | **int** | Number of results to return per page. | \[optional\] |
| **search** | **str** | A search term. Available search_fields: (‘username’, ‘first_name’, ’last_name’) | \[optional\] |
| **sort** | **str** | Which field to use when ordering the results. Available ordering_fields: \[‘username’, ‘first_name’, ’last_name’, ‘id’, ‘is_active’\] | \[optional\] |
| **username** | **str** | A simple equality filter for the username field | \[optional\] |

There are also optional kwargs that control the function invocation
behavior. [Read more
here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type: `Tuple[PaginatedMetaUserList, urllib3.HTTPResponse]`.

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

## **partial_update**

> partial_update( id, patched_user_request=None, \*\*kwargs )

Update a user

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
    id = 1 # int | A unique integer value identifying this user.
    patched_user_request = PatchedUserRequest(
        username="A",
        first_name="first_name_example",
        last_name="last_name_example",
        email="email_example",
        groups=[
            "groups_example",
        ],
        is_staff=True,
        is_superuser=True,
        is_active=True,
    ) # PatchedUserRequest |  (optional)

    try:
        (data, response) = api_client.users_api.partial_update(
            id,
            patched_user_request=patched_user_request,
        )
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling UsersApi.partial_update(): %s\n" % e)
```

</div>

### Parameters

| Name | Type | Description | Notes |
|----|----|----|----|
| **id** | **int** | A unique integer value identifying this user. |  |
| **patched_user_request** | [**PatchedUserRequest**](../../models/patched-user-request) |  | \[optional\] |

There are also optional kwargs that control the function invocation
behavior. [Read more
here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type: `Tuple[MetaUser, urllib3.HTTPResponse]`.

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

## **retrieve**

> retrieve( id, \*\*kwargs )

Get user details

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
    id = 1 # int | A unique integer value identifying this user.

    try:
        (data, response) = api_client.users_api.retrieve(
            id,)
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling UsersApi.retrieve(): %s\n" % e)
```

</div>

### Parameters

| Name   | Type    | Description                                   | Notes |
|--------|---------|-----------------------------------------------|-------|
| **id** | **int** | A unique integer value identifying this user. |       |

There are also optional kwargs that control the function invocation
behavior. [Read more
here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type: `Tuple[MetaUser, urllib3.HTTPResponse]`.

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

## **retrieve_self**

> retrieve_self( \*\*kwargs )

Get details of the current user

Method returns an instance of a user who is currently authenticated

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
        (data, response) = api_client.users_api.retrieve_self()
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling UsersApi.retrieve_self(): %s\n" % e)
```

</div>

### Parameters

This endpoint does not need any parameter.

There are also optional kwargs that control the function invocation
behavior. [Read more
here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type: `Tuple[MetaUser, urllib3.HTTPResponse]`.

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

</div>

</div>
