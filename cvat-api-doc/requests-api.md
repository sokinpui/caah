<div class="col-12 col-md-9 col-xl-8 ps-md-5" role="main">

1.  [Home](https://docs.cvat.ai/docs/)
2.  [Developers](https://docs.cvat.ai/docs/api_sdk/)
3.  [SDK](https://docs.cvat.ai/docs/api_sdk/sdk/)
4.  [API Reference](https://docs.cvat.ai/docs/api_sdk/sdk/reference/)
5.  [APIs](https://docs.cvat.ai/docs/api_sdk/sdk/reference/apis/)
6.  RequestsApi

<div class="td-content">

# RequestsApi class reference

<div class="article-meta">

</div>

All URIs are relative to *http://localhost*

| Method | HTTP request | Description |
|----|----|----|
| [**create_cancel**](../requests-api#create_cancel) | **POST** /api/requests/{id}/cancel | Cancel request |
| [**list**](../requests-api#list) | **GET** /api/requests | List requests |
| [**retrieve**](../requests-api#retrieve) | **GET** /api/requests/{id} | Get request details |

## **create_cancel**

> create_cancel( id, \*\*kwargs )

Cancel request

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
    id = "id_example" # str | 

    try:
        api_client.requests_api.create_cancel(
            id,)
    except exceptions.ApiException as e:
        print("Exception when calling RequestsApi.create_cancel(): %s\n" % e)
```

</div>

### Parameters

| Name   | Type    | Description | Notes |
|--------|---------|-------------|-------|
| **id** | **str** |             |       |

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

| Status code | Description                    | Response headers |
|-------------|--------------------------------|------------------|
| **200**     | The request has been cancelled | \-               |

## **list**

> list( action=None, filter=None, format=None, job_id=None, org=None,
> page=None, page_size=None, project_id=None, sort=None, status=None,
> subresource=None, target=None, task_id=None, \*\*kwargs )

List requests

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
    action = "action_example" # str | A simple equality filter for the action field (optional)
    filter = "filter_example" # str |  JSON Logic filter. This filter can be used to perform complex filtering by grouping rules.  Details about the syntax used can be found at the link: https://jsonlogic.com/   Available filter_fields: ['status', 'project_id', 'task_id', 'job_id', 'action', 'target', 'subresource', 'format']. (optional)
    format = "format_example" # str | A simple equality filter for the format field (optional)
    job_id = 1 # int | A simple equality filter for the job_id field (optional)
    org = "org_example" # str | A simple equality filter for the org field (optional)
    page = 1 # int | A page number within the paginated result set. (optional)
    page_size = 1 # int | Number of results to return per page. (optional)
    project_id = 1 # int | A simple equality filter for the project_id field (optional)
    sort = "sort_example" # str | Which field to use when ordering the results. Available ordering_fields: ['created_date', 'status', 'action'] (optional)
    status = "queued" # str | A simple equality filter for the status field (optional)
    subresource = "subresource_example" # str | A simple equality filter for the subresource field (optional)
    target = "target_example" # str | A simple equality filter for the target field (optional)
    task_id = 1 # int | A simple equality filter for the task_id field (optional)

    try:
        (data, response) = api_client.requests_api.list(
            action=action,
            filter=filter,
            format=format,
            job_id=job_id,
            org=org,
            page=page,
            page_size=page_size,
            project_id=project_id,
            sort=sort,
            status=status,
            subresource=subresource,
            target=target,
            task_id=task_id,
        )
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling RequestsApi.list(): %s\n" % e)
```

</div>

### Parameters

| Name | Type | Description | Notes |
|----|----|----|----|
| **action** | **str** | A simple equality filter for the action field | \[optional\] |
| **filter** | **str** | JSON Logic filter. This filter can be used to perform complex filtering by grouping rules. Details about the syntax used can be found at the link: <https://jsonlogic.com/> Available filter_fields: \[‘status’, ‘project_id’, ’task_id’, ‘job_id’, ‘action’, ’target’, ‘subresource’, ‘format’\]. | \[optional\] |
| **format** | **str** | A simple equality filter for the format field | \[optional\] |
| **job_id** | **int** | A simple equality filter for the job_id field | \[optional\] |
| **org** | **str** | A simple equality filter for the org field | \[optional\] |
| **page** | **int** | A page number within the paginated result set. | \[optional\] |
| **page_size** | **int** | Number of results to return per page. | \[optional\] |
| **project_id** | **int** | A simple equality filter for the project_id field | \[optional\] |
| **sort** | **str** | Which field to use when ordering the results. Available ordering_fields: \[‘created_date’, ‘status’, ‘action’\] | \[optional\] |
| **status** | **str** | A simple equality filter for the status field | \[optional\] |
| **subresource** | **str** | A simple equality filter for the subresource field | \[optional\] |
| **target** | **str** | A simple equality filter for the target field | \[optional\] |
| **task_id** | **int** | A simple equality filter for the task_id field | \[optional\] |

There are also optional kwargs that control the function invocation
behavior. [Read more
here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type: `Tuple[PaginatedRequestList, urllib3.HTTPResponse]`.

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

## **retrieve**

> retrieve( id, \*\*kwargs )

Get request details

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
    id = "id_example" # str | 

    try:
        (data, response) = api_client.requests_api.retrieve(
            id,)
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling RequestsApi.retrieve(): %s\n" % e)
```

</div>

### Parameters

| Name   | Type    | Description | Notes |
|--------|---------|-------------|-------|
| **id** | **str** |             |       |

There are also optional kwargs that control the function invocation
behavior. [Read more
here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type: `Tuple[Request, urllib3.HTTPResponse]`.

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
