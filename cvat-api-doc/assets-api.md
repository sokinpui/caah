<div class="col-12 col-md-9 col-xl-8 ps-md-5" role="main">

1.  [Home](https://docs.cvat.ai/docs/)
2.  [Developers](https://docs.cvat.ai/docs/api_sdk/)
3.  [SDK](https://docs.cvat.ai/docs/api_sdk/sdk/)
4.  [API Reference](https://docs.cvat.ai/docs/api_sdk/sdk/reference/)
5.  [APIs](https://docs.cvat.ai/docs/api_sdk/sdk/reference/apis/)
6.  AssetsApi

<div class="td-content">

# AssetsApi class reference

<div class="article-meta">

</div>

All URIs are relative to *http://localhost*

| Method | HTTP request | Description |
|----|----|----|
| [**create**](../assets-api#create) | **POST** /api/assets | Create an asset |
| [**destroy**](../assets-api#destroy) | **DELETE** /api/assets/{uuid} | Delete an asset |
| [**retrieve**](../assets-api#retrieve) | **GET** /api/assets/{uuid} | Get an asset |

## **create**

> create( guide_id, file, \*\*kwargs )

Create an asset

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
    guide_id = 1 # int | 
    file = open('/path/to/file', 'rb') # file_type | 

    try:
        (data, response) = api_client.assets_api.create(
            guide_id,
            file,)
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling AssetsApi.create(): %s\n" % e)
```

</div>

### Parameters

| Name         | Type          | Description | Notes |
|--------------|---------------|-------------|-------|
| **guide_id** | **int**       |             |       |
| **file**     | **file_type** |             |       |

There are also optional kwargs that control the function invocation
behavior. [Read more
here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type: `Tuple[AssetRead, urllib3.HTTPResponse]`.

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

- **Content-Type**: multipart/form-data
- **Accept**: application/vnd.cvat+json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **201**     |             | \-               |

## **destroy**

> destroy( uuid, \*\*kwargs )

Delete an asset

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
    uuid = "uuid_example" # str | A UUID string identifying this asset.

    try:
        api_client.assets_api.destroy(
            uuid,)
    except exceptions.ApiException as e:
        print("Exception when calling AssetsApi.destroy(): %s\n" % e)
```

</div>

### Parameters

| Name     | Type    | Description                           | Notes |
|----------|---------|---------------------------------------|-------|
| **uuid** | **str** | A UUID string identifying this asset. |       |

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
| **204**     | The asset has been deleted | \-               |

## **retrieve**

> retrieve( uuid, \*\*kwargs )

Get an asset

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
    uuid = "uuid_example" # str | A UUID string identifying this asset.

    try:
        api_client.assets_api.retrieve(
            uuid,)
    except exceptions.ApiException as e:
        print("Exception when calling AssetsApi.retrieve(): %s\n" % e)
```

</div>

### Parameters

| Name     | Type    | Description                           | Notes |
|----------|---------|---------------------------------------|-------|
| **uuid** | **str** | A UUID string identifying this asset. |       |

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

| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200**     | Asset file  | \-               |

</div>

</div>
