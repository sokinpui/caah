<div class="col-12 col-md-9 col-xl-8 ps-md-5" role="main">

1.  [Home](https://docs.cvat.ai/docs/)
2.  [Developers](https://docs.cvat.ai/docs/api_sdk/)
3.  [SDK](https://docs.cvat.ai/docs/api_sdk/sdk/)
4.  [API Reference](https://docs.cvat.ai/docs/api_sdk/sdk/reference/)
5.  [APIs](https://docs.cvat.ai/docs/api_sdk/sdk/reference/apis/)
6.  WebhooksApi

<div class="td-content">

# WebhooksApi class reference

<div class="article-meta">

</div>

All URIs are relative to *http://localhost*

| Method | HTTP request | Description |
|----|----|----|
| [**create**](../webhooks-api#create) | **POST** /api/webhooks | Create a webhook |
| [**create_deliveries_redelivery**](../webhooks-api#create_deliveries_redelivery) | **POST** /api/webhooks/{id}/deliveries/{delivery_id}/redelivery | Redeliver a webhook delivery |
| [**create_ping**](../webhooks-api#create_ping) | **POST** /api/webhooks/{id}/ping | Send a ping webhook |
| [**destroy**](../webhooks-api#destroy) | **DELETE** /api/webhooks/{id} | Delete a webhook |
| [**list**](../webhooks-api#list) | **GET** /api/webhooks | List webhooks |
| [**list_deliveries**](../webhooks-api#list_deliveries) | **GET** /api/webhooks/{id}/deliveries | List deliveries for a webhook |
| [**partial_update**](../webhooks-api#partial_update) | **PATCH** /api/webhooks/{id} | Update a webhook |
| [**retrieve**](../webhooks-api#retrieve) | **GET** /api/webhooks/{id} | Get webhook details |
| [**retrieve_deliveries**](../webhooks-api#retrieve_deliveries) | **GET** /api/webhooks/{id}/deliveries/{delivery_id} | Get details of a webhook delivery |
| [**retrieve_events**](../webhooks-api#retrieve_events) | **GET** /api/webhooks/events | List available webhook events |
| [**update**](../webhooks-api#update) | **PUT** /api/webhooks/{id} | Replace a webhook |

## **create**

> create( webhook_write_request, x_organization=None, org=None,
> org_id=None, \*\*kwargs )

Create a webhook

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
    webhook_write_request = WebhookWriteRequest(
        target_url="target_url_example",
        description="description_example",
        type=WebhookType("organization"),
        content_type=WebhookContentType("application/json"),
        secret="secret_example",
        is_active=True,
        enable_ssl=True,
        project_id=1,
        events=[
            EventsEnum("create:comment"),
        ],
    ) # WebhookWriteRequest | 
    x_organization = "X-Organization_example" # str | Organization unique slug (optional)
    org = "org_example" # str | Organization unique slug (optional)
    org_id = 1 # int | Organization identifier (optional)

    try:
        (data, response) = api_client.webhooks_api.create(
            webhook_write_request,
            x_organization=x_organization,
            org=org,
            org_id=org_id,
        )
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling WebhooksApi.create(): %s\n" % e)
```

</div>

### Parameters

| Name | Type | Description | Notes |
|----|----|----|----|
| **webhook_write_request** | [**WebhookWriteRequest**](../../models/webhook-write-request) |  |  |
| **x_organization** | **str** | Organization unique slug | \[optional\] |
| **org** | **str** | Organization unique slug | \[optional\] |
| **org_id** | **int** | Organization identifier | \[optional\] |

There are also optional kwargs that control the function invocation
behavior. [Read more
here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type: `Tuple[WebhookRead, urllib3.HTTPResponse]`.

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

## **create_deliveries_redelivery**

> create_deliveries_redelivery( delivery_id, id, \*\*kwargs )

Redeliver a webhook delivery

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
    delivery_id = "4" # str | 
    id = 1 # int | A unique integer value identifying this webhook.

    try:
        api_client.webhooks_api.create_deliveries_redelivery(
            delivery_id,
            id,)
    except exceptions.ApiException as e:
        print("Exception when calling WebhooksApi.create_deliveries_redelivery(): %s\n" % e)
```

</div>

### Parameters

| Name | Type | Description | Notes |
|----|----|----|----|
| **delivery_id** | **str** |  |  |
| **id** | **int** | A unique integer value identifying this webhook. |  |

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

| Status code | Description      | Response headers |
|-------------|------------------|------------------|
| **200**     | No response body | \-               |

## **create_ping**

> create_ping( id, \*\*kwargs )

Send a ping webhook

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
    id = 1 # int | A unique integer value identifying this webhook.

    try:
        (data, response) = api_client.webhooks_api.create_ping(
            id,)
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling WebhooksApi.create_ping(): %s\n" % e)
```

</div>

### Parameters

| Name   | Type    | Description                                      | Notes |
|--------|---------|--------------------------------------------------|-------|
| **id** | **int** | A unique integer value identifying this webhook. |       |

There are also optional kwargs that control the function invocation
behavior. [Read more
here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type: `Tuple[WebhookDeliveryRead, urllib3.HTTPResponse]`.

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

## **destroy**

> destroy( id, \*\*kwargs )

Delete a webhook

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
    id = 1 # int | A unique integer value identifying this webhook.

    try:
        api_client.webhooks_api.destroy(
            id,)
    except exceptions.ApiException as e:
        print("Exception when calling WebhooksApi.destroy(): %s\n" % e)
```

</div>

### Parameters

| Name   | Type    | Description                                      | Notes |
|--------|---------|--------------------------------------------------|-------|
| **id** | **int** | A unique integer value identifying this webhook. |       |

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
| **204**     | The webhook has been deleted | \-               |

## **list**

> list( x_organization=None, filter=None, org=None, org_id=None,
> owner=None, page=None, page_size=None, project_id=None, search=None,
> sort=None, target_url=None, type=None, \*\*kwargs )

List webhooks

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
    filter = "filter_example" # str |  JSON Logic filter. This filter can be used to perform complex filtering by grouping rules.  For example, using such a filter you can get all resources created by you:      - {\"and\":[{\"==\":[{\"var\":\"owner\"},\"<user>\"]}]}  Details about the syntax used can be found at the link: https://jsonlogic.com/   Available filter_fields: ['target_url', 'owner', 'type', 'description', 'id', 'project_id', 'updated_date']. (optional)
    org = "org_example" # str | Organization unique slug (optional)
    org_id = 1 # int | Organization identifier (optional)
    owner = "owner_example" # str | A simple equality filter for the owner field (optional)
    page = 1 # int | A page number within the paginated result set. (optional)
    page_size = 1 # int | Number of results to return per page. (optional)
    project_id = 1 # int | A simple equality filter for the project_id field (optional)
    search = "search_example" # str | A search term. Available search_fields: ('target_url', 'owner', 'type', 'description') (optional)
    sort = "sort_example" # str | Which field to use when ordering the results. Available ordering_fields: ['target_url', 'owner', 'type', 'description', 'id', 'project_id', 'updated_date'] (optional)
    target_url = "target_url_example" # str | A simple equality filter for the target_url field (optional)
    type = "organization" # str | A simple equality filter for the type field (optional)

    try:
        (data, response) = api_client.webhooks_api.list(
            x_organization=x_organization,
            filter=filter,
            org=org,
            org_id=org_id,
            owner=owner,
            page=page,
            page_size=page_size,
            project_id=project_id,
            search=search,
            sort=sort,
            target_url=target_url,
            type=type,
        )
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling WebhooksApi.list(): %s\n" % e)
```

</div>

### Parameters

| Name | Type | Description | Notes |
|----|----|----|----|
| **x_organization** | **str** | Organization unique slug | \[optional\] |
| **filter** | **str** | JSON Logic filter. This filter can be used to perform complex filtering by grouping rules. For example, using such a filter you can get all resources created by you: - {"and":\[{"==":\[{"var":"owner"},""\]}\]} Details about the syntax used can be found at the link: <https://jsonlogic.com/> Available filter_fields: \[’target_url’, ‘owner’, ’type’, ‘description’, ‘id’, ‘project_id’, ‘updated_date’\]. | \[optional\] |
| **org** | **str** | Organization unique slug | \[optional\] |
| **org_id** | **int** | Organization identifier | \[optional\] |
| **owner** | **str** | A simple equality filter for the owner field | \[optional\] |
| **page** | **int** | A page number within the paginated result set. | \[optional\] |
| **page_size** | **int** | Number of results to return per page. | \[optional\] |
| **project_id** | **int** | A simple equality filter for the project_id field | \[optional\] |
| **search** | **str** | A search term. Available search_fields: (’target_url’, ‘owner’, ’type’, ‘description’) | \[optional\] |
| **sort** | **str** | Which field to use when ordering the results. Available ordering_fields: \[’target_url’, ‘owner’, ’type’, ‘description’, ‘id’, ‘project_id’, ‘updated_date’\] | \[optional\] |
| **target_url** | **str** | A simple equality filter for the target_url field | \[optional\] |
| **type** | **str** | A simple equality filter for the type field | \[optional\] |

There are also optional kwargs that control the function invocation
behavior. [Read more
here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type: `Tuple[PaginatedWebhookReadList, urllib3.HTTPResponse]`.

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

## **list_deliveries**

> list_deliveries( id, page=None, page_size=None, \*\*kwargs )

List deliveries for a webhook

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
    id = 1 # int | A unique integer value identifying this webhook.
    page = 1 # int | A page number within the paginated result set. (optional)
    page_size = 1 # int | Number of results to return per page. (optional)

    try:
        (data, response) = api_client.webhooks_api.list_deliveries(
            id,
            page=page,
            page_size=page_size,
        )
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling WebhooksApi.list_deliveries(): %s\n" % e)
```

</div>

### Parameters

| Name | Type | Description | Notes |
|----|----|----|----|
| **id** | **int** | A unique integer value identifying this webhook. |  |
| **page** | **int** | A page number within the paginated result set. | \[optional\] |
| **page_size** | **int** | Number of results to return per page. | \[optional\] |

There are also optional kwargs that control the function invocation
behavior. [Read more
here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type:
`Tuple[PaginatedWebhookDeliveryReadList, urllib3.HTTPResponse]`.

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

> partial_update( id, patched_webhook_write_request=None, \*\*kwargs )

Update a webhook

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
    id = 1 # int | A unique integer value identifying this webhook.
    patched_webhook_write_request = PatchedWebhookWriteRequest(
        target_url="target_url_example",
        description="description_example",
        content_type=WebhookContentType("application/json"),
        secret="secret_example",
        is_active=True,
        enable_ssl=True,
        events=[
            EventsEnum("create:comment"),
        ],
    ) # PatchedWebhookWriteRequest |  (optional)

    try:
        (data, response) = api_client.webhooks_api.partial_update(
            id,
            patched_webhook_write_request=patched_webhook_write_request,
        )
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling WebhooksApi.partial_update(): %s\n" % e)
```

</div>

### Parameters

| Name | Type | Description | Notes |
|----|----|----|----|
| **id** | **int** | A unique integer value identifying this webhook. |  |
| **patched_webhook_write_request** | [**PatchedWebhookWriteRequest**](../../models/patched-webhook-write-request) |  | \[optional\] |

There are also optional kwargs that control the function invocation
behavior. [Read more
here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type: `Tuple[WebhookRead, urllib3.HTTPResponse]`.

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

Get webhook details

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
    id = 1 # int | A unique integer value identifying this webhook.

    try:
        (data, response) = api_client.webhooks_api.retrieve(
            id,)
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling WebhooksApi.retrieve(): %s\n" % e)
```

</div>

### Parameters

| Name   | Type    | Description                                      | Notes |
|--------|---------|--------------------------------------------------|-------|
| **id** | **int** | A unique integer value identifying this webhook. |       |

There are also optional kwargs that control the function invocation
behavior. [Read more
here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type: `Tuple[WebhookRead, urllib3.HTTPResponse]`.

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

## **retrieve_deliveries**

> retrieve_deliveries( delivery_id, id, \*\*kwargs )

Get details of a webhook delivery

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
    delivery_id = "4" # str | 
    id = 1 # int | A unique integer value identifying this webhook.

    try:
        (data, response) = api_client.webhooks_api.retrieve_deliveries(
            delivery_id,
            id,)
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling WebhooksApi.retrieve_deliveries(): %s\n" % e)
```

</div>

### Parameters

| Name | Type | Description | Notes |
|----|----|----|----|
| **delivery_id** | **str** |  |  |
| **id** | **int** | A unique integer value identifying this webhook. |  |

There are also optional kwargs that control the function invocation
behavior. [Read more
here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type: `Tuple[WebhookDeliveryRead, urllib3.HTTPResponse]`.

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

## **retrieve_events**

> retrieve_events( type=None, \*\*kwargs )

List available webhook events

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
    type = "type_example" # str | Type of webhook (optional)

    try:
        (data, response) = api_client.webhooks_api.retrieve_events(
            type=type,
        )
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling WebhooksApi.retrieve_events(): %s\n" % e)
```

</div>

### Parameters

| Name     | Type    | Description     | Notes        |
|----------|---------|-----------------|--------------|
| **type** | **str** | Type of webhook | \[optional\] |

There are also optional kwargs that control the function invocation
behavior. [Read more
here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type: `Tuple[Events, urllib3.HTTPResponse]`.

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

## **update**

> update( id, webhook_write_request, \*\*kwargs )

Replace a webhook

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
    id = 1 # int | A unique integer value identifying this webhook.
    webhook_write_request = WebhookWriteRequest(
        target_url="target_url_example",
        description="description_example",
        type=WebhookType("organization"),
        content_type=WebhookContentType("application/json"),
        secret="secret_example",
        is_active=True,
        enable_ssl=True,
        project_id=1,
        events=[
            EventsEnum("create:comment"),
        ],
    ) # WebhookWriteRequest | 

    try:
        (data, response) = api_client.webhooks_api.update(
            id,
            webhook_write_request,)
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling WebhooksApi.update(): %s\n" % e)
```

</div>

### Parameters

| Name | Type | Description | Notes |
|----|----|----|----|
| **id** | **int** | A unique integer value identifying this webhook. |  |
| **webhook_write_request** | [**WebhookWriteRequest**](../../models/webhook-write-request) |  |  |

There are also optional kwargs that control the function invocation
behavior. [Read more
here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type: `Tuple[WebhookRead, urllib3.HTTPResponse]`.

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

</div>

</div>
