<div class="col-12 col-md-9 col-xl-8 ps-md-5" role="main">

1.  [Home](https://docs.cvat.ai/docs/)
2.  [Developers](https://docs.cvat.ai/docs/api_sdk/)
3.  [SDK](https://docs.cvat.ai/docs/api_sdk/sdk/)
4.  [API Reference](https://docs.cvat.ai/docs/api_sdk/sdk/reference/)
5.  [APIs](https://docs.cvat.ai/docs/api_sdk/sdk/reference/apis/)
6.  SchemaApi

<div class="td-content">

# SchemaApi class reference

<div class="article-meta">

</div>

All URIs are relative to *http://localhost*

| Method                                 | HTTP request         | Description |
|----------------------------------------|----------------------|-------------|
| [**retrieve**](../schema-api#retrieve) | **GET** /api/schema/ |             |

## **retrieve**

> retrieve( lang=None, scheme=None, \*\*kwargs )

OpenApi3 schema for this API. Format can be selected via content
negotiation. - YAML: application/vnd.oai.openapi - JSON:
application/vnd.oai.openapi+json

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
    lang = "af" # str |  (optional)
    scheme = "json" # str |  (optional)

    try:
        (data, response) = api_client.schema_api.retrieve(
            lang=lang,
            scheme=scheme,
        )
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling SchemaApi.retrieve(): %s\n" % e)
```

</div>

### Parameters

| Name       | Type    | Description | Notes        |
|------------|---------|-------------|--------------|
| **lang**   | **str** |             | \[optional\] |
| **scheme** | **str** |             | \[optional\] |

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
- **Accept**: application/vnd.oai.openapi, application/yaml,
  application/vnd.oai.openapi+json, application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200**     |             | \-               |

</div>

</div>
