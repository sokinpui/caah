<div class="col-12 col-md-9 col-xl-8 ps-md-5" role="main">

1.  [Home](https://docs.cvat.ai/docs/)
2.  [Developers](https://docs.cvat.ai/docs/api_sdk/)
3.  [SDK](https://docs.cvat.ai/docs/api_sdk/sdk/)
4.  [API Reference](https://docs.cvat.ai/docs/api_sdk/sdk/reference/)
5.  [APIs](https://docs.cvat.ai/docs/api_sdk/sdk/reference/apis/)
6.  LabelsApi

<div class="td-content">

# LabelsApi class reference

<div class="article-meta">

</div>

All URIs are relative to *http://localhost*

| Method | HTTP request | Description |
|----|----|----|
| [**destroy**](../labels-api#destroy) | **DELETE** /api/labels/{id} | Delete a label |
| [**list**](../labels-api#list) | **GET** /api/labels | List labels |
| [**partial_update**](../labels-api#partial_update) | **PATCH** /api/labels/{id} | Update a label |
| [**retrieve**](../labels-api#retrieve) | **GET** /api/labels/{id} | Get label details |

## **destroy**

> destroy( id, \*\*kwargs )

Delete a label

To delete a sublabel, please use the PATCH method of the parent label.

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
    id = 1 # int | A unique integer value identifying this label.

    try:
        api_client.labels_api.destroy(
            id,)
    except exceptions.ApiException as e:
        print("Exception when calling LabelsApi.destroy(): %s\n" % e)
```

</div>

### Parameters

| Name   | Type    | Description                                    | Notes |
|--------|---------|------------------------------------------------|-------|
| **id** | **int** | A unique integer value identifying this label. |       |

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
| **204**     | The label has been deleted | \-               |

## **list**

> list( x_organization=None, color=None, filter=None, job_id=None,
> name=None, org=None, org_id=None, page=None, page_size=None,
> parent=None, parent_id=None, project_id=None, search=None, sort=None,
> task_id=None, type=None, \*\*kwargs )

List labels

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
    color = "color_example" # str | A simple equality filter for the color field (optional)
    filter = "filter_example" # str |  JSON Logic filter. This filter can be used to perform complex filtering by grouping rules.  For example, using such a filter you can get all resources created by you:      - {\"and\":[{\"==\":[{\"var\":\"owner\"},\"<user>\"]}]}  Details about the syntax used can be found at the link: https://jsonlogic.com/   Available filter_fields: ['name', 'parent', 'id', 'type', 'color', 'parent_id']. (optional)
    job_id = 1 # int | A simple equality filter for job id (optional)
    name = "name_example" # str | A simple equality filter for the name field (optional)
    org = "org_example" # str | Organization unique slug (optional)
    org_id = 1 # int | Organization identifier (optional)
    page = 1 # int | A page number within the paginated result set. (optional)
    page_size = 1 # int | Number of results to return per page. (optional)
    parent = "parent_example" # str | A simple equality filter for the parent field (optional)
    parent_id = 1 # int | A simple equality filter for the parent_id field (optional)
    project_id = 1 # int | A simple equality filter for project id (optional)
    search = "search_example" # str | A search term. Available search_fields: ('name', 'parent') (optional)
    sort = "sort_example" # str | Which field to use when ordering the results. Available ordering_fields: ['name', 'parent', 'id', 'type', 'color', 'parent_id'] (optional)
    task_id = 1 # int | A simple equality filter for task id (optional)
    type = "any" # str | A simple equality filter for the type field (optional)

    try:
        (data, response) = api_client.labels_api.list(
            x_organization=x_organization,
            color=color,
            filter=filter,
            job_id=job_id,
            name=name,
            org=org,
            org_id=org_id,
            page=page,
            page_size=page_size,
            parent=parent,
            parent_id=parent_id,
            project_id=project_id,
            search=search,
            sort=sort,
            task_id=task_id,
            type=type,
        )
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling LabelsApi.list(): %s\n" % e)
```

</div>

### Parameters

| Name | Type | Description | Notes |
|----|----|----|----|
| **x_organization** | **str** | Organization unique slug | \[optional\] |
| **color** | **str** | A simple equality filter for the color field | \[optional\] |
| **filter** | **str** | JSON Logic filter. This filter can be used to perform complex filtering by grouping rules. For example, using such a filter you can get all resources created by you: - {"and":\[{"==":\[{"var":"owner"},""\]}\]} Details about the syntax used can be found at the link: <https://jsonlogic.com/> Available filter_fields: \[’name’, ‘parent’, ‘id’, ’type’, ‘color’, ‘parent_id’\]. | \[optional\] |
| **job_id** | **int** | A simple equality filter for job id | \[optional\] |
| **name** | **str** | A simple equality filter for the name field | \[optional\] |
| **org** | **str** | Organization unique slug | \[optional\] |
| **org_id** | **int** | Organization identifier | \[optional\] |
| **page** | **int** | A page number within the paginated result set. | \[optional\] |
| **page_size** | **int** | Number of results to return per page. | \[optional\] |
| **parent** | **str** | A simple equality filter for the parent field | \[optional\] |
| **parent_id** | **int** | A simple equality filter for the parent_id field | \[optional\] |
| **project_id** | **int** | A simple equality filter for project id | \[optional\] |
| **search** | **str** | A search term. Available search_fields: (’name’, ‘parent’) | \[optional\] |
| **sort** | **str** | Which field to use when ordering the results. Available ordering_fields: \[’name’, ‘parent’, ‘id’, ’type’, ‘color’, ‘parent_id’\] | \[optional\] |
| **task_id** | **int** | A simple equality filter for task id | \[optional\] |
| **type** | **str** | A simple equality filter for the type field | \[optional\] |

There are also optional kwargs that control the function invocation
behavior. [Read more
here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type: `Tuple[PaginatedLabelList, urllib3.HTTPResponse]`.

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

> partial_update( id, patched_label_request=None, \*\*kwargs )

Update a label

To modify a sublabel, please use the PATCH method of the parent label.

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
    id = 1 # int | A unique integer value identifying this label.
    patched_label_request = PatchedLabelRequest(
        id=1,
        name="name_example",
        color="color_example",
        attributes=[
            AttributeRequest(
                id=1,
                name="name_example",
                mutable=True,
                input_type=InputTypeEnum("checkbox"),
                default_value="default_value_example",
                values=[
                    "values_example",
                ],
            ),
        ],
        deleted=True,
        type=None,
        svg="svg_example",
        sublabels=[
            SublabelRequest(
                id=1,
                name="name_example",
                color="color_example",
                attributes=[
                    AttributeRequest(
                        id=1,
                        name="name_example",
                        mutable=True,
                        input_type=InputTypeEnum("checkbox"),
                        default_value="default_value_example",
                        values=[
                            "values_example",
                        ],
                    ),
                ],
                type=None,
                has_parent=True,
            ),
        ],
    ) # PatchedLabelRequest |  (optional)

    try:
        (data, response) = api_client.labels_api.partial_update(
            id,
            patched_label_request=patched_label_request,
        )
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling LabelsApi.partial_update(): %s\n" % e)
```

</div>

### Parameters

| Name | Type | Description | Notes |
|----|----|----|----|
| **id** | **int** | A unique integer value identifying this label. |  |
| **patched_label_request** | [**PatchedLabelRequest**](../../models/patched-label-request) |  | \[optional\] |

There are also optional kwargs that control the function invocation
behavior. [Read more
here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type: `Tuple[Label, urllib3.HTTPResponse]`.

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

Get label details

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
    id = 1 # int | A unique integer value identifying this label.

    try:
        (data, response) = api_client.labels_api.retrieve(
            id,)
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling LabelsApi.retrieve(): %s\n" % e)
```

</div>

### Parameters

| Name   | Type    | Description                                    | Notes |
|--------|---------|------------------------------------------------|-------|
| **id** | **int** | A unique integer value identifying this label. |       |

There are also optional kwargs that control the function invocation
behavior. [Read more
here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type: `Tuple[Label, urllib3.HTTPResponse]`.

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
