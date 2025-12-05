<div class="col-12 col-md-9 col-xl-8 ps-md-5" role="main">

1.  [Home](https://docs.cvat.ai/docs/)
2.  [Developers](https://docs.cvat.ai/docs/api_sdk/)
3.  [SDK](https://docs.cvat.ai/docs/api_sdk/sdk/)
4.  [API Reference](https://docs.cvat.ai/docs/api_sdk/sdk/reference/)
5.  [APIs](https://docs.cvat.ai/docs/api_sdk/sdk/reference/apis/)
6.  ConsensusApi

<div class="td-content">

# ConsensusApi class reference

<div class="article-meta">

</div>

All URIs are relative to *http://localhost*

| Method | HTTP request | Description |
|----|----|----|
| [**create_merge**](../consensus-api#create_merge) | **POST** /api/consensus/merges | Create a consensus merge |
| [**list_settings**](../consensus-api#list_settings) | **GET** /api/consensus/settings | List consensus settings instances |
| [**partial_update_settings**](../consensus-api#partial_update_settings) | **PATCH** /api/consensus/settings/{id} | Update a consensus settings instance |
| [**retrieve_settings**](../consensus-api#retrieve_settings) | **GET** /api/consensus/settings/{id} | Get consensus settings instance details |

## **create_merge**

> create_merge( consensus_merge_create_request=None, \*\*kwargs )

Create a consensus merge

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
    consensus_merge_create_request = ConsensusMergeCreateRequest(
        task_id=1,
        job_id=1,
    ) # ConsensusMergeCreateRequest |  (optional)

    try:
        (data, response) = api_client.consensus_api.create_merge(
            consensus_merge_create_request=consensus_merge_create_request,
        )
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling ConsensusApi.create_merge(): %s\n" % e)
```

</div>

### Parameters

| Name | Type | Description | Notes |
|----|----|----|----|
| **consensus_merge_create_request** | [**ConsensusMergeCreateRequest**](../../models/consensus-merge-create-request) |  | \[optional\] |

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

- **Content-Type**: application/json
- **Accept**: application/vnd.cvat+json

### HTTP response details

| Status code | Description | Response headers |
|----|----|----|
| **202** | A consensus merge request has been enqueued, the request id is returned. The request status can be checked by using common requests API: GET /api/requests/\<rq_id\> | \- |
| **400** | Invalid or failed request, check the response data for details | \- |

## **list_settings**

> list_settings( x_organization=None, filter=None, org=None,
> org_id=None, page=None, page_size=None, sort=None, task_id=None,
> \*\*kwargs )

List consensus settings instances

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
    filter = "filter_example" # str |  JSON Logic filter. This filter can be used to perform complex filtering by grouping rules.  For example, using such a filter you can get all resources created by you:      - {\"and\":[{\"==\":[{\"var\":\"owner\"},\"<user>\"]}]}  Details about the syntax used can be found at the link: https://jsonlogic.com/   Available filter_fields: ['id', 'task_id']. (optional)
    org = "org_example" # str | Organization unique slug (optional)
    org_id = 1 # int | Organization identifier (optional)
    page = 1 # int | A page number within the paginated result set. (optional)
    page_size = 1 # int | Number of results to return per page. (optional)
    sort = "sort_example" # str | Which field to use when ordering the results. Available ordering_fields: ['id'] (optional)
    task_id = 1 # int | A simple equality filter for the task_id field (optional)

    try:
        (data, response) = api_client.consensus_api.list_settings(
            x_organization=x_organization,
            filter=filter,
            org=org,
            org_id=org_id,
            page=page,
            page_size=page_size,
            sort=sort,
            task_id=task_id,
        )
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling ConsensusApi.list_settings(): %s\n" % e)
```

</div>

### Parameters

| Name | Type | Description | Notes |
|----|----|----|----|
| **x_organization** | **str** | Organization unique slug | \[optional\] |
| **filter** | **str** | JSON Logic filter. This filter can be used to perform complex filtering by grouping rules. For example, using such a filter you can get all resources created by you: - {"and":\[{"==":\[{"var":"owner"},""\]}\]} Details about the syntax used can be found at the link: <https://jsonlogic.com/> Available filter_fields: \[‘id’, ’task_id’\]. | \[optional\] |
| **org** | **str** | Organization unique slug | \[optional\] |
| **org_id** | **int** | Organization identifier | \[optional\] |
| **page** | **int** | A page number within the paginated result set. | \[optional\] |
| **page_size** | **int** | Number of results to return per page. | \[optional\] |
| **sort** | **str** | Which field to use when ordering the results. Available ordering_fields: \[‘id’\] | \[optional\] |
| **task_id** | **int** | A simple equality filter for the task_id field | \[optional\] |

There are also optional kwargs that control the function invocation
behavior. [Read more
here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type:
`Tuple[PaginatedConsensusSettingsList, urllib3.HTTPResponse]`.

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

## **partial_update_settings**

> partial_update_settings( id, patched_consensus_settings_request=None,
> \*\*kwargs )

Update a consensus settings instance

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
    id = 1 # int | An id of a consensus settings instance
    patched_consensus_settings_request = PatchedConsensusSettingsRequest(
        iou_threshold=0,
        quorum=0,
    ) # PatchedConsensusSettingsRequest |  (optional)

    try:
        (data, response) = api_client.consensus_api.partial_update_settings(
            id,
            patched_consensus_settings_request=patched_consensus_settings_request,
        )
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling ConsensusApi.partial_update_settings(): %s\n" % e)
```

</div>

### Parameters

| Name | Type | Description | Notes |
|----|----|----|----|
| **id** | **int** | An id of a consensus settings instance |  |
| **patched_consensus_settings_request** | [**PatchedConsensusSettingsRequest**](../../models/patched-consensus-settings-request) |  | \[optional\] |

There are also optional kwargs that control the function invocation
behavior. [Read more
here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type: `Tuple[ConsensusSettings, urllib3.HTTPResponse]`.

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

## **retrieve_settings**

> retrieve_settings( id, \*\*kwargs )

Get consensus settings instance details

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
    id = 1 # int | An id of a consensus settings instance

    try:
        (data, response) = api_client.consensus_api.retrieve_settings(
            id,)
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling ConsensusApi.retrieve_settings(): %s\n" % e)
```

</div>

### Parameters

| Name   | Type    | Description                            | Notes |
|--------|---------|----------------------------------------|-------|
| **id** | **int** | An id of a consensus settings instance |       |

There are also optional kwargs that control the function invocation
behavior. [Read more
here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type: `Tuple[ConsensusSettings, urllib3.HTTPResponse]`.

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
