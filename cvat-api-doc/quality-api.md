<div class="col-12 col-md-9 col-xl-8 ps-md-5" role="main">

1.  [Home](https://docs.cvat.ai/docs/)
2.  [Developers](https://docs.cvat.ai/docs/api_sdk/)
3.  [SDK](https://docs.cvat.ai/docs/api_sdk/sdk/)
4.  [API Reference](https://docs.cvat.ai/docs/api_sdk/sdk/reference/)
5.  [APIs](https://docs.cvat.ai/docs/api_sdk/sdk/reference/apis/)
6.  QualityApi

<div class="td-content">

# QualityApi class reference

<div class="article-meta">

</div>

All URIs are relative to *http://localhost*

| Method | HTTP request | Description |
|----|----|----|
| [**create_report**](../quality-api#create_report) | **POST** /api/quality/reports | Create a quality report |
| [**list_conflicts**](../quality-api#list_conflicts) | **GET** /api/quality/conflicts | List annotation conflicts in a quality report |
| [**list_reports**](../quality-api#list_reports) | **GET** /api/quality/reports | Method returns a paginated list of quality reports. |
| [**list_settings**](../quality-api#list_settings) | **GET** /api/quality/settings | List quality settings instances |
| [**partial_update_settings**](../quality-api#partial_update_settings) | **PATCH** /api/quality/settings/{id} | Update a quality settings instance |
| [**retrieve_report**](../quality-api#retrieve_report) | **GET** /api/quality/reports/{id} | Get quality report details |
| [**retrieve_report_data**](../quality-api#retrieve_report_data) | **GET** /api/quality/reports/{id}/data | Get quality report contents |
| [**retrieve_settings**](../quality-api#retrieve_settings) | **GET** /api/quality/settings/{id} | Get quality settings instance details |

## **create_report**

> create_report( rq_id=None, quality_report_create_request=None,
> \*\*kwargs )

Create a quality report

Deprecation warning: Utilizing this endpoint to check the computation
status is no longer possible. Consider using common requests API: GET
/api/requests/\<rq_id\>

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
    rq_id = "rq_id_example" # str | The report creation request id. Can be specified to check the report creation status.  (optional)
    quality_report_create_request = QualityReportCreateRequest(
        task_id=1,
        project_id=1,
    ) # QualityReportCreateRequest |  (optional)

    try:
        (data, response) = api_client.quality_api.create_report(
            rq_id=rq_id,
            quality_report_create_request=quality_report_create_request,
        )
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling QualityApi.create_report(): %s\n" % e)
```

</div>

### Parameters

| Name | Type | Description | Notes |
|----|----|----|----|
| **rq_id** | **str** | The report creation request id. Can be specified to check the report creation status. | \[optional\] |
| **quality_report_create_request** | [**QualityReportCreateRequest**](../../models/quality-report-create-request) |  | \[optional\] |

There are also optional kwargs that control the function invocation
behavior. [Read more
here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type: `Tuple[QualityReport, urllib3.HTTPResponse]`.

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
| **201** |  | \- |
| **202** | A quality report request has been enqueued, the request id is returned. The request status can be checked at this endpoint by passing the rq_id as the query parameter. If the request id is specified, this response means the quality report request is queued or is being processed. | \- |
| **400** | Invalid or failed request, check the response data for details | \- |

## **list_conflicts**

> list_conflicts( x_organization=None, filter=None, frame=None,
> job_id=None, org=None, org_id=None, page=None, page_size=None,
> project_id=None, report_id=None, severity=None, sort=None,
> task_id=None, type=None, \*\*kwargs )

List annotation conflicts in a quality report

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
    filter = "filter_example" # str |  JSON Logic filter. This filter can be used to perform complex filtering by grouping rules.  For example, using such a filter you can get all resources created by you:      - {\"and\":[{\"==\":[{\"var\":\"owner\"},\"<user>\"]}]}  Details about the syntax used can be found at the link: https://jsonlogic.com/   Available filter_fields: ['id', 'frame', 'type', 'job_id', 'task_id', 'project_id', 'severity']. (optional)
    frame = 1 # int | A simple equality filter for the frame field (optional)
    job_id = 1 # int | A simple equality filter for the job_id field (optional)
    org = "org_example" # str | Organization unique slug (optional)
    org_id = 1 # int | Organization identifier (optional)
    page = 1 # int | A page number within the paginated result set. (optional)
    page_size = 1 # int | Number of results to return per page. (optional)
    project_id = 1 # int | A simple equality filter for the project_id field (optional)
    report_id = 1 # int | A simple equality filter for report id (optional)
    severity = "warning" # str | A simple equality filter for the severity field (optional)
    sort = "sort_example" # str | Which field to use when ordering the results. Available ordering_fields: ['id', 'frame', 'type', 'job_id', 'task_id', 'project_id', 'severity'] (optional)
    task_id = 1 # int | A simple equality filter for the task_id field (optional)
    type = "missing_annotation" # str | A simple equality filter for the type field (optional)

    try:
        (data, response) = api_client.quality_api.list_conflicts(
            x_organization=x_organization,
            filter=filter,
            frame=frame,
            job_id=job_id,
            org=org,
            org_id=org_id,
            page=page,
            page_size=page_size,
            project_id=project_id,
            report_id=report_id,
            severity=severity,
            sort=sort,
            task_id=task_id,
            type=type,
        )
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling QualityApi.list_conflicts(): %s\n" % e)
```

</div>

### Parameters

| Name | Type | Description | Notes |
|----|----|----|----|
| **x_organization** | **str** | Organization unique slug | \[optional\] |
| **filter** | **str** | JSON Logic filter. This filter can be used to perform complex filtering by grouping rules. For example, using such a filter you can get all resources created by you: - {"and":\[{"==":\[{"var":"owner"},""\]}\]} Details about the syntax used can be found at the link: <https://jsonlogic.com/> Available filter_fields: \[‘id’, ‘frame’, ’type’, ‘job_id’, ’task_id’, ‘project_id’, ‘severity’\]. | \[optional\] |
| **frame** | **int** | A simple equality filter for the frame field | \[optional\] |
| **job_id** | **int** | A simple equality filter for the job_id field | \[optional\] |
| **org** | **str** | Organization unique slug | \[optional\] |
| **org_id** | **int** | Organization identifier | \[optional\] |
| **page** | **int** | A page number within the paginated result set. | \[optional\] |
| **page_size** | **int** | Number of results to return per page. | \[optional\] |
| **project_id** | **int** | A simple equality filter for the project_id field | \[optional\] |
| **report_id** | **int** | A simple equality filter for report id | \[optional\] |
| **severity** | **str** | A simple equality filter for the severity field | \[optional\] |
| **sort** | **str** | Which field to use when ordering the results. Available ordering_fields: \[‘id’, ‘frame’, ’type’, ‘job_id’, ’task_id’, ‘project_id’, ‘severity’\] | \[optional\] |
| **task_id** | **int** | A simple equality filter for the task_id field | \[optional\] |
| **type** | **str** | A simple equality filter for the type field | \[optional\] |

There are also optional kwargs that control the function invocation
behavior. [Read more
here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type:
`Tuple[PaginatedAnnotationConflictList, urllib3.HTTPResponse]`.

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

## **list_reports**

> list_reports( x_organization=None, filter=None, job_id=None, org=None,
> org_id=None, page=None, page_size=None, parent_id=None,
> project_id=None, sort=None, target=None, task_id=None, \*\*kwargs )

Method returns a paginated list of quality reports.

Please note that children reports are included by default if the
"task_id", "project_id" filters are used. If you want to restrict the
list of results to a specific report type, use the "target" parameter.
The "parent_id" filter includes all the nested reports recursively. For
instance, if the "parent_id" is a project report, all the related task
and job reports will be returned. Please note that a report can be
reused in several parent reports, but the "parent_id" field in responses
will include only the first parent report id. The "parent_id" filter
still returns all the relevant nested reports, even though the response
"parent_id" values may be different from the requested one.

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
    filter = "filter_example" # str |  JSON Logic filter. This filter can be used to perform complex filtering by grouping rules.  For example, using such a filter you can get all resources created by you:      - {\"and\":[{\"==\":[{\"var\":\"owner\"},\"<user>\"]}]}  Details about the syntax used can be found at the link: https://jsonlogic.com/   Available filter_fields: ['id', 'job_id', 'task_id', 'project_id', 'created_date', 'gt_last_updated', 'target_last_updated']. (optional)
    job_id = 1 # int | A simple equality filter for the job_id field (optional)
    org = "org_example" # str | Organization unique slug (optional)
    org_id = 1 # int | Organization identifier (optional)
    page = 1 # int | A page number within the paginated result set. (optional)
    page_size = 1 # int | Number of results to return per page. (optional)
    parent_id = 1 # int | A simple equality filter for parent id (optional)
    project_id = 1 # int | A simple equality filter for project id (optional)
    sort = "sort_example" # str | Which field to use when ordering the results. Available ordering_fields: ['id', 'job_id', 'task_id', 'project_id', 'created_date', 'gt_last_updated', 'target_last_updated'] (optional)
    target = "job" # str | A simple equality filter for target (optional)
    task_id = 1 # int | A simple equality filter for task id (optional)

    try:
        (data, response) = api_client.quality_api.list_reports(
            x_organization=x_organization,
            filter=filter,
            job_id=job_id,
            org=org,
            org_id=org_id,
            page=page,
            page_size=page_size,
            parent_id=parent_id,
            project_id=project_id,
            sort=sort,
            target=target,
            task_id=task_id,
        )
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling QualityApi.list_reports(): %s\n" % e)
```

</div>

### Parameters

| Name | Type | Description | Notes |
|----|----|----|----|
| **x_organization** | **str** | Organization unique slug | \[optional\] |
| **filter** | **str** | JSON Logic filter. This filter can be used to perform complex filtering by grouping rules. For example, using such a filter you can get all resources created by you: - {"and":\[{"==":\[{"var":"owner"},""\]}\]} Details about the syntax used can be found at the link: <https://jsonlogic.com/> Available filter_fields: \[‘id’, ‘job_id’, ’task_id’, ‘project_id’, ‘created_date’, ‘gt_last_updated’, ’target_last_updated’\]. | \[optional\] |
| **job_id** | **int** | A simple equality filter for the job_id field | \[optional\] |
| **org** | **str** | Organization unique slug | \[optional\] |
| **org_id** | **int** | Organization identifier | \[optional\] |
| **page** | **int** | A page number within the paginated result set. | \[optional\] |
| **page_size** | **int** | Number of results to return per page. | \[optional\] |
| **parent_id** | **int** | A simple equality filter for parent id | \[optional\] |
| **project_id** | **int** | A simple equality filter for project id | \[optional\] |
| **sort** | **str** | Which field to use when ordering the results. Available ordering_fields: \[‘id’, ‘job_id’, ’task_id’, ‘project_id’, ‘created_date’, ‘gt_last_updated’, ’target_last_updated’\] | \[optional\] |
| **target** | **str** | A simple equality filter for target | \[optional\] |
| **task_id** | **int** | A simple equality filter for task id | \[optional\] |

There are also optional kwargs that control the function invocation
behavior. [Read more
here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type:
`Tuple[PaginatedQualityReportList, urllib3.HTTPResponse]`.

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

## **list_settings**

> list_settings( x_organization=None, filter=None, inherit=None,
> org=None, org_id=None, page=None, page_size=None, parent_type=None,
> project_id=None, sort=None, task_id=None, \*\*kwargs )

List quality settings instances

Please note that child task settings are included by default if the
"project_id" filter is used. If you want to restrict results only to a
specific parent type, use the "parent_type" parameter.

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
    filter = "filter_example" # str |  JSON Logic filter. This filter can be used to perform complex filtering by grouping rules.  For example, using such a filter you can get all resources created by you:      - {\"and\":[{\"==\":[{\"var\":\"owner\"},\"<user>\"]}]}  Details about the syntax used can be found at the link: https://jsonlogic.com/   Available filter_fields: ['id', 'task_id', 'project_id', 'inherit', 'created_date', 'updated_date']. (optional)
    inherit = True # bool | A simple equality filter for the inherit field (optional)
    org = "org_example" # str | Organization unique slug (optional)
    org_id = 1 # int | Organization identifier (optional)
    page = 1 # int | A page number within the paginated result set. (optional)
    page_size = 1 # int | Number of results to return per page. (optional)
    parent_type = "project" # str | A simple equality filter for parent instance type (optional)
    project_id = 1 # int | A simple equality filter for project id (optional)
    sort = "sort_example" # str | Which field to use when ordering the results. Available ordering_fields: ['id', 'task_id', 'project_id', 'inherit', 'created_date', 'updated_date'] (optional)
    task_id = 1 # int | A simple equality filter for the task_id field (optional)

    try:
        (data, response) = api_client.quality_api.list_settings(
            x_organization=x_organization,
            filter=filter,
            inherit=inherit,
            org=org,
            org_id=org_id,
            page=page,
            page_size=page_size,
            parent_type=parent_type,
            project_id=project_id,
            sort=sort,
            task_id=task_id,
        )
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling QualityApi.list_settings(): %s\n" % e)
```

</div>

### Parameters

| Name | Type | Description | Notes |
|----|----|----|----|
| **x_organization** | **str** | Organization unique slug | \[optional\] |
| **filter** | **str** | JSON Logic filter. This filter can be used to perform complex filtering by grouping rules. For example, using such a filter you can get all resources created by you: - {"and":\[{"==":\[{"var":"owner"},""\]}\]} Details about the syntax used can be found at the link: <https://jsonlogic.com/> Available filter_fields: \[‘id’, ’task_id’, ‘project_id’, ‘inherit’, ‘created_date’, ‘updated_date’\]. | \[optional\] |
| **inherit** | **bool** | A simple equality filter for the inherit field | \[optional\] |
| **org** | **str** | Organization unique slug | \[optional\] |
| **org_id** | **int** | Organization identifier | \[optional\] |
| **page** | **int** | A page number within the paginated result set. | \[optional\] |
| **page_size** | **int** | Number of results to return per page. | \[optional\] |
| **parent_type** | **str** | A simple equality filter for parent instance type | \[optional\] |
| **project_id** | **int** | A simple equality filter for project id | \[optional\] |
| **sort** | **str** | Which field to use when ordering the results. Available ordering_fields: \[‘id’, ’task_id’, ‘project_id’, ‘inherit’, ‘created_date’, ‘updated_date’\] | \[optional\] |
| **task_id** | **int** | A simple equality filter for the task_id field | \[optional\] |

There are also optional kwargs that control the function invocation
behavior. [Read more
here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type:
`Tuple[PaginatedQualitySettingsList, urllib3.HTTPResponse]`.

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

> partial_update_settings( id, patched_quality_settings_request=None,
> \*\*kwargs )

Update a quality settings instance

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
    id = 1 # int | An id of a quality settings instance
    patched_quality_settings_request = PatchedQualitySettingsRequest(
        job_filter="job_filter_example",
        inherit=True,
        target_metric=None,
        target_metric_threshold=0,
        max_validations_per_job=0,
        iou_threshold=0.4,
        oks_sigma=0.09,
        point_size_base=None,
        line_thickness=0.01,
        low_overlap_threshold=0.8,
        compare_line_orientation=True,
        line_orientation_threshold=0.1,
        compare_groups=True,
        group_match_threshold=0.5,
        check_covered_annotations=True,
        object_visibility_threshold=0.05,
        panoptic_comparison=True,
        compare_attributes=True,
        empty_is_annotated=False,
    ) # PatchedQualitySettingsRequest |  (optional)

    try:
        (data, response) = api_client.quality_api.partial_update_settings(
            id,
            patched_quality_settings_request=patched_quality_settings_request,
        )
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling QualityApi.partial_update_settings(): %s\n" % e)
```

</div>

### Parameters

| Name | Type | Description | Notes |
|----|----|----|----|
| **id** | **int** | An id of a quality settings instance |  |
| **patched_quality_settings_request** | [**PatchedQualitySettingsRequest**](../../models/patched-quality-settings-request) |  | \[optional\] |

There are also optional kwargs that control the function invocation
behavior. [Read more
here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type: `Tuple[QualitySettings, urllib3.HTTPResponse]`.

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

## **retrieve_report**

> retrieve_report( id, \*\*kwargs )

Get quality report details

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
    id = 1 # int | A unique integer value identifying this quality report.

    try:
        (data, response) = api_client.quality_api.retrieve_report(
            id,)
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling QualityApi.retrieve_report(): %s\n" % e)
```

</div>

### Parameters

| Name | Type | Description | Notes |
|----|----|----|----|
| **id** | **int** | A unique integer value identifying this quality report. |  |

There are also optional kwargs that control the function invocation
behavior. [Read more
here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type: `Tuple[QualityReport, urllib3.HTTPResponse]`.

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

## **retrieve_report_data**

> retrieve_report_data( id, \*\*kwargs )

Get quality report contents

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
    id = 1 # int | A unique integer value identifying this quality report.

    try:
        (data, response) = api_client.quality_api.retrieve_report_data(
            id,)
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling QualityApi.retrieve_report_data(): %s\n" % e)
```

</div>

### Parameters

| Name | Type | Description | Notes |
|----|----|----|----|
| **id** | **int** | A unique integer value identifying this quality report. |  |

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

| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200**     |             | \-               |

## **retrieve_settings**

> retrieve_settings( id, \*\*kwargs )

Get quality settings instance details

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
    id = 1 # int | An id of a quality settings instance

    try:
        (data, response) = api_client.quality_api.retrieve_settings(
            id,)
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling QualityApi.retrieve_settings(): %s\n" % e)
```

</div>

### Parameters

| Name   | Type    | Description                          | Notes |
|--------|---------|--------------------------------------|-------|
| **id** | **int** | An id of a quality settings instance |       |

There are also optional kwargs that control the function invocation
behavior. [Read more
here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type: `Tuple[QualitySettings, urllib3.HTTPResponse]`.

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
