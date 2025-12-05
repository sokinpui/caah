<div class="col-12 col-md-9 col-xl-8 ps-md-5" role="main">

1.  [Home](https://docs.cvat.ai/docs/)
2.  [Developers](https://docs.cvat.ai/docs/api_sdk/)
3.  [SDK](https://docs.cvat.ai/docs/api_sdk/sdk/)
4.  [API Reference](https://docs.cvat.ai/docs/api_sdk/sdk/reference/)
5.  [APIs](https://docs.cvat.ai/docs/api_sdk/sdk/reference/apis/)
6.  EventsApi

<div class="td-content">

# EventsApi class reference

<div class="article-meta">

</div>

All URIs are relative to *http://localhost*

| Method | HTTP request | Description |
|----|----|----|
| [**create**](../events-api#create) | **POST** /api/events | Log client events |
| [**create_export**](../events-api#create_export) | **POST** /api/events/export | Initiate a process to export events |
| [**list**](../events-api#list) | **GET** /api/events | Get an event log |

## **create**

> create( client_events_request, x_organization=None, org=None,
> org_id=None, \*\*kwargs )

Log client events

Sends logs to the Clickhouse if it is connected

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
    client_events_request = ClientEventsRequest(
        events=[
            EventRequest(
                scope="scope_example",
                obj_name="obj_name_example",
                obj_id=1,
                obj_val="obj_val_example",
                source="source_example",
                timestamp=dateutil_parser('1970-01-01T00:00:00.00Z'),
                count=1,
                duration=0,
                project_id=1,
                task_id=1,
                job_id=1,
                user_id=1,
                user_name="user_name_example",
                user_email="user_email_example",
                org_id=1,
                org_slug="org_slug_example",
                payload="payload_example",
            ),
        ],
        previous_event=ClientEventsRequestPreviousEvent(None),
        timestamp=dateutil_parser('1970-01-01T00:00:00.00Z'),
    ) # ClientEventsRequest | 
    x_organization = "X-Organization_example" # str | Organization unique slug (optional)
    org = "org_example" # str | Organization unique slug (optional)
    org_id = 1 # int | Organization identifier (optional)

    try:
        (data, response) = api_client.events_api.create(
            client_events_request,
            x_organization=x_organization,
            org=org,
            org_id=org_id,
        )
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling EventsApi.create(): %s\n" % e)
```

</div>

### Parameters

| Name | Type | Description | Notes |
|----|----|----|----|
| **client_events_request** | [**ClientEventsRequest**](../../models/client-events-request) |  |  |
| **x_organization** | **str** | Organization unique slug | \[optional\] |
| **org** | **str** | Organization unique slug | \[optional\] |
| **org_id** | **int** | Organization identifier | \[optional\] |

There are also optional kwargs that control the function invocation
behavior. [Read more
here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type: `Tuple[ClientEvents, urllib3.HTTPResponse]`.

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

## **create_export**

> create_export( cloud_storage_id=None, filename=None, \_from=None,
> job_id=None, location=None, org_id=None, project_id=None,
> task_id=None, to=None, user_id=None, \*\*kwargs )

Initiate a process to export events

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
    cloud_storage_id = 1 # int | Storage id (optional)
    filename = "filename_example" # str | Desired output file name (optional)
    _from = dateutil_parser('1970-01-01T00:00:00.00Z') # datetime | UTC start date for events filtration. Default is the minimal time. (optional)
    job_id = 1 # int | Filter events by job ID (optional)
    location = "cloud_storage" # str | Where need to save events file (optional)
    org_id = 1 # int | Filter events by organization ID (optional)
    project_id = 1 # int | Filter events by project ID (optional)
    task_id = 1 # int | Filter events by task ID (optional)
    to = dateutil_parser('1970-01-01T00:00:00.00Z') # datetime | UTC end date for events filtration. Default is the current time. (optional)
    user_id = 1 # int | Filter events by user ID (optional)

    try:
        (data, response) = api_client.events_api.create_export(
            cloud_storage_id=cloud_storage_id,
            filename=filename,
            _from=_from,
            job_id=job_id,
            location=location,
            org_id=org_id,
            project_id=project_id,
            task_id=task_id,
            to=to,
            user_id=user_id,
        )
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling EventsApi.create_export(): %s\n" % e)
```

</div>

### Parameters

| Name | Type | Description | Notes |
|----|----|----|----|
| **cloud_storage_id** | **int** | Storage id | \[optional\] |
| **filename** | **str** | Desired output file name | \[optional\] |
| **\_from** | **datetime** | UTC start date for events filtration. Default is the minimal time. | \[optional\] |
| **job_id** | **int** | Filter events by job ID | \[optional\] |
| **location** | **str** | Where need to save events file | \[optional\] |
| **org_id** | **int** | Filter events by organization ID | \[optional\] |
| **project_id** | **int** | Filter events by project ID | \[optional\] |
| **task_id** | **int** | Filter events by task ID | \[optional\] |
| **to** | **datetime** | UTC end date for events filtration. Default is the current time. | \[optional\] |
| **user_id** | **int** | Filter events by user ID | \[optional\] |

There are also optional kwargs that control the function invocation
behavior. [Read more
here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type: `Tuple[RqId, urllib3.HTTPResponse]`.

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
| **202**     |             | \-               |

## **list**

> list( action=None, filename=None, \_from=None, job_id=None,
> org_id=None, project_id=None, query_id=None, task_id=None, to=None,
> user_id=None, \*\*kwargs )

Get an event log

The log is returned in the CSV format.

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
    action = "download" # str | Used to start downloading process after annotation file had been created (optional) if omitted the server will use the default value of "download"
    filename = "filename_example" # str | Desired output file name (optional)
    _from = dateutil_parser('1970-01-01T00:00:00.00Z') # datetime | UTC start date for events filtration. Default is the minimal time. (optional)
    job_id = 1 # int | Filter events by job ID (optional)
    org_id = 1 # int | Filter events by organization ID (optional)
    project_id = 1 # int | Filter events by project ID (optional)
    query_id = "query_id_example" # str | ID of query request that need to check or download (optional)
    task_id = 1 # int | Filter events by task ID (optional)
    to = dateutil_parser('1970-01-01T00:00:00.00Z') # datetime | UTC end date for events filtration. Default is the current time. (optional)
    user_id = 1 # int | Filter events by user ID (optional)

    try:
        api_client.events_api.list(
            action=action,
            filename=filename,
            _from=_from,
            job_id=job_id,
            org_id=org_id,
            project_id=project_id,
            query_id=query_id,
            task_id=task_id,
            to=to,
            user_id=user_id,
        )
    except exceptions.ApiException as e:
        print("Exception when calling EventsApi.list(): %s\n" % e)
```

</div>

### Parameters

| Name | Type | Description | Notes |
|----|----|----|----|
| **action** | **str** | Used to start downloading process after annotation file had been created | \[optional\] if omitted the server will use the default value of “download” |
| **filename** | **str** | Desired output file name | \[optional\] |
| **\_from** | **datetime** | UTC start date for events filtration. Default is the minimal time. | \[optional\] |
| **job_id** | **int** | Filter events by job ID | \[optional\] |
| **org_id** | **int** | Filter events by organization ID | \[optional\] |
| **project_id** | **int** | Filter events by project ID | \[optional\] |
| **query_id** | **str** | ID of query request that need to check or download | \[optional\] |
| **task_id** | **int** | Filter events by task ID | \[optional\] |
| **to** | **datetime** | UTC end date for events filtration. Default is the current time. | \[optional\] |
| **user_id** | **int** | Filter events by user ID | \[optional\] |

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

| Status code | Description                              | Response headers |
|-------------|------------------------------------------|------------------|
| **200**     | Download of file started                 | \-               |
| **201**     | CSV log file is ready for downloading    | \-               |
| **202**     | Creating a CSV log file has been started | \-               |

</div>

</div>
