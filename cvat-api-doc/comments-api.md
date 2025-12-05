<div class="col-12 col-md-9 col-xl-8 ps-md-5" role="main">

1.  [Home](https://docs.cvat.ai/docs/)
2.  [Developers](https://docs.cvat.ai/docs/api_sdk/)
3.  [SDK](https://docs.cvat.ai/docs/api_sdk/sdk/)
4.  [API Reference](https://docs.cvat.ai/docs/api_sdk/sdk/reference/)
5.  [APIs](https://docs.cvat.ai/docs/api_sdk/sdk/reference/apis/)
6.  CommentsApi

<div class="td-content">

# CommentsApi class reference

<div class="article-meta">

</div>

All URIs are relative to *http://localhost*

| Method | HTTP request | Description |
|----|----|----|
| [**create**](../comments-api#create) | **POST** /api/comments | Create a comment |
| [**destroy**](../comments-api#destroy) | **DELETE** /api/comments/{id} | Delete a comment |
| [**list**](../comments-api#list) | **GET** /api/comments | List comments |
| [**partial_update**](../comments-api#partial_update) | **PATCH** /api/comments/{id} | Update a comment |
| [**retrieve**](../comments-api#retrieve) | **GET** /api/comments/{id} | Get comment details |

## **create**

> create( comment_write_request, x_organization=None, org=None,
> org_id=None, \*\*kwargs )

Create a comment

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
    comment_write_request = CommentWriteRequest(
        issue=1,
        message="message_example",
    ) # CommentWriteRequest | 
    x_organization = "X-Organization_example" # str | Organization unique slug (optional)
    org = "org_example" # str | Organization unique slug (optional)
    org_id = 1 # int | Organization identifier (optional)

    try:
        (data, response) = api_client.comments_api.create(
            comment_write_request,
            x_organization=x_organization,
            org=org,
            org_id=org_id,
        )
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling CommentsApi.create(): %s\n" % e)
```

</div>

### Parameters

| Name | Type | Description | Notes |
|----|----|----|----|
| **comment_write_request** | [**CommentWriteRequest**](../../models/comment-write-request) |  |  |
| **x_organization** | **str** | Organization unique slug | \[optional\] |
| **org** | **str** | Organization unique slug | \[optional\] |
| **org_id** | **int** | Organization identifier | \[optional\] |

There are also optional kwargs that control the function invocation
behavior. [Read more
here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type: `Tuple[CommentRead, urllib3.HTTPResponse]`.

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

## **destroy**

> destroy( id, \*\*kwargs )

Delete a comment

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
    id = 1 # int | A unique integer value identifying this comment.

    try:
        api_client.comments_api.destroy(
            id,)
    except exceptions.ApiException as e:
        print("Exception when calling CommentsApi.destroy(): %s\n" % e)
```

</div>

### Parameters

| Name   | Type    | Description                                      | Notes |
|--------|---------|--------------------------------------------------|-------|
| **id** | **int** | A unique integer value identifying this comment. |       |

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

| Status code | Description                  | Response headers |
|-------------|------------------------------|------------------|
| **204**     | The comment has been deleted | \-               |

## **list**

> list( x_organization=None, filter=None, frame_id=None, issue_id=None,
> job_id=None, org=None, org_id=None, owner=None, page=None,
> page_size=None, search=None, sort=None, \*\*kwargs )

List comments

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
    filter = "filter_example" # str |  JSON Logic filter. This filter can be used to perform complex filtering by grouping rules.  For example, using such a filter you can get all resources created by you:      - {\"and\":[{\"==\":[{\"var\":\"owner\"},\"<user>\"]}]}  Details about the syntax used can be found at the link: https://jsonlogic.com/   Available filter_fields: ['owner', 'id', 'issue_id', 'frame_id', 'job_id']. (optional)
    frame_id = 1 # int | A simple equality filter for the frame_id field (optional)
    issue_id = 1 # int | A simple equality filter for the issue_id field (optional)
    job_id = 1 # int | A simple equality filter for the job_id field (optional)
    org = "org_example" # str | Organization unique slug (optional)
    org_id = 1 # int | Organization identifier (optional)
    owner = "owner_example" # str | A simple equality filter for the owner field (optional)
    page = 1 # int | A page number within the paginated result set. (optional)
    page_size = 1 # int | Number of results to return per page. (optional)
    search = "search_example" # str | A search term. Available search_fields: ('owner',) (optional)
    sort = "sort_example" # str | Which field to use when ordering the results. Available ordering_fields: ['owner', 'id', 'issue_id', 'frame_id', 'job_id'] (optional)

    try:
        (data, response) = api_client.comments_api.list(
            x_organization=x_organization,
            filter=filter,
            frame_id=frame_id,
            issue_id=issue_id,
            job_id=job_id,
            org=org,
            org_id=org_id,
            owner=owner,
            page=page,
            page_size=page_size,
            search=search,
            sort=sort,
        )
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling CommentsApi.list(): %s\n" % e)
```

</div>

### Parameters

| Name | Type | Description | Notes |
|----|----|----|----|
| **x_organization** | **str** | Organization unique slug | \[optional\] |
| **filter** | **str** | JSON Logic filter. This filter can be used to perform complex filtering by grouping rules. For example, using such a filter you can get all resources created by you: - {"and":\[{"==":\[{"var":"owner"},""\]}\]} Details about the syntax used can be found at the link: <https://jsonlogic.com/> Available filter_fields: \[‘owner’, ‘id’, ‘issue_id’, ‘frame_id’, ‘job_id’\]. | \[optional\] |
| **frame_id** | **int** | A simple equality filter for the frame_id field | \[optional\] |
| **issue_id** | **int** | A simple equality filter for the issue_id field | \[optional\] |
| **job_id** | **int** | A simple equality filter for the job_id field | \[optional\] |
| **org** | **str** | Organization unique slug | \[optional\] |
| **org_id** | **int** | Organization identifier | \[optional\] |
| **owner** | **str** | A simple equality filter for the owner field | \[optional\] |
| **page** | **int** | A page number within the paginated result set. | \[optional\] |
| **page_size** | **int** | Number of results to return per page. | \[optional\] |
| **search** | **str** | A search term. Available search_fields: (‘owner’,) | \[optional\] |
| **sort** | **str** | Which field to use when ordering the results. Available ordering_fields: \[‘owner’, ‘id’, ‘issue_id’, ‘frame_id’, ‘job_id’\] | \[optional\] |

There are also optional kwargs that control the function invocation
behavior. [Read more
here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type: `Tuple[PaginatedCommentReadList, urllib3.HTTPResponse]`.

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

> partial_update( id, patched_comment_write_request=None, \*\*kwargs )

Update a comment

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
    id = 1 # int | A unique integer value identifying this comment.
    patched_comment_write_request = PatchedCommentWriteRequest(
        message="message_example",
    ) # PatchedCommentWriteRequest |  (optional)

    try:
        (data, response) = api_client.comments_api.partial_update(
            id,
            patched_comment_write_request=patched_comment_write_request,
        )
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling CommentsApi.partial_update(): %s\n" % e)
```

</div>

### Parameters

| Name | Type | Description | Notes |
|----|----|----|----|
| **id** | **int** | A unique integer value identifying this comment. |  |
| **patched_comment_write_request** | [**PatchedCommentWriteRequest**](../../models/patched-comment-write-request) |  | \[optional\] |

There are also optional kwargs that control the function invocation
behavior. [Read more
here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type: `Tuple[CommentRead, urllib3.HTTPResponse]`.

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

Get comment details

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
    id = 1 # int | A unique integer value identifying this comment.

    try:
        (data, response) = api_client.comments_api.retrieve(
            id,)
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling CommentsApi.retrieve(): %s\n" % e)
```

</div>

### Parameters

| Name   | Type    | Description                                      | Notes |
|--------|---------|--------------------------------------------------|-------|
| **id** | **int** | A unique integer value identifying this comment. |       |

There are also optional kwargs that control the function invocation
behavior. [Read more
here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type: `Tuple[CommentRead, urllib3.HTTPResponse]`.

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
