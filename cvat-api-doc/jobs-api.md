<div class="col-12 col-md-9 col-xl-8 ps-md-5" role="main">

1.  [Home](https://docs.cvat.ai/docs/)
2.  [Developers](https://docs.cvat.ai/docs/api_sdk/)
3.  [SDK](https://docs.cvat.ai/docs/api_sdk/sdk/)
4.  [API Reference](https://docs.cvat.ai/docs/api_sdk/sdk/reference/)
5.  [APIs](https://docs.cvat.ai/docs/api_sdk/sdk/reference/apis/)
6.  JobsApi

<div class="td-content">

# JobsApi class reference

<div class="article-meta">

</div>

All URIs are relative to *http://localhost*

| Method | HTTP request | Description |
|----|----|----|
| [**create**](../jobs-api#create) | **POST** /api/jobs | Create a job |
| [**create_annotations**](../jobs-api#create_annotations) | **POST** /api/jobs/{id}/annotations/ | Import annotations into a job |
| [**create_dataset_export**](../jobs-api#create_dataset_export) | **POST** /api/jobs/{id}/dataset/export | Initialize process to export resource as a dataset in a specific format |
| [**destroy**](../jobs-api#destroy) | **DELETE** /api/jobs/{id} | Delete a job |
| [**destroy_annotations**](../jobs-api#destroy_annotations) | **DELETE** /api/jobs/{id}/annotations/ | Delete job annotations |
| [**list**](../jobs-api#list) | **GET** /api/jobs | List jobs |
| [**partial_update**](../jobs-api#partial_update) | **PATCH** /api/jobs/{id} | Update a job |
| [**partial_update_annotations**](../jobs-api#partial_update_annotations) | **PATCH** /api/jobs/{id}/annotations/ | Update job annotations |
| [**partial_update_data_meta**](../jobs-api#partial_update_data_meta) | **PATCH** /api/jobs/{id}/data/meta | Update metainformation for media files in a job |
| [**partial_update_validation_layout**](../jobs-api#partial_update_validation_layout) | **PATCH** /api/jobs/{id}/validation_layout | Allows updating current validation configuration |
| [**retrieve**](../jobs-api#retrieve) | **GET** /api/jobs/{id} | Get job details |
| [**retrieve_annotations**](../jobs-api#retrieve_annotations) | **GET** /api/jobs/{id}/annotations/ | Get job annotations |
| [**retrieve_data**](../jobs-api#retrieve_data) | **GET** /api/jobs/{id}/data | Get data of a job |
| [**retrieve_data_meta**](../jobs-api#retrieve_data_meta) | **GET** /api/jobs/{id}/data/meta | Get metainformation for media files in a job |
| [**retrieve_preview**](../jobs-api#retrieve_preview) | **GET** /api/jobs/{id}/preview | Get a preview image for a job |
| [**retrieve_validation_layout**](../jobs-api#retrieve_validation_layout) | **GET** /api/jobs/{id}/validation_layout | Allows getting current validation configuration |
| [**update_annotations**](../jobs-api#update_annotations) | **PUT** /api/jobs/{id}/annotations/ | Replace job annotations |

## **create**

> create( job_write_request, \*\*kwargs )

Create a job

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
    job_write_request = JobWriteRequest(
        assignee=1,
        stage=JobStage("annotation"),
        state=OperationStatus("new"),
        type=JobType("annotation"),
        task_id=1,
        frame_selection_method=FrameSelectionMethod("random_uniform"),
        frame_count=1,
        frame_share=3.14,
        frames_per_job_count=1,
        frames_per_job_share=3.14,
        random_seed=0,
        frames=[
            0,
        ],
    ) # JobWriteRequest | 

    try:
        (data, response) = api_client.jobs_api.create(
            job_write_request,)
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling JobsApi.create(): %s\n" % e)
```

</div>

### Parameters

| Name | Type | Description | Notes |
|----|----|----|----|
| **job_write_request** | [**JobWriteRequest**](../../models/job-write-request) |  |  |

There are also optional kwargs that control the function invocation
behavior. [Read more
here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type: `Tuple[JobRead, urllib3.HTTPResponse]`.

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

## **create_annotations**

> create_annotations( id, cloud_storage_id=None, filename=None,
> format=None, location=None, use_default_location=None,
> annotation_file_request=None, \*\*kwargs )

Import annotations into a job

The request POST /api/jobs/id/annotations initiates a background process
to import annotations into a job. Please, use the GET
/api/requests/\<rq_id\> endpoint for checking status of the process. The
`rq_id` parameter can be found in the response on initiating request.

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
    id = 1 # int | A unique integer value identifying this job.
    cloud_storage_id = 1 # int | Storage id (optional)
    filename = "filename_example" # str | Annotation file name (optional)
    format = "format_example" # str | Input format name You can get the list of supported formats at: /server/annotation/formats (optional)
    location = "cloud_storage" # str | where to import the annotation from (optional)
    use_default_location = True # bool | Use the location that was configured in the task to import annotation (optional) if omitted the server will use the default value of True
    annotation_file_request = AnnotationFileRequest(
        annotation_file=open('/path/to/file', 'rb'),
    ) # AnnotationFileRequest |  (optional)

    try:
        api_client.jobs_api.create_annotations(
            id,
            cloud_storage_id=cloud_storage_id,
            filename=filename,
            format=format,
            location=location,
            use_default_location=use_default_location,
            annotation_file_request=annotation_file_request,
        )
    except exceptions.ApiException as e:
        print("Exception when calling JobsApi.create_annotations(): %s\n" % e)
```

</div>

### Parameters

| Name | Type | Description | Notes |
|----|----|----|----|
| **id** | **int** | A unique integer value identifying this job. |  |
| **cloud_storage_id** | **int** | Storage id | \[optional\] |
| **filename** | **str** | Annotation file name | \[optional\] |
| **format** | **str** | Input format name You can get the list of supported formats at: /server/annotation/formats | \[optional\] |
| **location** | **str** | where to import the annotation from | \[optional\] |
| **use_default_location** | **bool** | Use the location that was configured in the task to import annotation | \[optional\] if omitted the server will use the default value of True |
| **annotation_file_request** | [**AnnotationFileRequest**](../../models/annotation-file-request) |  | \[optional\] |

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

- **Content-Type**: application/json, multipart/form-data
- **Accept**: application/vnd.cvat+json

### HTTP response details

| Status code | Description                | Response headers |
|-------------|----------------------------|------------------|
| **201**     | Uploading has finished     | \-               |
| **202**     | Uploading has been started | \-               |
| **405**     | Format is not available    | \-               |

## **create_dataset_export**

> create_dataset_export( format, id, cloud_storage_id=None,
> filename=None, location=None, save_images=None, \*\*kwargs )

Initialize process to export resource as a dataset in a specific format

The request `POST /api/<projects|tasks|jobs>/id/dataset/export` will
initialize a background process to export a dataset. To check status of
the process please, use `GET /api/requests/<rq_id>` where **rq_id** is
request ID returned in the response for this endpoint.

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
    format = "format_example" # str | Desired output format name You can get the list of supported formats at: /server/annotation/formats
    id = 1 # int | A unique integer value identifying this job.
    cloud_storage_id = 1 # int | Storage id (optional)
    filename = "filename_example" # str | Desired output file name (optional)
    location = "cloud_storage" # str | Where need to save downloaded dataset (optional)
    save_images = False # bool | Include images or not (optional) if omitted the server will use the default value of False

    try:
        (data, response) = api_client.jobs_api.create_dataset_export(
            format,
            id,
            cloud_storage_id=cloud_storage_id,
            filename=filename,
            location=location,
            save_images=save_images,
        )
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling JobsApi.create_dataset_export(): %s\n" % e)
```

</div>

### Parameters

| Name | Type | Description | Notes |
|----|----|----|----|
| **format** | **str** | Desired output format name You can get the list of supported formats at: /server/annotation/formats |  |
| **id** | **int** | A unique integer value identifying this job. |  |
| **cloud_storage_id** | **int** | Storage id | \[optional\] |
| **filename** | **str** | Desired output file name | \[optional\] |
| **location** | **str** | Where need to save downloaded dataset | \[optional\] |
| **save_images** | **bool** | Include images or not | \[optional\] if omitted the server will use the default value of False |

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

| Status code | Description                      | Response headers |
|-------------|----------------------------------|------------------|
| **202**     | Exporting has been started       | \-               |
| **405**     | Format is not available          | \-               |
| **409**     | Exporting is already in progress | \-               |

## **destroy**

> destroy( id, \*\*kwargs )

Delete a job

Related annotations will be deleted as well. Please note, that not every
job can be removed. Currently, it is only available for Ground Truth
jobs.

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
    id = 1 # int | A unique integer value identifying this job.

    try:
        api_client.jobs_api.destroy(
            id,)
    except exceptions.ApiException as e:
        print("Exception when calling JobsApi.destroy(): %s\n" % e)
```

</div>

### Parameters

| Name   | Type    | Description                                  | Notes |
|--------|---------|----------------------------------------------|-------|
| **id** | **int** | A unique integer value identifying this job. |       |

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

| Status code | Description              | Response headers |
|-------------|--------------------------|------------------|
| **204**     | The job has been deleted | \-               |

## **destroy_annotations**

> destroy_annotations( id, \*\*kwargs )

Delete job annotations

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
    id = 1 # int | A unique integer value identifying this job.

    try:
        api_client.jobs_api.destroy_annotations(
            id,)
    except exceptions.ApiException as e:
        print("Exception when calling JobsApi.destroy_annotations(): %s\n" % e)
```

</div>

### Parameters

| Name   | Type    | Description                                  | Notes |
|--------|---------|----------------------------------------------|-------|
| **id** | **int** | A unique integer value identifying this job. |       |

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

| Status code | Description                     | Response headers |
|-------------|---------------------------------|------------------|
| **204**     | The annotation has been deleted | \-               |

## **list**

> list( x_organization=None, assignee=None, dimension=None, filter=None,
> org=None, org_id=None, page=None, page_size=None, parent_job_id=None,
> project_id=None, project_name=None, search=None, sort=None,
> stage=None, state=None, task_id=None, task_name=None, type=None,
> \*\*kwargs )

List jobs

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
    assignee = "assignee_example" # str | A simple equality filter for the assignee field (optional)
    dimension = "3d" # str | A simple equality filter for the dimension field (optional)
    filter = "filter_example" # str |  JSON Logic filter. This filter can be used to perform complex filtering by grouping rules.  For example, using such a filter you can get all resources created by you:      - {\"and\":[{\"==\":[{\"var\":\"owner\"},\"<user>\"]}]}  Details about the syntax used can be found at the link: https://jsonlogic.com/   Available filter_fields: ['task_name', 'project_name', 'assignee', 'state', 'stage', 'id', 'task_id', 'project_id', 'updated_date', 'dimension', 'type', 'parent_job_id']. (optional)
    org = "org_example" # str | Organization unique slug (optional)
    org_id = 1 # int | Organization identifier (optional)
    page = 1 # int | A page number within the paginated result set. (optional)
    page_size = 1 # int | Number of results to return per page. (optional)
    parent_job_id = 1 # int | A simple equality filter for the parent_job_id field (optional)
    project_id = 1 # int | A simple equality filter for the project_id field (optional)
    project_name = "project_name_example" # str | A simple equality filter for the project_name field (optional)
    search = "search_example" # str | A search term. Available search_fields: ('task_name', 'project_name', 'assignee', 'state', 'stage') (optional)
    sort = "sort_example" # str | Which field to use when ordering the results. Available ordering_fields: ['task_name', 'project_name', 'assignee', 'state', 'stage', 'id', 'task_id', 'project_id', 'updated_date', 'dimension', 'type', 'parent_job_id'] (optional)
    stage = "annotation" # str | A simple equality filter for the stage field (optional)
    state = "new" # str | A simple equality filter for the state field (optional)
    task_id = 1 # int | A simple equality filter for the task_id field (optional)
    task_name = "task_name_example" # str | A simple equality filter for the task_name field (optional)
    type = "annotation" # str | A simple equality filter for the type field (optional)

    try:
        (data, response) = api_client.jobs_api.list(
            x_organization=x_organization,
            assignee=assignee,
            dimension=dimension,
            filter=filter,
            org=org,
            org_id=org_id,
            page=page,
            page_size=page_size,
            parent_job_id=parent_job_id,
            project_id=project_id,
            project_name=project_name,
            search=search,
            sort=sort,
            stage=stage,
            state=state,
            task_id=task_id,
            task_name=task_name,
            type=type,
        )
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling JobsApi.list(): %s\n" % e)
```

</div>

### Parameters

| Name | Type | Description | Notes |
|----|----|----|----|
| **x_organization** | **str** | Organization unique slug | \[optional\] |
| **assignee** | **str** | A simple equality filter for the assignee field | \[optional\] |
| **dimension** | **str** | A simple equality filter for the dimension field | \[optional\] |
| **filter** | **str** | JSON Logic filter. This filter can be used to perform complex filtering by grouping rules. For example, using such a filter you can get all resources created by you: - {"and":\[{"==":\[{"var":"owner"},""\]}\]} Details about the syntax used can be found at the link: <https://jsonlogic.com/> Available filter_fields: \[’task_name’, ‘project_name’, ‘assignee’, ‘state’, ‘stage’, ‘id’, ’task_id’, ‘project_id’, ‘updated_date’, ‘dimension’, ’type’, ‘parent_job_id’\]. | \[optional\] |
| **org** | **str** | Organization unique slug | \[optional\] |
| **org_id** | **int** | Organization identifier | \[optional\] |
| **page** | **int** | A page number within the paginated result set. | \[optional\] |
| **page_size** | **int** | Number of results to return per page. | \[optional\] |
| **parent_job_id** | **int** | A simple equality filter for the parent_job_id field | \[optional\] |
| **project_id** | **int** | A simple equality filter for the project_id field | \[optional\] |
| **project_name** | **str** | A simple equality filter for the project_name field | \[optional\] |
| **search** | **str** | A search term. Available search_fields: (’task_name’, ‘project_name’, ‘assignee’, ‘state’, ‘stage’) | \[optional\] |
| **sort** | **str** | Which field to use when ordering the results. Available ordering_fields: \[’task_name’, ‘project_name’, ‘assignee’, ‘state’, ‘stage’, ‘id’, ’task_id’, ‘project_id’, ‘updated_date’, ‘dimension’, ’type’, ‘parent_job_id’\] | \[optional\] |
| **stage** | **str** | A simple equality filter for the stage field | \[optional\] |
| **state** | **str** | A simple equality filter for the state field | \[optional\] |
| **task_id** | **int** | A simple equality filter for the task_id field | \[optional\] |
| **task_name** | **str** | A simple equality filter for the task_name field | \[optional\] |
| **type** | **str** | A simple equality filter for the type field | \[optional\] |

There are also optional kwargs that control the function invocation
behavior. [Read more
here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type: `Tuple[PaginatedJobReadList, urllib3.HTTPResponse]`.

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

> partial_update( id, patched_job_write_request=None, \*\*kwargs )

Update a job

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
    id = 1 # int | A unique integer value identifying this job.
    patched_job_write_request = PatchedJobWriteRequest(
        assignee=1,
        stage=JobStage("annotation"),
        state=OperationStatus("new"),
    ) # PatchedJobWriteRequest |  (optional)

    try:
        (data, response) = api_client.jobs_api.partial_update(
            id,
            patched_job_write_request=patched_job_write_request,
        )
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling JobsApi.partial_update(): %s\n" % e)
```

</div>

### Parameters

| Name | Type | Description | Notes |
|----|----|----|----|
| **id** | **int** | A unique integer value identifying this job. |  |
| **patched_job_write_request** | [**PatchedJobWriteRequest**](../../models/patched-job-write-request) |  | \[optional\] |

There are also optional kwargs that control the function invocation
behavior. [Read more
here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type: `Tuple[JobRead, urllib3.HTTPResponse]`.

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

## **partial_update_annotations**

> partial_update_annotations( action, id,
> patched_labeled_data_request=None, \*\*kwargs )

Update job annotations

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
    action = "create" # str | 
    id = 1 # int | A unique integer value identifying this job.
    patched_labeled_data_request = PatchedLabeledDataRequest(
        version=0,
        tags=[
            LabeledImageRequest(
                id=1,
                frame=0,
                label_id=0,
                group=0,
                source="manual",
                attributes=[
                    AttributeValRequest(
                        spec_id=1,
                        value="value_example",
                    ),
                ],
            ),
        ],
        shapes=[
            LabeledShapeRequest(
                type=ShapeType("rectangle"),
                occluded=False,
                outside=False,
                z_order=0,
                rotation=0.0,
                points=[
                    3.14,
                ],
                id=1,
                frame=0,
                label_id=0,
                group=0,
                source="manual",
                attributes=[
                    AttributeValRequest(
                        spec_id=1,
                        value="value_example",
                    ),
                ],
                elements=[
                    SubLabeledShapeRequest(
                        type=ShapeType("rectangle"),
                        occluded=False,
                        outside=False,
                        z_order=0,
                        rotation=0.0,
                        points=[
                            3.14,
                        ],
                        id=1,
                        frame=0,
                        label_id=0,
                        group=0,
                        source="manual",
                        attributes=[
                            AttributeValRequest(
                                spec_id=1,
                                value="value_example",
                            ),
                        ],
                    ),
                ],
            ),
        ],
        tracks=[
            LabeledTrackRequest(
                id=1,
                frame=0,
                label_id=0,
                group=0,
                source="manual",
                shapes=[
                    TrackedShapeRequest(
                        type=ShapeType("rectangle"),
                        occluded=False,
                        outside=False,
                        z_order=0,
                        rotation=0.0,
                        points=[
                            3.14,
                        ],
                        id=1,
                        frame=0,
                        attributes=[
                            AttributeValRequest(
                                spec_id=1,
                                value="value_example",
                            ),
                        ],
                    ),
                ],
                attributes=[
                    AttributeValRequest(
                        spec_id=1,
                        value="value_example",
                    ),
                ],
                elements=[
                    SubLabeledTrackRequest(
                        id=1,
                        frame=0,
                        label_id=0,
                        group=0,
                        source="manual",
                        shapes=[
                            TrackedShapeRequest(
                                type=ShapeType("rectangle"),
                                occluded=False,
                                outside=False,
                                z_order=0,
                                rotation=0.0,
                                points=[
                                    3.14,
                                ],
                                id=1,
                                frame=0,
                                attributes=[
                                    AttributeValRequest(
                                        spec_id=1,
                                        value="value_example",
                                    ),
                                ],
                            ),
                        ],
                        attributes=[
                            AttributeValRequest(
                                spec_id=1,
                                value="value_example",
                            ),
                        ],
                    ),
                ],
            ),
        ],
    ) # PatchedLabeledDataRequest |  (optional)

    try:
        api_client.jobs_api.partial_update_annotations(
            action,
            id,
            patched_labeled_data_request=patched_labeled_data_request,
        )
    except exceptions.ApiException as e:
        print("Exception when calling JobsApi.partial_update_annotations(): %s\n" % e)
```

</div>

### Parameters

| Name | Type | Description | Notes |
|----|----|----|----|
| **action** | **str** |  |  |
| **id** | **int** | A unique integer value identifying this job. |  |
| **patched_labeled_data_request** | [**PatchedLabeledDataRequest**](../../models/patched-labeled-data-request) |  | \[optional\] |

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

- **Content-Type**: application/json, multipart/form-data
- **Accept**: Not defined

### HTTP response details

| Status code | Description                       | Response headers |
|-------------|-----------------------------------|------------------|
| **200**     | Annotations successfully uploaded | \-               |

## **partial_update_data_meta**

> partial_update_data_meta( id,
> patched_job_data_meta_write_request=None, \*\*kwargs )

Update metainformation for media files in a job

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
    id = 1 # int | A unique integer value identifying this job.
    patched_job_data_meta_write_request = PatchedJobDataMetaWriteRequest(
        deleted_frames=[
            0,
        ],
    ) # PatchedJobDataMetaWriteRequest |  (optional)

    try:
        (data, response) = api_client.jobs_api.partial_update_data_meta(
            id,
            patched_job_data_meta_write_request=patched_job_data_meta_write_request,
        )
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling JobsApi.partial_update_data_meta(): %s\n" % e)
```

</div>

### Parameters

| Name | Type | Description | Notes |
|----|----|----|----|
| **id** | **int** | A unique integer value identifying this job. |  |
| **patched_job_data_meta_write_request** | [**PatchedJobDataMetaWriteRequest**](../../models/patched-job-data-meta-write-request) |  | \[optional\] |

There are also optional kwargs that control the function invocation
behavior. [Read more
here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type: `Tuple[DataMetaRead, urllib3.HTTPResponse]`.

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

## **partial_update_validation_layout**

> partial_update_validation_layout( id,
> patched_job_validation_layout_write_request=None, \*\*kwargs )

Allows updating current validation configuration

WARNING: this operation is not protected from race conditions. It’s up
to the user to ensure no parallel calls to this operation happen. It
affects image access, including exports with images, backups, chunk
downloading etc.

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
    id = 1 # int | A unique integer value identifying this job.
    patched_job_validation_layout_write_request = PatchedJobValidationLayoutWriteRequest(
        frame_selection_method=None,
        honeypot_real_frames=[
            0,
        ],
    ) # PatchedJobValidationLayoutWriteRequest |  (optional)

    try:
        (data, response) = api_client.jobs_api.partial_update_validation_layout(
            id,
            patched_job_validation_layout_write_request=patched_job_validation_layout_write_request,
        )
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling JobsApi.partial_update_validation_layout(): %s\n" % e)
```

</div>

### Parameters

| Name | Type | Description | Notes |
|----|----|----|----|
| **id** | **int** | A unique integer value identifying this job. |  |
| **patched_job_validation_layout_write_request** | [**PatchedJobValidationLayoutWriteRequest**](../../models/patched-job-validation-layout-write-request) |  | \[optional\] |

There are also optional kwargs that control the function invocation
behavior. [Read more
here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type: `Tuple[JobValidationLayoutRead, urllib3.HTTPResponse]`.

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

Get job details

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
    id = 1 # int | A unique integer value identifying this job.

    try:
        (data, response) = api_client.jobs_api.retrieve(
            id,)
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling JobsApi.retrieve(): %s\n" % e)
```

</div>

### Parameters

| Name   | Type    | Description                                  | Notes |
|--------|---------|----------------------------------------------|-------|
| **id** | **int** | A unique integer value identifying this job. |       |

There are also optional kwargs that control the function invocation
behavior. [Read more
here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type: `Tuple[JobRead, urllib3.HTTPResponse]`.

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

## **retrieve_annotations**

> retrieve_annotations( id, action=None, cloud_storage_id=None,
> filename=None, format=None, location=None, \*\*kwargs )

Get job annotations

Deprecation warning: Utilizing this endpoint to export job dataset in a
specific format is no longer possible. Consider using new API: -
`POST /api/jobs/<job_id>/dataset/export?save_images=True` to initiate
export process - `GET /api/requests/<rq_id>` to check process status,
where `rq_id` is request id returned on initializing request -
`GET result_url` to download a prepared file, where `result_url` can be
found in the response on checking status request

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
    id = 1 # int | A unique integer value identifying this job.
    action = "action_example" # str | This parameter is no longer supported (optional)
    cloud_storage_id = 1 # int | This parameter is no longer supported (optional)
    filename = "filename_example" # str | This parameter is no longer supported (optional)
    format = "format_example" # str | This parameter is no longer supported (optional)
    location = "cloud_storage" # str | This parameter is no longer supported (optional)

    try:
        (data, response) = api_client.jobs_api.retrieve_annotations(
            id,
            action=action,
            cloud_storage_id=cloud_storage_id,
            filename=filename,
            format=format,
            location=location,
        )
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling JobsApi.retrieve_annotations(): %s\n" % e)
```

</div>

### Parameters

| Name | Type | Description | Notes |
|----|----|----|----|
| **id** | **int** | A unique integer value identifying this job. |  |
| **action** | **str** | This parameter is no longer supported | \[optional\] |
| **cloud_storage_id** | **int** | This parameter is no longer supported | \[optional\] |
| **filename** | **str** | This parameter is no longer supported | \[optional\] |
| **format** | **str** | This parameter is no longer supported | \[optional\] |
| **location** | **str** | This parameter is no longer supported | \[optional\] |

There are also optional kwargs that control the function invocation
behavior. [Read more
here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type: `Tuple[LabeledData, urllib3.HTTPResponse]`.

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
|----|----|----|
| **200** |  | \- |
| **410** | API endpoint no longer handles dataset exporting process | \- |

## **retrieve_data**

> retrieve_data( id, type, index=None, number=None, quality=None,
> \*\*kwargs )

Get data of a job

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
    id = 1 # int | A unique integer value identifying this job.
    type = "chunk" # str | Specifies the type of the requested data
    index = 1 # int | A unique number value identifying chunk, starts from 0 for each job (optional)
    number = 1 # int | A unique number value identifying chunk or frame. The numbers are the same as for the task. Deprecated for chunks in favor of 'index' (optional)
    quality = "compressed" # str | Specifies the quality level of the requested data (optional)

    try:
        (data, response) = api_client.jobs_api.retrieve_data(
            id,
            type,
            index=index,
            number=number,
            quality=quality,
        )
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling JobsApi.retrieve_data(): %s\n" % e)
```

</div>

### Parameters

| Name | Type | Description | Notes |
|----|----|----|----|
| **id** | **int** | A unique integer value identifying this job. |  |
| **type** | **str** | Specifies the type of the requested data |  |
| **index** | **int** | A unique number value identifying chunk, starts from 0 for each job | \[optional\] |
| **number** | **int** | A unique number value identifying chunk or frame. The numbers are the same as for the task. Deprecated for chunks in favor of ‘index’ | \[optional\] |
| **quality** | **str** | Specifies the quality level of the requested data | \[optional\] |

There are also optional kwargs that control the function invocation
behavior. [Read more
here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type: `Tuple[file_type, urllib3.HTTPResponse]`.

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

| Status code | Description             | Response headers |
|-------------|-------------------------|------------------|
| **200**     | Data of a specific type | \-               |

## **retrieve_data_meta**

> retrieve_data_meta( id, \*\*kwargs )

Get metainformation for media files in a job

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
    id = 1 # int | A unique integer value identifying this job.

    try:
        (data, response) = api_client.jobs_api.retrieve_data_meta(
            id,)
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling JobsApi.retrieve_data_meta(): %s\n" % e)
```

</div>

### Parameters

| Name   | Type    | Description                                  | Notes |
|--------|---------|----------------------------------------------|-------|
| **id** | **int** | A unique integer value identifying this job. |       |

There are also optional kwargs that control the function invocation
behavior. [Read more
here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type: `Tuple[DataMetaRead, urllib3.HTTPResponse]`.

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

## **retrieve_preview**

> retrieve_preview( id, \*\*kwargs )

Get a preview image for a job

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
    id = 1 # int | A unique integer value identifying this job.

    try:
        api_client.jobs_api.retrieve_preview(
            id,)
    except exceptions.ApiException as e:
        print("Exception when calling JobsApi.retrieve_preview(): %s\n" % e)
```

</div>

### Parameters

| Name   | Type    | Description                                  | Notes |
|--------|---------|----------------------------------------------|-------|
| **id** | **int** | A unique integer value identifying this job. |       |

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

| Status code | Description       | Response headers |
|-------------|-------------------|------------------|
| **200**     | Job image preview | \-               |

## **retrieve_validation_layout**

> retrieve_validation_layout( id, \*\*kwargs )

Allows getting current validation configuration

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
    id = 1 # int | A unique integer value identifying this job.

    try:
        (data, response) = api_client.jobs_api.retrieve_validation_layout(
            id,)
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling JobsApi.retrieve_validation_layout(): %s\n" % e)
```

</div>

### Parameters

| Name   | Type    | Description                                  | Notes |
|--------|---------|----------------------------------------------|-------|
| **id** | **int** | A unique integer value identifying this job. |       |

There are also optional kwargs that control the function invocation
behavior. [Read more
here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type: `Tuple[JobValidationLayoutRead, urllib3.HTTPResponse]`.

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

## **update_annotations**

> update_annotations( id, labeled_data_request=None, \*\*kwargs )

Replace job annotations

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
    id = 1 # int | A unique integer value identifying this job.
    labeled_data_request = LabeledDataRequest(
        version=0,
        tags=[
            LabeledImageRequest(
                id=1,
                frame=0,
                label_id=0,
                group=0,
                source="manual",
                attributes=[
                    AttributeValRequest(
                        spec_id=1,
                        value="value_example",
                    ),
                ],
            ),
        ],
        shapes=[
            LabeledShapeRequest(
                type=ShapeType("rectangle"),
                occluded=False,
                outside=False,
                z_order=0,
                rotation=0.0,
                points=[
                    3.14,
                ],
                id=1,
                frame=0,
                label_id=0,
                group=0,
                source="manual",
                attributes=[
                    AttributeValRequest(
                        spec_id=1,
                        value="value_example",
                    ),
                ],
                elements=[
                    SubLabeledShapeRequest(
                        type=ShapeType("rectangle"),
                        occluded=False,
                        outside=False,
                        z_order=0,
                        rotation=0.0,
                        points=[
                            3.14,
                        ],
                        id=1,
                        frame=0,
                        label_id=0,
                        group=0,
                        source="manual",
                        attributes=[
                            AttributeValRequest(
                                spec_id=1,
                                value="value_example",
                            ),
                        ],
                    ),
                ],
            ),
        ],
        tracks=[
            LabeledTrackRequest(
                id=1,
                frame=0,
                label_id=0,
                group=0,
                source="manual",
                shapes=[
                    TrackedShapeRequest(
                        type=ShapeType("rectangle"),
                        occluded=False,
                        outside=False,
                        z_order=0,
                        rotation=0.0,
                        points=[
                            3.14,
                        ],
                        id=1,
                        frame=0,
                        attributes=[
                            AttributeValRequest(
                                spec_id=1,
                                value="value_example",
                            ),
                        ],
                    ),
                ],
                attributes=[
                    AttributeValRequest(
                        spec_id=1,
                        value="value_example",
                    ),
                ],
                elements=[
                    SubLabeledTrackRequest(
                        id=1,
                        frame=0,
                        label_id=0,
                        group=0,
                        source="manual",
                        shapes=[
                            TrackedShapeRequest(
                                type=ShapeType("rectangle"),
                                occluded=False,
                                outside=False,
                                z_order=0,
                                rotation=0.0,
                                points=[
                                    3.14,
                                ],
                                id=1,
                                frame=0,
                                attributes=[
                                    AttributeValRequest(
                                        spec_id=1,
                                        value="value_example",
                                    ),
                                ],
                            ),
                        ],
                        attributes=[
                            AttributeValRequest(
                                spec_id=1,
                                value="value_example",
                            ),
                        ],
                    ),
                ],
            ),
        ],
    ) # LabeledDataRequest |  (optional)

    try:
        api_client.jobs_api.update_annotations(
            id,
            labeled_data_request=labeled_data_request,
        )
    except exceptions.ApiException as e:
        print("Exception when calling JobsApi.update_annotations(): %s\n" % e)
```

</div>

### Parameters

| Name | Type | Description | Notes |
|----|----|----|----|
| **id** | **int** | A unique integer value identifying this job. |  |
| **labeled_data_request** | [**LabeledDataRequest**](../../models/labeled-data-request) |  | \[optional\] |

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

- **Content-Type**: application/json, multipart/form-data
- **Accept**: Not defined

### HTTP response details

| Status code | Description                    | Response headers |
|-------------|--------------------------------|------------------|
| **200**     | Annotations have been replaced | \-               |

</div>

</div>
