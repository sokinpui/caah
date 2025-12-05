<div class="col-12 col-md-9 col-xl-8 ps-md-5" role="main">

1.  [Home](https://docs.cvat.ai/docs/)
2.  [Developers](https://docs.cvat.ai/docs/api_sdk/)
3.  [SDK](https://docs.cvat.ai/docs/api_sdk/sdk/)
4.  [API Reference](https://docs.cvat.ai/docs/api_sdk/sdk/reference/)
5.  [APIs](https://docs.cvat.ai/docs/api_sdk/sdk/reference/apis/)
6.  IssuesApi

<div class="td-content">

# IssuesApi class reference

<div class="article-meta">

</div>

All URIs are relative to *http://localhost*

| Method | HTTP request | Description |
|----|----|----|
| [**create**](../issues-api#create) | **POST** /api/issues | Create an issue |
| [**destroy**](../issues-api#destroy) | **DELETE** /api/issues/{id} | Delete an issue |
| [**list**](../issues-api#list) | **GET** /api/issues | List issues |
| [**partial_update**](../issues-api#partial_update) | **PATCH** /api/issues/{id} | Update an issue |
| [**retrieve**](../issues-api#retrieve) | **GET** /api/issues/{id} | Get issue details |

## **create**

> create( issue_write_request, x_organization=None, org=None,
> org_id=None, \*\*kwargs )

Create an issue

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
    issue_write_request = IssueWriteRequest(
        frame=0,
        position=[
            3.14,
        ],
        job=1,
        assignee=1,
        message="message_example",
        resolved=True,
    ) # IssueWriteRequest | 
    x_organization = "X-Organization_example" # str | Organization unique slug (optional)
    org = "org_example" # str | Organization unique slug (optional)
    org_id = 1 # int | Organization identifier (optional)

    try:
        (data, response) = api_client.issues_api.create(
            issue_write_request,
            x_organization=x_organization,
            org=org,
            org_id=org_id,
        )
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling IssuesApi.create(): %s\n" % e)
```

</div>

### Parameters

| Name | Type | Description | Notes |
|----|----|----|----|
| **issue_write_request** | [**IssueWriteRequest**](../../models/issue-write-request) |  |  |
| **x_organization** | **str** | Organization unique slug | \[optional\] |
| **org** | **str** | Organization unique slug | \[optional\] |
| **org_id** | **int** | Organization identifier | \[optional\] |

There are also optional kwargs that control the function invocation
behavior. [Read more
here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type: `Tuple[IssueRead, urllib3.HTTPResponse]`.

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

Delete an issue

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
    id = 1 # int | A unique integer value identifying this issue.

    try:
        api_client.issues_api.destroy(
            id,)
    except exceptions.ApiException as e:
        print("Exception when calling IssuesApi.destroy(): %s\n" % e)
```

</div>

### Parameters

| Name   | Type    | Description                                    | Notes |
|--------|---------|------------------------------------------------|-------|
| **id** | **int** | A unique integer value identifying this issue. |       |

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

| Status code | Description                | Response headers |
|-------------|----------------------------|------------------|
| **204**     | The issue has been deleted | \-               |

## **list**

> list( x_organization=None, assignee=None, filter=None, frame_id=None,
> job_id=None, org=None, org_id=None, owner=None, page=None,
> page_size=None, resolved=None, search=None, sort=None, task_id=None,
> \*\*kwargs )

List issues

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
    assignee = "assignee_example" # str | A simple equality filter for the assignee field (optional)
    filter = "filter_example" # str |  JSON Logic filter. This filter can be used to perform complex filtering by grouping rules.  For example, using such a filter you can get all resources created by you:      - {\"and\":[{\"==\":[{\"var\":\"owner\"},\"<user>\"]}]}  Details about the syntax used can be found at the link: https://jsonlogic.com/   Available filter_fields: ['owner', 'assignee', 'id', 'job_id', 'task_id', 'resolved', 'frame_id']. (optional)
    frame_id = 1 # int | A simple equality filter for the frame_id field (optional)
    job_id = 1 # int | A simple equality filter for the job_id field (optional)
    org = "org_example" # str | Organization unique slug (optional)
    org_id = 1 # int | Organization identifier (optional)
    owner = "owner_example" # str | A simple equality filter for the owner field (optional)
    page = 1 # int | A page number within the paginated result set. (optional)
    page_size = 1 # int | Number of results to return per page. (optional)
    resolved = True # bool | A simple equality filter for the resolved field (optional)
    search = "search_example" # str | A search term. Available search_fields: ('owner', 'assignee') (optional)
    sort = "sort_example" # str | Which field to use when ordering the results. Available ordering_fields: ['owner', 'assignee', 'id', 'job_id', 'task_id', 'resolved', 'frame_id'] (optional)
    task_id = 1 # int | A simple equality filter for the task_id field (optional)

    try:
        (data, response) = api_client.issues_api.list(
            x_organization=x_organization,
            assignee=assignee,
            filter=filter,
            frame_id=frame_id,
            job_id=job_id,
            org=org,
            org_id=org_id,
            owner=owner,
            page=page,
            page_size=page_size,
            resolved=resolved,
            search=search,
            sort=sort,
            task_id=task_id,
        )
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling IssuesApi.list(): %s\n" % e)
```

</div>

### Parameters

| Name | Type | Description | Notes |
|----|----|----|----|
| **x_organization** | **str** | Organization unique slug | \[optional\] |
| **assignee** | **str** | A simple equality filter for the assignee field | \[optional\] |
| **filter** | **str** | JSON Logic filter. This filter can be used to perform complex filtering by grouping rules. For example, using such a filter you can get all resources created by you: - {"and":\[{"==":\[{"var":"owner"},""\]}\]} Details about the syntax used can be found at the link: <https://jsonlogic.com/> Available filter_fields: \[‘owner’, ‘assignee’, ‘id’, ‘job_id’, ’task_id’, ‘resolved’, ‘frame_id’\]. | \[optional\] |
| **frame_id** | **int** | A simple equality filter for the frame_id field | \[optional\] |
| **job_id** | **int** | A simple equality filter for the job_id field | \[optional\] |
| **org** | **str** | Organization unique slug | \[optional\] |
| **org_id** | **int** | Organization identifier | \[optional\] |
| **owner** | **str** | A simple equality filter for the owner field | \[optional\] |
| **page** | **int** | A page number within the paginated result set. | \[optional\] |
| **page_size** | **int** | Number of results to return per page. | \[optional\] |
| **resolved** | **bool** | A simple equality filter for the resolved field | \[optional\] |
| **search** | **str** | A search term. Available search_fields: (‘owner’, ‘assignee’) | \[optional\] |
| **sort** | **str** | Which field to use when ordering the results. Available ordering_fields: \[‘owner’, ‘assignee’, ‘id’, ‘job_id’, ’task_id’, ‘resolved’, ‘frame_id’\] | \[optional\] |
| **task_id** | **int** | A simple equality filter for the task_id field | \[optional\] |

There are also optional kwargs that control the function invocation
behavior. [Read more
here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type: `Tuple[PaginatedIssueReadList, urllib3.HTTPResponse]`.

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

> partial_update( id, patched_issue_write_request=None, \*\*kwargs )

Update an issue

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
    id = 1 # int | A unique integer value identifying this issue.
    patched_issue_write_request = PatchedIssueWriteRequest(
        position=[
            3.14,
        ],
        assignee=1,
        resolved=True,
    ) # PatchedIssueWriteRequest |  (optional)

    try:
        (data, response) = api_client.issues_api.partial_update(
            id,
            patched_issue_write_request=patched_issue_write_request,
        )
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling IssuesApi.partial_update(): %s\n" % e)
```

</div>

### Parameters

| Name | Type | Description | Notes |
|----|----|----|----|
| **id** | **int** | A unique integer value identifying this issue. |  |
| **patched_issue_write_request** | [**PatchedIssueWriteRequest**](../../models/patched-issue-write-request) |  | \[optional\] |

There are also optional kwargs that control the function invocation
behavior. [Read more
here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type: `Tuple[IssueRead, urllib3.HTTPResponse]`.

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

Get issue details

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
    id = 1 # int | A unique integer value identifying this issue.

    try:
        (data, response) = api_client.issues_api.retrieve(
            id,)
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling IssuesApi.retrieve(): %s\n" % e)
```

</div>

### Parameters

| Name   | Type    | Description                                    | Notes |
|--------|---------|------------------------------------------------|-------|
| **id** | **int** | A unique integer value identifying this issue. |       |

There are also optional kwargs that control the function invocation
behavior. [Read more
here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type: `Tuple[IssueRead, urllib3.HTTPResponse]`.

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
