<div class="col-12 col-md-9 col-xl-8 ps-md-5" role="main">

1.  [Home](https://docs.cvat.ai/docs/)
2.  [Developers](https://docs.cvat.ai/docs/api_sdk/)
3.  [SDK](https://docs.cvat.ai/docs/api_sdk/sdk/)
4.  [API Reference](https://docs.cvat.ai/docs/api_sdk/sdk/reference/)
5.  [APIs](https://docs.cvat.ai/docs/api_sdk/sdk/reference/apis/)
6.  MembershipsApi

<div class="td-content">

# MembershipsApi class reference

<div class="article-meta">

</div>

All URIs are relative to *http://localhost*

| Method | HTTP request | Description |
|----|----|----|
| [**destroy**](../memberships-api#destroy) | **DELETE** /api/memberships/{id} | Delete a membership |
| [**list**](../memberships-api#list) | **GET** /api/memberships | List memberships |
| [**partial_update**](../memberships-api#partial_update) | **PATCH** /api/memberships/{id} | Update a membership |
| [**retrieve**](../memberships-api#retrieve) | **GET** /api/memberships/{id} | Get membership details |

## **destroy**

> destroy( id, \*\*kwargs )

Delete a membership

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
    id = 1 # int | A unique integer value identifying this membership.

    try:
        api_client.memberships_api.destroy(
            id,)
    except exceptions.ApiException as e:
        print("Exception when calling MembershipsApi.destroy(): %s\n" % e)
```

</div>

### Parameters

| Name   | Type    | Description                                         | Notes |
|--------|---------|-----------------------------------------------------|-------|
| **id** | **int** | A unique integer value identifying this membership. |       |

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

| Status code | Description                     | Response headers |
|-------------|---------------------------------|------------------|
| **204**     | The membership has been deleted | \-               |

## **list**

> list( x_organization=None, filter=None, org=None, org_id=None,
> page=None, page_size=None, role=None, search=None, sort=None,
> user=None, \*\*kwargs )

List memberships

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
    filter = "filter_example" # str |  JSON Logic filter. This filter can be used to perform complex filtering by grouping rules.  For example, using such a filter you can get all resources created by you:      - {\"and\":[{\"==\":[{\"var\":\"owner\"},\"<user>\"]}]}  Details about the syntax used can be found at the link: https://jsonlogic.com/   Available filter_fields: ['user', 'role', 'id']. (optional)
    org = "org_example" # str | Organization unique slug (optional)
    org_id = 1 # int | Organization identifier (optional)
    page = 1 # int | A page number within the paginated result set. (optional)
    page_size = 1 # int | Number of results to return per page. (optional)
    role = "worker" # str | A simple equality filter for the role field (optional)
    search = "search_example" # str | A search term. Available search_fields: ('user', 'role') (optional)
    sort = "sort_example" # str | Which field to use when ordering the results. Available ordering_fields: ['user', 'role', 'id'] (optional)
    user = "user_example" # str | A simple equality filter for the user field (optional)

    try:
        (data, response) = api_client.memberships_api.list(
            x_organization=x_organization,
            filter=filter,
            org=org,
            org_id=org_id,
            page=page,
            page_size=page_size,
            role=role,
            search=search,
            sort=sort,
            user=user,
        )
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling MembershipsApi.list(): %s\n" % e)
```

</div>

### Parameters

| Name | Type | Description | Notes |
|----|----|----|----|
| **x_organization** | **str** | Organization unique slug | \[optional\] |
| **filter** | **str** | JSON Logic filter. This filter can be used to perform complex filtering by grouping rules. For example, using such a filter you can get all resources created by you: - {"and":\[{"==":\[{"var":"owner"},""\]}\]} Details about the syntax used can be found at the link: <https://jsonlogic.com/> Available filter_fields: \[‘user’, ‘role’, ‘id’\]. | \[optional\] |
| **org** | **str** | Organization unique slug | \[optional\] |
| **org_id** | **int** | Organization identifier | \[optional\] |
| **page** | **int** | A page number within the paginated result set. | \[optional\] |
| **page_size** | **int** | Number of results to return per page. | \[optional\] |
| **role** | **str** | A simple equality filter for the role field | \[optional\] |
| **search** | **str** | A search term. Available search_fields: (‘user’, ‘role’) | \[optional\] |
| **sort** | **str** | Which field to use when ordering the results. Available ordering_fields: \[‘user’, ‘role’, ‘id’\] | \[optional\] |
| **user** | **str** | A simple equality filter for the user field | \[optional\] |

There are also optional kwargs that control the function invocation
behavior. [Read more
here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type:
`Tuple[PaginatedMembershipReadList, urllib3.HTTPResponse]`.

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

> partial_update( id, patched_membership_write_request=None, \*\*kwargs
> )

Update a membership

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
    id = 1 # int | A unique integer value identifying this membership.
    patched_membership_write_request = PatchedMembershipWriteRequest(
        role=RoleEnum("worker"),
    ) # PatchedMembershipWriteRequest |  (optional)

    try:
        (data, response) = api_client.memberships_api.partial_update(
            id,
            patched_membership_write_request=patched_membership_write_request,
        )
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling MembershipsApi.partial_update(): %s\n" % e)
```

</div>

### Parameters

| Name | Type | Description | Notes |
|----|----|----|----|
| **id** | **int** | A unique integer value identifying this membership. |  |
| **patched_membership_write_request** | [**PatchedMembershipWriteRequest**](../../models/patched-membership-write-request) |  | \[optional\] |

There are also optional kwargs that control the function invocation
behavior. [Read more
here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type: `Tuple[MembershipRead, urllib3.HTTPResponse]`.

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

Get membership details

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
    id = 1 # int | A unique integer value identifying this membership.

    try:
        (data, response) = api_client.memberships_api.retrieve(
            id,)
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling MembershipsApi.retrieve(): %s\n" % e)
```

</div>

### Parameters

| Name   | Type    | Description                                         | Notes |
|--------|---------|-----------------------------------------------------|-------|
| **id** | **int** | A unique integer value identifying this membership. |       |

There are also optional kwargs that control the function invocation
behavior. [Read more
here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type: `Tuple[MembershipRead, urllib3.HTTPResponse]`.

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
