<div class="col-12 col-md-9 col-xl-8 ps-md-5" role="main">

1.  [Home](https://docs.cvat.ai/docs/)
2.  [Developers](https://docs.cvat.ai/docs/api_sdk/)
3.  [SDK](https://docs.cvat.ai/docs/api_sdk/sdk/)
4.  [API Reference](https://docs.cvat.ai/docs/api_sdk/sdk/reference/)
5.  [APIs](https://docs.cvat.ai/docs/api_sdk/sdk/reference/apis/)
6.  LambdaApi

<div class="td-content">

# LambdaApi class reference

<div class="article-meta">

</div>

All URIs are relative to *http://localhost*

| Method | HTTP request | Description |
|----|----|----|
| [**create_functions**](../lambda-api#create_functions) | **POST** /api/lambda/functions/{func_id} |  |
| [**create_requests**](../lambda-api#create_requests) | **POST** /api/lambda/requests | Method calls the function |
| [**delete_requests**](../lambda-api#delete_requests) | **DELETE** /api/lambda/requests/{id} | Method cancels the request |
| [**list_functions**](../lambda-api#list_functions) | **GET** /api/lambda/functions | Method returns a list of functions |
| [**list_requests**](../lambda-api#list_requests) | **GET** /api/lambda/requests | Method returns a list of requests |
| [**retrieve_functions**](../lambda-api#retrieve_functions) | **GET** /api/lambda/functions/{func_id} | Method returns the information about the function |
| [**retrieve_requests**](../lambda-api#retrieve_requests) | **GET** /api/lambda/requests/{id} | Method returns the status of the request |

## **create_functions**

> create_functions( func_id, online_function_call_request=None,
> \*\*kwargs )

Allows to execute a function for immediate computation. Intended for
short-lived executions, useful for interactive calls. When executed for
interactive annotation, the job id must be specified in the ‘job’ input
field. The task id is not required in this case, but if it is specified,
it must match the job task id.

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
    func_id = "2" # str | 
    online_function_call_request = OnlineFunctionCallRequest(
        job=1,
        task=1,
    ) # OnlineFunctionCallRequest |  (optional)

    try:
        api_client.lambda_api.create_functions(
            func_id,
            online_function_call_request=online_function_call_request,
        )
    except exceptions.ApiException as e:
        print("Exception when calling LambdaApi.create_functions(): %s\n" % e)
```

</div>

### Parameters

| Name | Type | Description | Notes |
|----|----|----|----|
| **func_id** | **str** |  |  |
| **online_function_call_request** | [**OnlineFunctionCallRequest**](../../models/online-function-call-request) |  | \[optional\] |

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

- **Content-Type**: application/json
- **Accept**: Not defined

### HTTP response details

| Status code | Description                         | Response headers |
|-------------|-------------------------------------|------------------|
| **200**     | Returns function invocation results | \-               |

## **create_requests**

> create_requests( function_call_request, x_organization=None, org=None,
> org_id=None, \*\*kwargs )

Method calls the function

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
    function_call_request = FunctionCallRequest(
        function="function_example",
        task=1,
        job=1,
        max_distance=1,
        threshold=3.14,
        cleanup=False,
        conv_mask_to_poly=True,
        conv_mask_to_poly=True,
        mapping={
            "key": LabelMappingEntryRequest(
                name="name_example",
                attributes={
                    "key": "key_example",
                },
                sublabels={
                    "key": SublabelMappingEntryRequest(
                        name="name_example",
                        attributes={
                            "key": "key_example",
                        },
                    ),
                },
            ),
        },
    ) # FunctionCallRequest | 
    x_organization = "X-Organization_example" # str | Organization unique slug (optional)
    org = "org_example" # str | Organization unique slug (optional)
    org_id = 1 # int | Organization identifier (optional)

    try:
        (data, response) = api_client.lambda_api.create_requests(
            function_call_request,
            x_organization=x_organization,
            org=org,
            org_id=org_id,
        )
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling LambdaApi.create_requests(): %s\n" % e)
```

</div>

### Parameters

| Name | Type | Description | Notes |
|----|----|----|----|
| **function_call_request** | [**FunctionCallRequest**](../../models/function-call-request) |  |  |
| **x_organization** | **str** | Organization unique slug | \[optional\] |
| **org** | **str** | Organization unique slug | \[optional\] |
| **org_id** | **int** | Organization identifier | \[optional\] |

There are also optional kwargs that control the function invocation
behavior. [Read more
here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type: `Tuple[FunctionCall, urllib3.HTTPResponse]`.

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

## **delete_requests**

> delete_requests( id, \*\*kwargs )

Method cancels the request

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
    id = "id_example" # str | Request id

    try:
        api_client.lambda_api.delete_requests(
            id,)
    except exceptions.ApiException as e:
        print("Exception when calling LambdaApi.delete_requests(): %s\n" % e)
```

</div>

### Parameters

| Name   | Type    | Description | Notes |
|--------|---------|-------------|-------|
| **id** | **str** | Request id  |       |

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
| **204**     | No response body | \-               |

## **list_functions**

> list_functions( \*\*kwargs )

Method returns a list of functions

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

    try:
        api_client.lambda_api.list_functions()
    except exceptions.ApiException as e:
        print("Exception when calling LambdaApi.list_functions(): %s\n" % e)
```

</div>

### Parameters

This endpoint does not need any parameter.

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

## **list_requests**

> list_requests( \*\*kwargs )

Method returns a list of requests

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

    try:
        (data, response) = api_client.lambda_api.list_requests()
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling LambdaApi.list_requests(): %s\n" % e)
```

</div>

### Parameters

This endpoint does not need any parameter.

There are also optional kwargs that control the function invocation
behavior. [Read more
here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type: `Tuple[list[FunctionCall], urllib3.HTTPResponse]`.

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

## **retrieve_functions**

> retrieve_functions( func_id, \*\*kwargs )

Method returns the information about the function

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
    func_id = "2" # str | 

    try:
        (data, response) = api_client.lambda_api.retrieve_functions(
            func_id,)
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling LambdaApi.retrieve_functions(): %s\n" % e)
```

</div>

### Parameters

| Name        | Type    | Description | Notes |
|-------------|---------|-------------|-------|
| **func_id** | **str** |             |       |

There are also optional kwargs that control the function invocation
behavior. [Read more
here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type:
`Tuple[dict[str, typing.Union[typing.Any, none_type]], urllib3.HTTPResponse]`.

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

| Status code | Description                    | Response headers |
|-------------|--------------------------------|------------------|
| **200**     | Information about the function | \-               |

## **retrieve_requests**

> retrieve_requests( id, \*\*kwargs )

Method returns the status of the request

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
    id = "id_example" # str | Request id

    try:
        (data, response) = api_client.lambda_api.retrieve_requests(
            id,)
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling LambdaApi.retrieve_requests(): %s\n" % e)
```

</div>

### Parameters

| Name   | Type    | Description | Notes |
|--------|---------|-------------|-------|
| **id** | **str** | Request id  |       |

There are also optional kwargs that control the function invocation
behavior. [Read more
here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type: `Tuple[FunctionCall, urllib3.HTTPResponse]`.

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
