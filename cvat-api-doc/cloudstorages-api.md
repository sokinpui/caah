<div class="col-12 col-md-9 col-xl-8 ps-md-5" role="main">

1.  [Home](https://docs.cvat.ai/docs/)
2.  [Developers](https://docs.cvat.ai/docs/api_sdk/)
3.  [SDK](https://docs.cvat.ai/docs/api_sdk/sdk/)
4.  [API Reference](https://docs.cvat.ai/docs/api_sdk/sdk/reference/)
5.  [APIs](https://docs.cvat.ai/docs/api_sdk/sdk/reference/apis/)
6.  CloudstoragesApi

<div class="td-content">

# CloudstoragesApi class reference

<div class="article-meta">

</div>

All URIs are relative to *http://localhost*

| Method | HTTP request | Description |
|----|----|----|
| [**create**](../cloudstorages-api#create) | **POST** /api/cloudstorages | Create a cloud storage |
| [**destroy**](../cloudstorages-api#destroy) | **DELETE** /api/cloudstorages/{id} | Delete a cloud storage |
| [**list**](../cloudstorages-api#list) | **GET** /api/cloudstorages | List cloud storages |
| [**partial_update**](../cloudstorages-api#partial_update) | **PATCH** /api/cloudstorages/{id} | Update a cloud storage |
| [**retrieve**](../cloudstorages-api#retrieve) | **GET** /api/cloudstorages/{id} | Get cloud storage details |
| [**retrieve_actions**](../cloudstorages-api#retrieve_actions) | **GET** /api/cloudstorages/{id}/actions | Get allowed actions for a cloud storage |
| [**retrieve_content_v2**](../cloudstorages-api#retrieve_content_v2) | **GET** /api/cloudstorages/{id}/content-v2 | Get cloud storage content |
| [**retrieve_preview**](../cloudstorages-api#retrieve_preview) | **GET** /api/cloudstorages/{id}/preview | Get a preview image for a cloud storage |
| [**retrieve_status**](../cloudstorages-api#retrieve_status) | **GET** /api/cloudstorages/{id}/status | Get the status of a cloud storage |

## **create**

> create( cloud_storage_write_request, x_organization=None, org=None,
> org_id=None, \*\*kwargs )

Create a cloud storage

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
    cloud_storage_write_request = CloudStorageWriteRequest(
        provider_type=ProviderTypeEnum("AWS_S3_BUCKET"),
        resource="resource_example",
        display_name="display_name_example",
        owner=BasicUserRequest(
            username="A",
            first_name="first_name_example",
            last_name="last_name_example",
        ),
        credentials_type=CredentialsTypeEnum("KEY_SECRET_KEY_PAIR"),
        session_token="session_token_example",
        account_name="account_name_example",
        key="key_example",
        secret_key="secret_key_example",
        connection_string="connection_string_example",
        key_file=open('/path/to/file', 'rb'),
        specific_attributes="specific_attributes_example",
        description="description_example",
        manifests=[],
    ) # CloudStorageWriteRequest | 
    x_organization = "X-Organization_example" # str | Organization unique slug (optional)
    org = "org_example" # str | Organization unique slug (optional)
    org_id = 1 # int | Organization identifier (optional)

    try:
        (data, response) = api_client.cloudstorages_api.create(
            cloud_storage_write_request,
            x_organization=x_organization,
            org=org,
            org_id=org_id,
        )
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling CloudstoragesApi.create(): %s\n" % e)
```

</div>

### Parameters

| Name | Type | Description | Notes |
|----|----|----|----|
| **cloud_storage_write_request** | [**CloudStorageWriteRequest**](../../models/cloud-storage-write-request) |  |  |
| **x_organization** | **str** | Organization unique slug | \[optional\] |
| **org** | **str** | Organization unique slug | \[optional\] |
| **org_id** | **int** | Organization identifier | \[optional\] |

There are also optional kwargs that control the function invocation
behavior. [Read more
here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type: `Tuple[CloudStorageRead, urllib3.HTTPResponse]`.

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

- **Content-Type**: application/json, multipart/form-data
- **Accept**: application/vnd.cvat+json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **201**     |             | \-               |

## **destroy**

> destroy( id, \*\*kwargs )

Delete a cloud storage

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
    id = 1 # int | A unique integer value identifying this cloud storage.

    try:
        api_client.cloudstorages_api.destroy(
            id,)
    except exceptions.ApiException as e:
        print("Exception when calling CloudstoragesApi.destroy(): %s\n" % e)
```

</div>

### Parameters

| Name   | Type    | Description                                            | Notes |
|--------|---------|--------------------------------------------------------|-------|
| **id** | **int** | A unique integer value identifying this cloud storage. |       |

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
| **204**     | The cloud storage has been removed | \-               |

## **list**

> list( x_organization=None, credentials_type=None, filter=None,
> name=None, org=None, org_id=None, owner=None, page=None,
> page_size=None, provider_type=None, resource=None, search=None,
> sort=None, \*\*kwargs )

List cloud storages

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
    credentials_type = "KEY_SECRET_KEY_PAIR" # str | A simple equality filter for the credentials_type field (optional)
    filter = "filter_example" # str |  JSON Logic filter. This filter can be used to perform complex filtering by grouping rules.  For example, using such a filter you can get all resources created by you:      - {\"and\":[{\"==\":[{\"var\":\"owner\"},\"<user>\"]}]}  Details about the syntax used can be found at the link: https://jsonlogic.com/   Available filter_fields: ['provider_type', 'name', 'resource', 'credentials_type', 'owner', 'description', 'id']. (optional)
    name = "name_example" # str | A simple equality filter for the name field (optional)
    org = "org_example" # str | Organization unique slug (optional)
    org_id = 1 # int | Organization identifier (optional)
    owner = "owner_example" # str | A simple equality filter for the owner field (optional)
    page = 1 # int | A page number within the paginated result set. (optional)
    page_size = 1 # int | Number of results to return per page. (optional)
    provider_type = "AWS_S3_BUCKET" # str | A simple equality filter for the provider_type field (optional)
    resource = "resource_example" # str | A simple equality filter for the resource field (optional)
    search = "search_example" # str | A search term. Available search_fields: ('provider_type', 'name', 'resource', 'credentials_type', 'owner', 'description') (optional)
    sort = "sort_example" # str | Which field to use when ordering the results. Available ordering_fields: ['provider_type', 'name', 'resource', 'credentials_type', 'owner', 'description', 'id'] (optional)

    try:
        (data, response) = api_client.cloudstorages_api.list(
            x_organization=x_organization,
            credentials_type=credentials_type,
            filter=filter,
            name=name,
            org=org,
            org_id=org_id,
            owner=owner,
            page=page,
            page_size=page_size,
            provider_type=provider_type,
            resource=resource,
            search=search,
            sort=sort,
        )
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling CloudstoragesApi.list(): %s\n" % e)
```

</div>

### Parameters

| Name | Type | Description | Notes |
|----|----|----|----|
| **x_organization** | **str** | Organization unique slug | \[optional\] |
| **credentials_type** | **str** | A simple equality filter for the credentials_type field | \[optional\] |
| **filter** | **str** | JSON Logic filter. This filter can be used to perform complex filtering by grouping rules. For example, using such a filter you can get all resources created by you: - {"and":\[{"==":\[{"var":"owner"},""\]}\]} Details about the syntax used can be found at the link: <https://jsonlogic.com/> Available filter_fields: \[‘provider_type’, ’name’, ‘resource’, ‘credentials_type’, ‘owner’, ‘description’, ‘id’\]. | \[optional\] |
| **name** | **str** | A simple equality filter for the name field | \[optional\] |
| **org** | **str** | Organization unique slug | \[optional\] |
| **org_id** | **int** | Organization identifier | \[optional\] |
| **owner** | **str** | A simple equality filter for the owner field | \[optional\] |
| **page** | **int** | A page number within the paginated result set. | \[optional\] |
| **page_size** | **int** | Number of results to return per page. | \[optional\] |
| **provider_type** | **str** | A simple equality filter for the provider_type field | \[optional\] |
| **resource** | **str** | A simple equality filter for the resource field | \[optional\] |
| **search** | **str** | A search term. Available search_fields: (‘provider_type’, ’name’, ‘resource’, ‘credentials_type’, ‘owner’, ‘description’) | \[optional\] |
| **sort** | **str** | Which field to use when ordering the results. Available ordering_fields: \[‘provider_type’, ’name’, ‘resource’, ‘credentials_type’, ‘owner’, ‘description’, ‘id’\] | \[optional\] |

There are also optional kwargs that control the function invocation
behavior. [Read more
here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type:
`Tuple[PaginatedCloudStorageReadList, urllib3.HTTPResponse]`.

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

> partial_update( id, patched_cloud_storage_write_request=None,
> \*\*kwargs )

Update a cloud storage

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
    id = 1 # int | A unique integer value identifying this cloud storage.
    patched_cloud_storage_write_request = PatchedCloudStorageWriteRequest(
        provider_type=ProviderTypeEnum("AWS_S3_BUCKET"),
        resource="resource_example",
        display_name="display_name_example",
        owner=BasicUserRequest(
            username="A",
            first_name="first_name_example",
            last_name="last_name_example",
        ),
        credentials_type=CredentialsTypeEnum("KEY_SECRET_KEY_PAIR"),
        session_token="session_token_example",
        account_name="account_name_example",
        key="key_example",
        secret_key="secret_key_example",
        connection_string="connection_string_example",
        key_file=open('/path/to/file', 'rb'),
        specific_attributes="specific_attributes_example",
        description="description_example",
        manifests=[],
    ) # PatchedCloudStorageWriteRequest |  (optional)

    try:
        (data, response) = api_client.cloudstorages_api.partial_update(
            id,
            patched_cloud_storage_write_request=patched_cloud_storage_write_request,
        )
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling CloudstoragesApi.partial_update(): %s\n" % e)
```

</div>

### Parameters

| Name | Type | Description | Notes |
|----|----|----|----|
| **id** | **int** | A unique integer value identifying this cloud storage. |  |
| **patched_cloud_storage_write_request** | [**PatchedCloudStorageWriteRequest**](../../models/patched-cloud-storage-write-request) |  | \[optional\] |

There are also optional kwargs that control the function invocation
behavior. [Read more
here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type: `Tuple[CloudStorageRead, urllib3.HTTPResponse]`.

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

- **Content-Type**: application/json, multipart/form-data
- **Accept**: application/vnd.cvat+json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200**     |             | \-               |

## **retrieve**

> retrieve( id, \*\*kwargs )

Get cloud storage details

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
    id = 1 # int | A unique integer value identifying this cloud storage.

    try:
        (data, response) = api_client.cloudstorages_api.retrieve(
            id,)
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling CloudstoragesApi.retrieve(): %s\n" % e)
```

</div>

### Parameters

| Name   | Type    | Description                                            | Notes |
|--------|---------|--------------------------------------------------------|-------|
| **id** | **int** | A unique integer value identifying this cloud storage. |       |

There are also optional kwargs that control the function invocation
behavior. [Read more
here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type: `Tuple[CloudStorageRead, urllib3.HTTPResponse]`.

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

## **retrieve_actions**

> retrieve_actions( id, \*\*kwargs )

Get allowed actions for a cloud storage

Method return allowed actions for cloud storage. It’s required for
reading/writing

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
    id = 1 # int | A unique integer value identifying this cloud storage.

    try:
        (data, response) = api_client.cloudstorages_api.retrieve_actions(
            id,)
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling CloudstoragesApi.retrieve_actions(): %s\n" % e)
```

</div>

### Parameters

| Name   | Type    | Description                                            | Notes |
|--------|---------|--------------------------------------------------------|-------|
| **id** | **int** | A unique integer value identifying this cloud storage. |       |

There are also optional kwargs that control the function invocation
behavior. [Read more
here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type: `Tuple[str, urllib3.HTTPResponse]`.

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

| Status code | Description                | Response headers |
|-------------|----------------------------|------------------|
| **200**     | Cloud Storage actions (GET | PUT              |

## **retrieve_content_v2**

> retrieve_content_v2( id, manifest_path=None, next_token=None,
> page_size=None, prefix=None, \*\*kwargs )

Get cloud storage content

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
    id = 1 # int | A unique integer value identifying this cloud storage.
    manifest_path = "manifest_path_example" # str | Path to the manifest file in a cloud storage (optional)
    next_token = "next_token_example" # str | Used to continue listing files in the bucket (optional)
    page_size = 1 # int |  (optional)
    prefix = "prefix_example" # str | Prefix to filter data (optional)

    try:
        (data, response) = api_client.cloudstorages_api.retrieve_content_v2(
            id,
            manifest_path=manifest_path,
            next_token=next_token,
            page_size=page_size,
            prefix=prefix,
        )
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling CloudstoragesApi.retrieve_content_v2(): %s\n" % e)
```

</div>

### Parameters

| Name | Type | Description | Notes |
|----|----|----|----|
| **id** | **int** | A unique integer value identifying this cloud storage. |  |
| **manifest_path** | **str** | Path to the manifest file in a cloud storage | \[optional\] |
| **next_token** | **str** | Used to continue listing files in the bucket | \[optional\] |
| **page_size** | **int** |  | \[optional\] |
| **prefix** | **str** | Prefix to filter data | \[optional\] |

There are also optional kwargs that control the function invocation
behavior. [Read more
here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type: `Tuple[CloudStorageContent, urllib3.HTTPResponse]`.

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

| Status code | Description        | Response headers |
|-------------|--------------------|------------------|
| **200**     | A manifest content | \-               |

## **retrieve_preview**

> retrieve_preview( id, \*\*kwargs )

Get a preview image for a cloud storage

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
    id = 1 # int | A unique integer value identifying this cloud storage.

    try:
        api_client.cloudstorages_api.retrieve_preview(
            id,)
    except exceptions.ApiException as e:
        print("Exception when calling CloudstoragesApi.retrieve_preview(): %s\n" % e)
```

</div>

### Parameters

| Name   | Type    | Description                                            | Notes |
|--------|---------|--------------------------------------------------------|-------|
| **id** | **int** | A unique integer value identifying this cloud storage. |       |

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

| Status code | Description                         | Response headers |
|-------------|-------------------------------------|------------------|
| **200**     | Cloud Storage preview               | \-               |
| **400**     | Failed to get cloud storage preview | \-               |
| **404**     | Cloud Storage preview not found     | \-               |

## **retrieve_status**

> retrieve_status( id, \*\*kwargs )

Get the status of a cloud storage

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
    id = 1 # int | A unique integer value identifying this cloud storage.

    try:
        (data, response) = api_client.cloudstorages_api.retrieve_status(
            id,)
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling CloudstoragesApi.retrieve_status(): %s\n" % e)
```

</div>

### Parameters

| Name   | Type    | Description                                            | Notes |
|--------|---------|--------------------------------------------------------|-------|
| **id** | **int** | A unique integer value identifying this cloud storage. |       |

There are also optional kwargs that control the function invocation
behavior. [Read more
here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type: `Tuple[str, urllib3.HTTPResponse]`.

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

| Status code | Description          | Response headers |
|-------------|----------------------|------------------|
| **200**     | Cloud Storage Status | \-               |

</div>

</div>
