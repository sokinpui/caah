All URIs are relative to _http://localhost_

| Method                                                                                                                                  | HTTP request                                | Description                                                             |
| --------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------- | ----------------------------------------------------------------------- |
| [**create**](https://docs.cvat.ai/docs/api_sdk/sdk/reference/apis/tasks-api#create)                                                     | **POST** /api/tasks                         | Create a task                                                           |
| [**create_annotations**](https://docs.cvat.ai/docs/api_sdk/sdk/reference/apis/tasks-api#create_annotations)                             | **POST** /api/tasks/{id}/annotations/       | Import annotations into a task                                          |
| [**create_backup**](https://docs.cvat.ai/docs/api_sdk/sdk/reference/apis/tasks-api#create_backup)                                       | **POST** /api/tasks/backup/                 | Recreate a task from a backup                                           |
| [**create_backup_export**](https://docs.cvat.ai/docs/api_sdk/sdk/reference/apis/tasks-api#create_backup_export)                         | **POST** /api/tasks/{id}/backup/export      | Initiate process to backup resource                                     |
| [**create_data**](https://docs.cvat.ai/docs/api_sdk/sdk/reference/apis/tasks-api#create_data)                                           | **POST** /api/tasks/{id}/data/              | Attach data to a task                                                   |
| [**create_dataset_export**](https://docs.cvat.ai/docs/api_sdk/sdk/reference/apis/tasks-api#create_dataset_export)                       | **POST** /api/tasks/{id}/dataset/export     | Initialize process to export resource as a dataset in a specific format |
| [**destroy**](https://docs.cvat.ai/docs/api_sdk/sdk/reference/apis/tasks-api#destroy)                                                   | **DELETE** /api/tasks/{id}                  | Delete a task                                                           |
| [**destroy_annotations**](https://docs.cvat.ai/docs/api_sdk/sdk/reference/apis/tasks-api#destroy_annotations)                           | **DELETE** /api/tasks/{id}/annotations/     | Delete task annotations                                                 |
| [**list**](https://docs.cvat.ai/docs/api_sdk/sdk/reference/apis/tasks-api#list)                                                         | **GET** /api/tasks                          | List tasks                                                              |
| [**partial_update**](https://docs.cvat.ai/docs/api_sdk/sdk/reference/apis/tasks-api#partial_update)                                     | **PATCH** /api/tasks/{id}                   | Update a task                                                           |
| [**partial_update_annotations**](https://docs.cvat.ai/docs/api_sdk/sdk/reference/apis/tasks-api#partial_update_annotations)             | **PATCH** /api/tasks/{id}/annotations/      | Update task annotations                                                 |
| [**partial_update_data_meta**](https://docs.cvat.ai/docs/api_sdk/sdk/reference/apis/tasks-api#partial_update_data_meta)                 | **PATCH** /api/tasks/{id}/data/meta         | Update metainformation for media files in a task                        |
| [**partial_update_validation_layout**](https://docs.cvat.ai/docs/api_sdk/sdk/reference/apis/tasks-api#partial_update_validation_layout) | **PATCH** /api/tasks/{id}/validation_layout | Allows updating current validation configuration                        |
| [**retrieve**](https://docs.cvat.ai/docs/api_sdk/sdk/reference/apis/tasks-api#retrieve)                                                 | **GET** /api/tasks/{id}                     | Get task details                                                        |
| [**retrieve_annotations**](https://docs.cvat.ai/docs/api_sdk/sdk/reference/apis/tasks-api#retrieve_annotations)                         | **GET** /api/tasks/{id}/annotations/        | Get task annotations                                                    |
| [**retrieve_data**](https://docs.cvat.ai/docs/api_sdk/sdk/reference/apis/tasks-api#retrieve_data)                                       | **GET** /api/tasks/{id}/data/               | Get data of a task                                                      |
| [**retrieve_data_meta**](https://docs.cvat.ai/docs/api_sdk/sdk/reference/apis/tasks-api#retrieve_data_meta)                             | **GET** /api/tasks/{id}/data/meta           | Get metainformation for media files in a task                           |
| [**retrieve_preview**](https://docs.cvat.ai/docs/api_sdk/sdk/reference/apis/tasks-api#retrieve_preview)                                 | **GET** /api/tasks/{id}/preview             | Get a preview image for a task                                          |
| [**retrieve_status**](https://docs.cvat.ai/docs/api_sdk/sdk/reference/apis/tasks-api#retrieve_status)                                   | **GET** /api/tasks/{id}/status              | Get the creation status of a task                                       |
| [**retrieve_validation_layout**](https://docs.cvat.ai/docs/api_sdk/sdk/reference/apis/tasks-api#retrieve_validation_layout)             | **GET** /api/tasks/{id}/validation_layout   | Allows getting current validation configuration                         |
| [**update_annotations**](https://docs.cvat.ai/docs/api_sdk/sdk/reference/apis/tasks-api#update_annotations)                             | **PUT** /api/tasks/{id}/annotations/        | Replace task annotations                                                |

## create

> create( task_write_request, x_organization=None, org=None, org_id=None, \*\*kwargs )

Create a task

The new task will not have any attached images or videos. To attach them, use the /api/tasks/ /data endpoint.

### Example

```python
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
    task_write_request = TaskWriteRequest(
        name="name_example",
        project_id=1,
        owner_id=1,
        assignee_id=1,
        bug_tracker="bug_tracker_example",
        overlap=0,
        segment_size=0,
        labels=[
            PatchedLabelRequest(
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
            ),
        ],
        subset="subset_example",
        target_storage=StorageRequest(
            location=LocationEnum("cloud_storage"),
            cloud_storage_id=1,
        ),
        source_storage=StorageRequest(
            location=LocationEnum("cloud_storage"),
            cloud_storage_id=1,
        ),
        consensus_replicas=0,
    ) # TaskWriteRequest |
    x_organization = "X-Organization_example" # str | Organization unique slug (optional)
    org = "org_example" # str | Organization unique slug (optional)
    org_id = 1 # int | Organization identifier (optional)

    try:
        (data, response) = api_client.tasks_api.create(
            task_write_request,
            x_organization=x_organization,
            org=org,
            org_id=org_id,
        )
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling TasksApi.create(): %s\n" % e)
```

### Parameters

| Name                   | Type                                                                                              | Description              | Notes        |
| ---------------------- | ------------------------------------------------------------------------------------------------- | ------------------------ | ------------ |
| **task_write_request** | [**TaskWriteRequest**](https://docs.cvat.ai/docs/api_sdk/sdk/reference/models/task-write-request) |                          |              |
| **x_organization**     | **str**                                                                                           | Organization unique slug | \[optional\] |
| **org**                | **str**                                                                                           | Organization unique slug | \[optional\] |
| **org_id**             | **int**                                                                                           | Organization identifier  | \[optional\] |

There are also optional kwargs that control the function invocation behavior.[Read more here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type: `Tuple[TaskRead, urllib3.HTTPResponse]`.

Returns a tuple with 2 values: `(parsed_response, raw_response)`.

The first value is a model parsed from the response data. The second value is the raw response, which can be useful to get response parameters, such as status code, headers, or raw response data. Read more about invocation parameters and returned values [here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Authentication

accessTokenAuth, basicAuth, csrfAuth, csrfHeaderAuth, sessionAuth, tokenAuth

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/vnd.cvat+json

### HTTP response details

| Status code | Description | Response headers |
| ----------- | ----------- | ---------------- |
| **201**     |             | \-               |

## create_annotations

> create_annotations( id, cloud_storage_id=None, filename=None, format=None, location=None, use_default_location=None, annotation_file_request=None, \*\*kwargs )

Import annotations into a task

The request POST /api/tasks/id/annotations initiates a background process to import annotations into a task. Please, use the GET /api/requests/<rq_id> endpoint for checking status of the process. The `rq_id` parameter can be found in the response on initiating request.

### Example

```python
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
    id = 1 # int | A unique integer value identifying this task.
    cloud_storage_id = 1 # int | Storage id (optional)
    filename = "filename_example" # str | Annotation file name (optional)
    format = "format_example" # str | Input format name You can get the list of supported formats at: /server/annotation/formats (optional)
    location = "cloud_storage" # str | where to import the annotation from (optional)
    use_default_location = True # bool | Use the location that was configured in task to import annotations (optional) if omitted the server will use the default value of True
    annotation_file_request = AnnotationFileRequest(
        annotation_file=open('/path/to/file', 'rb'),
    ) # AnnotationFileRequest |  (optional)

    try:
        api_client.tasks_api.create_annotations(
            id,
            cloud_storage_id=cloud_storage_id,
            filename=filename,
            format=format,
            location=location,
            use_default_location=use_default_location,
            annotation_file_request=annotation_file_request,
        )
    except exceptions.ApiException as e:
        print("Exception when calling TasksApi.create_annotations(): %s\n" % e)
```

### Parameters

| Name                        | Type                                                                                                        | Description                                                                                | Notes                                                                 |
| --------------------------- | ----------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ | --------------------------------------------------------------------- |
| **id**                      | **int**                                                                                                     | A unique integer value identifying this task.                                              |                                                                       |
| **cloud_storage_id**        | **int**                                                                                                     | Storage id                                                                                 | \[optional\]                                                          |
| **filename**                | **str**                                                                                                     | Annotation file name                                                                       | \[optional\]                                                          |
| **format**                  | **str**                                                                                                     | Input format name You can get the list of supported formats at: /server/annotation/formats | \[optional\]                                                          |
| **location**                | **str**                                                                                                     | where to import the annotation from                                                        | \[optional\]                                                          |
| **use_default_location**    | **bool**                                                                                                    | Use the location that was configured in task to import annotations                         | \[optional\] if omitted the server will use the default value of True |
| **annotation_file_request** | [**AnnotationFileRequest**](https://docs.cvat.ai/docs/api_sdk/sdk/reference/models/annotation-file-request) |                                                                                            | \[optional\]                                                          |

There are also optional kwargs that control the function invocation behavior.[Read more here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type: `Tuple[None, urllib3.HTTPResponse]`.

Returns a tuple with 2 values: `(None, raw_response)`.

This endpoint does not have any return value, so `None` is always returned as the first value. The second value is the raw response, which can be useful to get response parameters, such as status code, headers, or raw response data. Read more about invocation parameters and returned values [here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Authentication

accessTokenAuth, basicAuth, csrfAuth, csrfHeaderAuth, sessionAuth, tokenAuth

### HTTP request headers

- **Content-Type**: application/json, multipart/form-data
- **Accept**: application/vnd.cvat+json

### HTTP response details

| Status code | Description                | Response headers |
| ----------- | -------------------------- | ---------------- |
| **201**     | Uploading has finished     | \-               |
| **202**     | Uploading has been started | \-               |
| **405**     | Format is not available    | \-               |

## create_backup

> create_backup( x_organization=None, cloud_storage_id=None, filename=None, location=None, org=None, org_id=None, task_file_request=None, \*\*kwargs )

Recreate a task from a backup

The backup import process is as follows: The first request POST /api/tasks/backup creates a background job on the server in which the process of a task creating from an uploaded backup is carried out. To check the status of the import process, use GET /api/requests/rq_id, where rq_id is the request ID obtained from the response to the previous request. Once the import completes successfully, the response will contain the ID of the newly created task in the result_id field.

### Example

```python
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
    cloud_storage_id = 1 # int | Storage id (optional)
    filename = "filename_example" # str | Backup file name (optional)
    location = "local" # str | Where to import the backup file from (optional) if omitted the server will use the default value of "local"
    org = "org_example" # str | Organization unique slug (optional)
    org_id = 1 # int | Organization identifier (optional)
    task_file_request = TaskFileRequest(
        task_file=open('/path/to/file', 'rb'),
    ) # TaskFileRequest |  (optional)

    try:
        (data, response) = api_client.tasks_api.create_backup(
            x_organization=x_organization,
            cloud_storage_id=cloud_storage_id,
            filename=filename,
            location=location,
            org=org,
            org_id=org_id,
            task_file_request=task_file_request,
        )
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling TasksApi.create_backup(): %s\n" % e)
```

### Parameters

| Name                  | Type                                                                                            | Description                          | Notes                                                                    |
| --------------------- | ----------------------------------------------------------------------------------------------- | ------------------------------------ | ------------------------------------------------------------------------ |
| **x_organization**    | **str**                                                                                         | Organization unique slug             | \[optional\]                                                             |
| **cloud_storage_id**  | **int**                                                                                         | Storage id                           | \[optional\]                                                             |
| **filename**          | **str**                                                                                         | Backup file name                     | \[optional\]                                                             |
| **location**          | **str**                                                                                         | Where to import the backup file from | \[optional\] if omitted the server will use the default value of “local” |
| **org**               | **str**                                                                                         | Organization unique slug             | \[optional\]                                                             |
| **org_id**            | **int**                                                                                         | Organization identifier              | \[optional\]                                                             |
| **task_file_request** | [**TaskFileRequest**](https://docs.cvat.ai/docs/api_sdk/sdk/reference/models/task-file-request) |                                      | \[optional\]                                                             |

There are also optional kwargs that control the function invocation behavior.[Read more here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type: `Tuple[RqId, urllib3.HTTPResponse]`.

Returns a tuple with 2 values: `(parsed_response, raw_response)`.

The first value is a model parsed from the response data. The second value is the raw response, which can be useful to get response parameters, such as status code, headers, or raw response data. Read more about invocation parameters and returned values [here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Authentication

accessTokenAuth, basicAuth, csrfAuth, csrfHeaderAuth, sessionAuth, tokenAuth

### HTTP request headers

- **Content-Type**: application/json, multipart/form-data
- **Accept**: application/vnd.cvat+json

### HTTP response details

| Status code | Description                           | Response headers |
| ----------- | ------------------------------------- | ---------------- |
| **202**     | Import of the backup file has started | \-               |

## create_backup_export

> create_backup_export( id, cloud_storage_id=None, filename=None, lightweight=None, location=None, \*\*kwargs )

Initiate process to backup resource

The request `POST /api/<projects|tasks>/id/backup/export` will initialize a background process to backup a resource. To check status of the process please, use `GET /api/requests/<rq_id>` where **rq_id** is request ID returned in the response for this endpoint.

### Example

```python
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
    id = 1 # int | A unique integer value identifying this task.
    cloud_storage_id = 1 # int | Storage id (optional)
    filename = "filename_example" # str | Backup file name (optional)
    lightweight = True # bool | Makes a lightweight backup (without media files) for tasks whose media is located in cloud storage (optional) if omitted the server will use the default value of True
    location = "cloud_storage" # str | Where need to save downloaded backup (optional)

    try:
        (data, response) = api_client.tasks_api.create_backup_export(
            id,
            cloud_storage_id=cloud_storage_id,
            filename=filename,
            lightweight=lightweight,
            location=location,
        )
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling TasksApi.create_backup_export(): %s\n" % e)
```

### Parameters

| Name                 | Type     | Description                                                                                        | Notes                                                                 |
| -------------------- | -------- | -------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------- |
| **id**               | **int**  | A unique integer value identifying this task.                                                      |                                                                       |
| **cloud_storage_id** | **int**  | Storage id                                                                                         | \[optional\]                                                          |
| **filename**         | **str**  | Backup file name                                                                                   | \[optional\]                                                          |
| **lightweight**      | **bool** | Makes a lightweight backup (without media files) for tasks whose media is located in cloud storage | \[optional\] if omitted the server will use the default value of True |
| **location**         | **str**  | Where need to save downloaded backup                                                               | \[optional\]                                                          |

There are also optional kwargs that control the function invocation behavior.[Read more here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type: `Tuple[RqId, urllib3.HTTPResponse]`.

Returns a tuple with 2 values: `(parsed_response, raw_response)`.

The first value is a model parsed from the response data. The second value is the raw response, which can be useful to get response parameters, such as status code, headers, or raw response data. Read more about invocation parameters and returned values [here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Authentication

accessTokenAuth, basicAuth, csrfAuth, csrfHeaderAuth, sessionAuth, tokenAuth

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/vnd.cvat+json

### HTTP response details

| Status code | Description                                                           | Response headers |
| ----------- | --------------------------------------------------------------------- | ---------------- |
| **202**     | Creating a backup file has been started                               | \-               |
| **400**     | Wrong query parameters were passed                                    | \-               |
| **409**     | The backup process has already been initiated and is not yet finished | \-               |

## create_data

> create_data( id, upload_finish=None, upload_multiple=None, upload_start=None, data_request=None, \*\*kwargs )

Attach data to a task

Allows to upload data (images, video, etc.) to a task. Supports the TUS open file uploading protocol ([https://tus.io/)](<https://tus.io/)>). Supports the following protocols: 1. A single Data request and 2.1. An Upload-Start request 2.2.a. Regular TUS protocol requests (Upload-Length + Chunks) 2.2.b. Upload-Multiple requests 2.3. An Upload-Finish request Requests: - Data - POST, no extra headers or ‘Upload-Start’ + ‘Upload-Finish’ headers. Contains data in the body. - Upload-Start - POST, has an ‘Upload-Start’ header. No body is expected. - Upload-Length - POST, has an ‘Upload-Length’ header (see the TUS specification) - Chunk - HEAD/PATCH (see the TUS specification). Sent to /data/ endpoints. - Upload-Finish - POST, has an ‘Upload-Finish’ header. Can contain data in the body. - Upload-Multiple - POST, has an ‘Upload-Multiple’ header. Contains data in the body. The ‘Upload-Finish’ request allows to specify the uploaded files should be ordered. This may be needed if the files can be sent unordered. To state that the input files are sent ordered, pass an empty list of files in the ‘upload_file_order’ field. If the files are sent unordered, the ordered file list is expected in the ‘upload_file_order’ field. It must be a list of string file paths, relative to the dataset root. Example: files = \[ "cats/cat_1.jpg", "dogs/dog2.jpg", "image_3.png", … \] Independently of the file declaration field used (‘client_files’, ‘server_files’, etc.), when the ‘predefined’ sorting method is selected, the uploaded files will be ordered according to the ‘.jsonl’ manifest file, if it is found in the list of files. For archives (e.g. ‘.zip’), a manifest file (’\*.jsonl’) is required when using the ‘predefined’ file ordering. Such file must be provided next to the archive in the list of files. Read more about manifest files here: [https://docs.cvat.ai/docs/manual/advanced/dataset_manifest/](https://docs.cvat.ai/docs/manual/advanced/dataset_manifest/) After all data is sent, the operation status can be retrieved via the `GET /api/requests/<rq_id>`, where **rq_id** is request ID returned for this request. Once data is attached to a task, it cannot be detached or replaced.

### Example

```python
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
    id = 1 # int | A unique integer value identifying this task.
    upload_finish = True # bool | Finishes data upload. Can be combined with Upload-Start header to create task data with one request (optional)
    upload_multiple = True # bool | Indicates that data with this request are single or multiple files that should be attached to a task (optional)
    upload_start = True # bool | Initializes data upload. Optionally, can include upload metadata in the request body. (optional)
    data_request = DataRequest(
        chunk_size=0,
        image_quality=0,
        start_frame=0,
        stop_frame=0,
        frame_filter="frame_filter_example",
        client_files=[],
        server_files=[],
        remote_files=[],
        use_zip_chunks=False,
        server_files_exclude=[],
        cloud_storage_id=1,
        use_cache=False,
        copy_data=False,
        storage_method=StorageMethod("cache"),
        sorting_method=SortingMethod("lexicographical"),
        filename_pattern="filename_pattern_example",
        job_file_mapping=[
            [
                "a",
            ],
        ],
        upload_file_order=[
            "upload_file_order_example",
        ],
        validation_params=DataRequestValidationParams(None),
    ) # DataRequest |  (optional)

    try:
        (data, response) = api_client.tasks_api.create_data(
            id,
            upload_finish=upload_finish,
            upload_multiple=upload_multiple,
            upload_start=upload_start,
            data_request=data_request,
        )
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling TasksApi.create_data(): %s\n" % e)
```

### Parameters

| Name                | Type                                                                                   | Description                                                                                          | Notes        |
| ------------------- | -------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- | ------------ |
| **id**              | **int**                                                                                | A unique integer value identifying this task.                                                        |              |
| **upload_finish**   | **bool**                                                                               | Finishes data upload. Can be combined with Upload-Start header to create task data with one request  | \[optional\] |
| **upload_multiple** | **bool**                                                                               | Indicates that data with this request are single or multiple files that should be attached to a task | \[optional\] |
| **upload_start**    | **bool**                                                                               | Initializes data upload. Optionally, can include upload metadata in the request body.                | \[optional\] |
| **data_request**    | [**DataRequest**](https://docs.cvat.ai/docs/api_sdk/sdk/reference/models/data-request) |                                                                                                      | \[optional\] |

There are also optional kwargs that control the function invocation behavior.[Read more here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type: `Tuple[DataResponse, urllib3.HTTPResponse]`.

Returns a tuple with 2 values: `(parsed_response, raw_response)`.

The first value is a model parsed from the response data. The second value is the raw response, which can be useful to get response parameters, such as status code, headers, or raw response data. Read more about invocation parameters and returned values [here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Authentication

accessTokenAuth, basicAuth, csrfAuth, csrfHeaderAuth, sessionAuth, tokenAuth

### HTTP request headers

- **Content-Type**: application/json, multipart/form-data
- **Accept**: application/vnd.cvat+json

### HTTP response details

| Status code | Description                                          | Response headers |
| ----------- | ---------------------------------------------------- | ---------------- |
| **202**     | Request to attach a data to a task has been accepted | \-               |

## create_dataset_export

> create_dataset_export( format, id, cloud_storage_id=None, filename=None, location=None, save_images=None, \*\*kwargs )

Initialize process to export resource as a dataset in a specific format

The request `POST /api/<projects|tasks|jobs>/id/dataset/export` will initialize a background process to export a dataset. To check status of the process please, use `GET /api/requests/<rq_id>` where **rq_id** is request ID returned in the response for this endpoint.

### Example

```python
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
    id = 1 # int | A unique integer value identifying this task.
    cloud_storage_id = 1 # int | Storage id (optional)
    filename = "filename_example" # str | Desired output file name (optional)
    location = "cloud_storage" # str | Where need to save downloaded dataset (optional)
    save_images = False # bool | Include images or not (optional) if omitted the server will use the default value of False

    try:
        (data, response) = api_client.tasks_api.create_dataset_export(
            format,
            id,
            cloud_storage_id=cloud_storage_id,
            filename=filename,
            location=location,
            save_images=save_images,
        )
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling TasksApi.create_dataset_export(): %s\n" % e)
```

### Parameters

| Name                 | Type     | Description                                                                                         | Notes                                                                  |
| -------------------- | -------- | --------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| **format**           | **str**  | Desired output format name You can get the list of supported formats at: /server/annotation/formats |                                                                        |
| **id**               | **int**  | A unique integer value identifying this task.                                                       |                                                                        |
| **cloud_storage_id** | **int**  | Storage id                                                                                          | \[optional\]                                                           |
| **filename**         | **str**  | Desired output file name                                                                            | \[optional\]                                                           |
| **location**         | **str**  | Where need to save downloaded dataset                                                               | \[optional\]                                                           |
| **save_images**      | **bool** | Include images or not                                                                               | \[optional\] if omitted the server will use the default value of False |

There are also optional kwargs that control the function invocation behavior.[Read more here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type: `Tuple[RqId, urllib3.HTTPResponse]`.

Returns a tuple with 2 values: `(parsed_response, raw_response)`.

The first value is a model parsed from the response data. The second value is the raw response, which can be useful to get response parameters, such as status code, headers, or raw response data. Read more about invocation parameters and returned values [here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Authentication

accessTokenAuth, basicAuth, csrfAuth, csrfHeaderAuth, sessionAuth, tokenAuth

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/vnd.cvat+json

### HTTP response details

| Status code | Description                      | Response headers |
| ----------- | -------------------------------- | ---------------- |
| **202**     | Exporting has been started       | \-               |
| **405**     | Format is not available          | \-               |
| **409**     | Exporting is already in progress | \-               |

## destroy

> destroy( id, \*\*kwargs )

Delete a task

All attached jobs, annotations and data will be deleted as well.

### Example

```python
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
    id = 1 # int | A unique integer value identifying this task.

    try:
        api_client.tasks_api.destroy(
            id,)
    except exceptions.ApiException as e:
        print("Exception when calling TasksApi.destroy(): %s\n" % e)
```

### Parameters

| Name   | Type    | Description                                   | Notes |
| ------ | ------- | --------------------------------------------- | ----- |
| **id** | **int** | A unique integer value identifying this task. |       |

There are also optional kwargs that control the function invocation behavior.[Read more here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type: `Tuple[None, urllib3.HTTPResponse]`.

Returns a tuple with 2 values: `(None, raw_response)`.

This endpoint does not have any return value, so `None` is always returned as the first value. The second value is the raw response, which can be useful to get response parameters, such as status code, headers, or raw response data. Read more about invocation parameters and returned values [here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Authentication

accessTokenAuth, basicAuth, csrfAuth, csrfHeaderAuth, sessionAuth, tokenAuth

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: Not defined

### HTTP response details

| Status code | Description               | Response headers |
| ----------- | ------------------------- | ---------------- |
| **204**     | The task has been deleted | \-               |

## destroy_annotations

> destroy_annotations( id, \*\*kwargs )

Delete task annotations

### Example

```python
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
    id = 1 # int | A unique integer value identifying this task.

    try:
        api_client.tasks_api.destroy_annotations(
            id,)
    except exceptions.ApiException as e:
        print("Exception when calling TasksApi.destroy_annotations(): %s\n" % e)
```

### Parameters

| Name   | Type    | Description                                   | Notes |
| ------ | ------- | --------------------------------------------- | ----- |
| **id** | **int** | A unique integer value identifying this task. |       |

There are also optional kwargs that control the function invocation behavior.[Read more here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type: `Tuple[None, urllib3.HTTPResponse]`.

Returns a tuple with 2 values: `(None, raw_response)`.

This endpoint does not have any return value, so `None` is always returned as the first value. The second value is the raw response, which can be useful to get response parameters, such as status code, headers, or raw response data. Read more about invocation parameters and returned values [here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Authentication

accessTokenAuth, basicAuth, csrfAuth, csrfHeaderAuth, sessionAuth, tokenAuth

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: Not defined

### HTTP response details

| Status code | Description                     | Response headers |
| ----------- | ------------------------------- | ---------------- |
| **204**     | The annotation has been deleted | \-               |

## list

> list( x_organization=None, assignee=None, dimension=None, filter=None, mode=None, name=None, org=None, org_id=None, owner=None, page=None, page_size=None, project_id=None, project_name=None, search=None, sort=None, status=None, subset=None, tracker_link=None, validation_mode=None, \*\*kwargs )

List tasks

### Example

```python
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
    filter = "filter_example" # str |  JSON Logic filter. This filter can be used to perform complex filtering by grouping rules.  For example, using such a filter you can get all resources created by you:      - {\"and\":[{\"==\":[{\"var\":\"owner\"},\"<user>\"]}]}  Details about the syntax used can be found at the link: https://jsonlogic.com/   Available filter_fields: ['project_name', 'name', 'owner', 'status', 'assignee', 'subset', 'mode', 'dimension', 'tracker_link', 'validation_mode', 'id', 'project_id', 'updated_date'].  There are few examples for complex filtering tasks:      - Get all tasks from 1,2,3 projects - { \"and\" : [{ \"in\" : [{ \"var\" : \"project_id\" }, [1, 2, 3]]}]}      - Get all completed tasks from 1 project - { \"and\": [{ \"==\": [{ \"var\" : \"status\" }, \"completed\"]}, { \"==\" : [{ \"var\" : \"project_id\"}, 1]}]}   (optional)
    mode = "mode_example" # str | A simple equality filter for the mode field (optional)
    name = "name_example" # str | A simple equality filter for the name field (optional)
    org = "org_example" # str | Organization unique slug (optional)
    org_id = 1 # int | Organization identifier (optional)
    owner = "owner_example" # str | A simple equality filter for the owner field (optional)
    page = 1 # int | A page number within the paginated result set. (optional)
    page_size = 1 # int | Number of results to return per page. (optional)
    project_id = 1 # int | A simple equality filter for the project_id field (optional)
    project_name = "project_name_example" # str | A simple equality filter for the project_name field (optional)
    search = "search_example" # str | A search term. Available search_fields: ('project_name', 'name', 'owner', 'status', 'assignee', 'subset', 'mode', 'dimension', 'tracker_link', 'validation_mode') (optional)
    sort = "sort_example" # str | Which field to use when ordering the results. Available ordering_fields: ['project_name', 'name', 'owner', 'status', 'assignee', 'subset', 'mode', 'dimension', 'tracker_link', 'validation_mode', 'id', 'project_id', 'updated_date'] (optional)
    status = "annotation" # str | A simple equality filter for the status field (optional)
    subset = "subset_example" # str | A simple equality filter for the subset field (optional)
    tracker_link = "tracker_link_example" # str | A simple equality filter for the tracker_link field (optional)
    validation_mode = "gt" # str | A simple equality filter for the validation_mode field (optional)

    try:
        (data, response) = api_client.tasks_api.list(
            x_organization=x_organization,
            assignee=assignee,
            dimension=dimension,
            filter=filter,
            mode=mode,
            name=name,
            org=org,
            org_id=org_id,
            owner=owner,
            page=page,
            page_size=page_size,
            project_id=project_id,
            project_name=project_name,
            search=search,
            sort=sort,
            status=status,
            subset=subset,
            tracker_link=tracker_link,
            validation_mode=validation_mode,
        )
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling TasksApi.list(): %s\n" % e)
```

### Parameters

| Name                | Type    | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | Notes        |
| ------------------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------ |
| **x_organization**  | **str** | Organization unique slug                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | \[optional\] |
| **assignee**        | **str** | A simple equality filter for the assignee field                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | \[optional\] |
| **dimension**       | **str** | A simple equality filter for the dimension field                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | \[optional\] |
| **filter**          | **str** | JSON Logic filter. This filter can be used to perform complex filtering by grouping rules. For example, using such a filter you can get all resources created by you: - {"and":\[{"==":\[{"var":"owner"}," "\]}\]} Details about the syntax used can be found at the link: [https://jsonlogic.com/](https://jsonlogic.com/) Available filter_fields: \[‘project_name’, ’name’, ‘owner’, ‘status’, ‘assignee’, ‘subset’, ‘mode’, ‘dimension’, ’tracker_link’, ‘validation_mode’, ‘id’, ‘project_id’, ‘updated_date’\]. There are few examples for complex filtering tasks: - Get all tasks from 1,2,3 projects - { "and": \[{ "in": \[{ "var": "project_id" }, \[1, 2, 3\]\]}\]} - Get all completed tasks from 1 project - { "and": \[{ "==": \[{ "var": "status" }, "completed"\]}, { "==": \[{ "var": "project_id"}, 1\]}\]} | \[optional\] |
| **mode**            | **str** | A simple equality filter for the mode field                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | \[optional\] |
| **name**            | **str** | A simple equality filter for the name field                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | \[optional\] |
| **org**             | **str** | Organization unique slug                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | \[optional\] |
| **org_id**          | **int** | Organization identifier                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        | \[optional\] |
| **owner**           | **str** | A simple equality filter for the owner field                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | \[optional\] |
| **page**            | **int** | A page number within the paginated result set.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | \[optional\] |
| **page_size**       | **int** | Number of results to return per page.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          | \[optional\] |
| **project_id**      | **int** | A simple equality filter for the project_id field                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | \[optional\] |
| **project_name**    | **str** | A simple equality filter for the project_name field                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | \[optional\] |
| **search**          | **str** | A search term. Available search_fields: (‘project_name’, ’name’, ‘owner’, ‘status’, ‘assignee’, ‘subset’, ‘mode’, ‘dimension’, ’tracker_link’, ‘validation_mode’)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | \[optional\] |
| **sort**            | **str** | Which field to use when ordering the results. Available ordering_fields: \[‘project_name’, ’name’, ‘owner’, ‘status’, ‘assignee’, ‘subset’, ‘mode’, ‘dimension’, ’tracker_link’, ‘validation_mode’, ‘id’, ‘project_id’, ‘updated_date’\]                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | \[optional\] |
| **status**          | **str** | A simple equality filter for the status field                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | \[optional\] |
| **subset**          | **str** | A simple equality filter for the subset field                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | \[optional\] |
| **tracker_link**    | **str** | A simple equality filter for the tracker_link field                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | \[optional\] |
| **validation_mode** | **str** | A simple equality filter for the validation_mode field                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | \[optional\] |

There are also optional kwargs that control the function invocation behavior.[Read more here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type: `Tuple[PaginatedTaskReadList, urllib3.HTTPResponse]`.

Returns a tuple with 2 values: `(parsed_response, raw_response)`.

The first value is a model parsed from the response data. The second value is the raw response, which can be useful to get response parameters, such as status code, headers, or raw response data. Read more about invocation parameters and returned values [here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Authentication

accessTokenAuth, basicAuth, csrfAuth, csrfHeaderAuth, sessionAuth, tokenAuth

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/vnd.cvat+json

### HTTP response details

| Status code | Description | Response headers |
| ----------- | ----------- | ---------------- |
| **200**     |             | \-               |

## partial_update

> partial_update( id, patched_task_write_request=None, \*\*kwargs )

Update a task

### Example

```python
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
    id = 1 # int | A unique integer value identifying this task.
    patched_task_write_request = PatchedTaskWriteRequest(
        name="name_example",
        project_id=1,
        owner_id=1,
        assignee_id=1,
        bug_tracker="bug_tracker_example",
        labels=[
            PatchedLabelRequest(
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
            ),
        ],
        subset="subset_example",
        target_storage=StorageRequest(
            location=LocationEnum("cloud_storage"),
            cloud_storage_id=1,
        ),
        source_storage=StorageRequest(
            location=LocationEnum("cloud_storage"),
            cloud_storage_id=1,
        ),
        organization_id=1,
    ) # PatchedTaskWriteRequest |  (optional)

    try:
        (data, response) = api_client.tasks_api.partial_update(
            id,
            patched_task_write_request=patched_task_write_request,
        )
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling TasksApi.partial_update(): %s\n" % e)
```

### Parameters

| Name                           | Type                                                                                                             | Description                                   | Notes        |
| ------------------------------ | ---------------------------------------------------------------------------------------------------------------- | --------------------------------------------- | ------------ |
| **id**                         | **int**                                                                                                          | A unique integer value identifying this task. |              |
| **patched_task_write_request** | [**PatchedTaskWriteRequest**](https://docs.cvat.ai/docs/api_sdk/sdk/reference/models/patched-task-write-request) |                                               | \[optional\] |

There are also optional kwargs that control the function invocation behavior.[Read more here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type: `Tuple[TaskRead, urllib3.HTTPResponse]`.

Returns a tuple with 2 values: `(parsed_response, raw_response)`.

The first value is a model parsed from the response data. The second value is the raw response, which can be useful to get response parameters, such as status code, headers, or raw response data. Read more about invocation parameters and returned values [here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Authentication

accessTokenAuth, basicAuth, csrfAuth, csrfHeaderAuth, sessionAuth, tokenAuth

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/vnd.cvat+json

### HTTP response details

| Status code | Description | Response headers |
| ----------- | ----------- | ---------------- |
| **200**     |             | \-               |

## partial_update_annotations

> partial_update_annotations( action, id, patched_labeled_data_request=None, \*\*kwargs )

Update task annotations

### Example

```python
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
    id = 1 # int | A unique integer value identifying this task.
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
        (data, response) = api_client.tasks_api.partial_update_annotations(
            action,
            id,
            patched_labeled_data_request=patched_labeled_data_request,
        )
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling TasksApi.partial_update_annotations(): %s\n" % e)
```

### Parameters

| Name                             | Type                                                                                                                 | Description                                   | Notes        |
| -------------------------------- | -------------------------------------------------------------------------------------------------------------------- | --------------------------------------------- | ------------ |
| **action**                       | **str**                                                                                                              |                                               |              |
| **id**                           | **int**                                                                                                              | A unique integer value identifying this task. |              |
| **patched_labeled_data_request** | [**PatchedLabeledDataRequest**](https://docs.cvat.ai/docs/api_sdk/sdk/reference/models/patched-labeled-data-request) |                                               | \[optional\] |

There are also optional kwargs that control the function invocation behavior.[Read more here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type: `Tuple[LabeledData, urllib3.HTTPResponse]`.

Returns a tuple with 2 values: `(parsed_response, raw_response)`.

The first value is a model parsed from the response data. The second value is the raw response, which can be useful to get response parameters, such as status code, headers, or raw response data. Read more about invocation parameters and returned values [here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Authentication

accessTokenAuth, basicAuth, csrfAuth, csrfHeaderAuth, sessionAuth, tokenAuth

### HTTP request headers

- **Content-Type**: application/json, multipart/form-data
- **Accept**: application/vnd.cvat+json

### HTTP response details

| Status code | Description | Response headers |
| ----------- | ----------- | ---------------- |
| **200**     |             | \-               |

## partial_update_data_meta

> partial_update_data_meta( id, patched_data_meta_write_request=None, \*\*kwargs )

Update metainformation for media files in a task

### Example

```python
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
    id = 1 # int | A unique integer value identifying this task.
    patched_data_meta_write_request = PatchedDataMetaWriteRequest(
        deleted_frames=[
            0,
        ],
        cloud_storage_id=1,
    ) # PatchedDataMetaWriteRequest |  (optional)

    try:
        (data, response) = api_client.tasks_api.partial_update_data_meta(
            id,
            patched_data_meta_write_request=patched_data_meta_write_request,
        )
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling TasksApi.partial_update_data_meta(): %s\n" % e)
```

### Parameters

| Name                                | Type                                                                                                                      | Description                                   | Notes        |
| ----------------------------------- | ------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------- | ------------ |
| **id**                              | **int**                                                                                                                   | A unique integer value identifying this task. |              |
| **patched_data_meta_write_request** | [**PatchedDataMetaWriteRequest**](https://docs.cvat.ai/docs/api_sdk/sdk/reference/models/patched-data-meta-write-request) |                                               | \[optional\] |

There are also optional kwargs that control the function invocation behavior.[Read more here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type: `Tuple[DataMetaRead, urllib3.HTTPResponse]`.

Returns a tuple with 2 values: `(parsed_response, raw_response)`.

The first value is a model parsed from the response data. The second value is the raw response, which can be useful to get response parameters, such as status code, headers, or raw response data. Read more about invocation parameters and returned values [here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Authentication

accessTokenAuth, basicAuth, csrfAuth, csrfHeaderAuth, sessionAuth, tokenAuth

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/vnd.cvat+json

### HTTP response details

| Status code | Description | Response headers |
| ----------- | ----------- | ---------------- |
| **200**     |             | \-               |

## partial_update_validation_layout

> partial_update_validation_layout( id, patched_task_validation_layout_write_request=None, \*\*kwargs )

Allows updating current validation configuration

WARNING: this operation is not protected from race conditions. It’s up to the user to ensure no parallel calls to this operation happen. It affects image access, including exports with images, backups, chunk downloading etc.

### Example

```python
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
    id = 1 # int | A unique integer value identifying this task.
    patched_task_validation_layout_write_request = PatchedTaskValidationLayoutWriteRequest(
        disabled_frames=[
            0,
        ],
        frame_selection_method=None,
        honeypot_real_frames=[
            0,
        ],
    ) # PatchedTaskValidationLayoutWriteRequest |  (optional)

    try:
        (data, response) = api_client.tasks_api.partial_update_validation_layout(
            id,
            patched_task_validation_layout_write_request=patched_task_validation_layout_write_request,
        )
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling TasksApi.partial_update_validation_layout(): %s\n" % e)
```

### Parameters

| Name                                             | Type                                                                                                                                               | Description                                   | Notes        |
| ------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------- | ------------ |
| **id**                                           | **int**                                                                                                                                            | A unique integer value identifying this task. |              |
| **patched_task_validation_layout_write_request** | [**PatchedTaskValidationLayoutWriteRequest**](https://docs.cvat.ai/docs/api_sdk/sdk/reference/models/patched-task-validation-layout-write-request) |                                               | \[optional\] |

There are also optional kwargs that control the function invocation behavior.[Read more here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type: `Tuple[TaskValidationLayoutRead, urllib3.HTTPResponse]`.

Returns a tuple with 2 values: `(parsed_response, raw_response)`.

The first value is a model parsed from the response data. The second value is the raw response, which can be useful to get response parameters, such as status code, headers, or raw response data. Read more about invocation parameters and returned values [here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Authentication

accessTokenAuth, basicAuth, csrfAuth, csrfHeaderAuth, sessionAuth, tokenAuth

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/vnd.cvat+json

### HTTP response details

| Status code | Description | Response headers |
| ----------- | ----------- | ---------------- |
| **200**     |             | \-               |

## retrieve

> retrieve( id, \*\*kwargs )

Get task details

### Example

```python
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
    id = 1 # int | A unique integer value identifying this task.

    try:
        (data, response) = api_client.tasks_api.retrieve(
            id,)
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling TasksApi.retrieve(): %s\n" % e)
```

### Parameters

| Name   | Type    | Description                                   | Notes |
| ------ | ------- | --------------------------------------------- | ----- |
| **id** | **int** | A unique integer value identifying this task. |       |

There are also optional kwargs that control the function invocation behavior.[Read more here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type: `Tuple[TaskRead, urllib3.HTTPResponse]`.

Returns a tuple with 2 values: `(parsed_response, raw_response)`.

The first value is a model parsed from the response data. The second value is the raw response, which can be useful to get response parameters, such as status code, headers, or raw response data. Read more about invocation parameters and returned values [here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Authentication

accessTokenAuth, basicAuth, csrfAuth, csrfHeaderAuth, sessionAuth, tokenAuth

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/vnd.cvat+json

### HTTP response details

| Status code | Description | Response headers |
| ----------- | ----------- | ---------------- |
| **200**     |             | \-               |

## retrieve_annotations

> retrieve_annotations( id, \*\*kwargs )

Get task annotations

### Example

```python
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
    id = 1 # int | A unique integer value identifying this task.

    try:
        (data, response) = api_client.tasks_api.retrieve_annotations(
            id,)
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling TasksApi.retrieve_annotations(): %s\n" % e)
```

### Parameters

| Name   | Type    | Description                                   | Notes |
| ------ | ------- | --------------------------------------------- | ----- |
| **id** | **int** | A unique integer value identifying this task. |       |

There are also optional kwargs that control the function invocation behavior.[Read more here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type: `Tuple[LabeledData, urllib3.HTTPResponse]`.

Returns a tuple with 2 values: `(parsed_response, raw_response)`.

The first value is a model parsed from the response data. The second value is the raw response, which can be useful to get response parameters, such as status code, headers, or raw response data. Read more about invocation parameters and returned values [here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Authentication

accessTokenAuth, basicAuth, csrfAuth, csrfHeaderAuth, sessionAuth, tokenAuth

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/vnd.cvat+json

### HTTP response details

| Status code | Description                                      | Response headers |
| ----------- | ------------------------------------------------ | ---------------- |
| **200**     |                                                  | \-               |
| **400**     | Exporting without data is not allowed            | \-               |
| **410**     | API endpoint no longer handles exporting process | \-               |

## retrieve_data

> retrieve_data( id, type, number=None, quality=None, \*\*kwargs )

Get data of a task

### Example

```python
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
    id = 1 # int | A unique integer value identifying this task.
    type = "chunk" # str | Specifies the type of the requested data
    number = 1 # int | A unique number value identifying chunk or frame (optional)
    quality = "compressed" # str | Specifies the quality level of the requested data (optional)

    try:
        api_client.tasks_api.retrieve_data(
            id,
            type,
            number=number,
            quality=quality,
        )
    except exceptions.ApiException as e:
        print("Exception when calling TasksApi.retrieve_data(): %s\n" % e)
```

### Parameters

| Name        | Type    | Description                                       | Notes        |
| ----------- | ------- | ------------------------------------------------- | ------------ |
| **id**      | **int** | A unique integer value identifying this task.     |              |
| **type**    | **str** | Specifies the type of the requested data          |              |
| **number**  | **int** | A unique number value identifying chunk or frame  | \[optional\] |
| **quality** | **str** | Specifies the quality level of the requested data | \[optional\] |

There are also optional kwargs that control the function invocation behavior.[Read more here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type: `Tuple[None, urllib3.HTTPResponse]`.

Returns a tuple with 2 values: `(None, raw_response)`.

This endpoint does not have any return value, so `None` is always returned as the first value. The second value is the raw response, which can be useful to get response parameters, such as status code, headers, or raw response data. Read more about invocation parameters and returned values [here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Authentication

accessTokenAuth, basicAuth, csrfAuth, csrfHeaderAuth, sessionAuth, tokenAuth

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: Not defined

### HTTP response details

| Status code | Description             | Response headers                                                                                                           |
| ----------- | ----------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| **200**     | Data of a specific type | \* X-Checksum - Data checksum, applicable for chunks only \* X-Updated-Date - Data update date, applicable for chunks only |

## retrieve_data_meta

> retrieve_data_meta( id, \*\*kwargs )

Get metainformation for media files in a task

### Example

```python
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
    id = 1 # int | A unique integer value identifying this task.

    try:
        (data, response) = api_client.tasks_api.retrieve_data_meta(
            id,)
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling TasksApi.retrieve_data_meta(): %s\n" % e)
```

### Parameters

| Name   | Type    | Description                                   | Notes |
| ------ | ------- | --------------------------------------------- | ----- |
| **id** | **int** | A unique integer value identifying this task. |       |

There are also optional kwargs that control the function invocation behavior.[Read more here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type: `Tuple[DataMetaRead, urllib3.HTTPResponse]`.

Returns a tuple with 2 values: `(parsed_response, raw_response)`.

The first value is a model parsed from the response data. The second value is the raw response, which can be useful to get response parameters, such as status code, headers, or raw response data. Read more about invocation parameters and returned values [here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Authentication

accessTokenAuth, basicAuth, csrfAuth, csrfHeaderAuth, sessionAuth, tokenAuth

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/vnd.cvat+json

### HTTP response details

| Status code | Description | Response headers |
| ----------- | ----------- | ---------------- |
| **200**     |             | \-               |

## retrieve_preview

> retrieve_preview( id, \*\*kwargs )

Get a preview image for a task

### Example

```python
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
    id = 1 # int | A unique integer value identifying this task.

    try:
        api_client.tasks_api.retrieve_preview(
            id,)
    except exceptions.ApiException as e:
        print("Exception when calling TasksApi.retrieve_preview(): %s\n" % e)
```

### Parameters

| Name   | Type    | Description                                   | Notes |
| ------ | ------- | --------------------------------------------- | ----- |
| **id** | **int** | A unique integer value identifying this task. |       |

There are also optional kwargs that control the function invocation behavior.[Read more here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type: `Tuple[None, urllib3.HTTPResponse]`.

Returns a tuple with 2 values: `(None, raw_response)`.

This endpoint does not have any return value, so `None` is always returned as the first value. The second value is the raw response, which can be useful to get response parameters, such as status code, headers, or raw response data. Read more about invocation parameters and returned values [here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Authentication

accessTokenAuth, basicAuth, csrfAuth, csrfHeaderAuth, sessionAuth, tokenAuth

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: Not defined

### HTTP response details

| Status code | Description                  | Response headers |
| ----------- | ---------------------------- | ---------------- |
| **200**     | Task image preview           | \-               |
| **404**     | Task image preview not found | \-               |

## retrieve_status

> retrieve_status( id, \*\*kwargs )

Get the creation status of a task

This method is deprecated and will be removed in one of the next releases. To check status of task creation, use new common API for managing background operations: GET /api/requests/?action=create&task_id=<task_id>

### Example

```python
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
    id = 1 # int | A unique integer value identifying this task.

    try:
        (data, response) = api_client.tasks_api.retrieve_status(
            id,)
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling TasksApi.retrieve_status(): %s\n" % e)
```

### Parameters

| Name   | Type    | Description                                   | Notes |
| ------ | ------- | --------------------------------------------- | ----- |
| **id** | **int** | A unique integer value identifying this task. |       |

There are also optional kwargs that control the function invocation behavior.[Read more here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type: `Tuple[RqStatus, urllib3.HTTPResponse]`.

Returns a tuple with 2 values: `(parsed_response, raw_response)`.

The first value is a model parsed from the response data. The second value is the raw response, which can be useful to get response parameters, such as status code, headers, or raw response data. Read more about invocation parameters and returned values [here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Authentication

accessTokenAuth, basicAuth, csrfAuth, csrfHeaderAuth, sessionAuth, tokenAuth

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/vnd.cvat+json

### HTTP response details

| Status code | Description | Response headers |
| ----------- | ----------- | ---------------- |
| **200**     |             | \-               |

## retrieve_validation_layout

> retrieve_validation_layout( id, \*\*kwargs )

Allows getting current validation configuration

### Example

```python
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
    id = 1 # int | A unique integer value identifying this task.

    try:
        (data, response) = api_client.tasks_api.retrieve_validation_layout(
            id,)
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling TasksApi.retrieve_validation_layout(): %s\n" % e)
```

### Parameters

| Name   | Type    | Description                                   | Notes |
| ------ | ------- | --------------------------------------------- | ----- |
| **id** | **int** | A unique integer value identifying this task. |       |

There are also optional kwargs that control the function invocation behavior.[Read more here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type: `Tuple[TaskValidationLayoutRead, urllib3.HTTPResponse]`.

Returns a tuple with 2 values: `(parsed_response, raw_response)`.

The first value is a model parsed from the response data. The second value is the raw response, which can be useful to get response parameters, such as status code, headers, or raw response data. Read more about invocation parameters and returned values [here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Authentication

accessTokenAuth, basicAuth, csrfAuth, csrfHeaderAuth, sessionAuth, tokenAuth

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/vnd.cvat+json

### HTTP response details

| Status code | Description | Response headers |
| ----------- | ----------- | ---------------- |
| **200**     |             | \-               |

## update_annotations

> update_annotations( id, labeled_data_request=None, \*\*kwargs )

Replace task annotations

### Example

```python
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
    id = 1 # int | A unique integer value identifying this task.
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
        api_client.tasks_api.update_annotations(
            id,
            labeled_data_request=labeled_data_request,
        )
    except exceptions.ApiException as e:
        print("Exception when calling TasksApi.update_annotations(): %s\n" % e)
```

### Parameters

| Name                     | Type                                                                                                  | Description                                   | Notes        |
| ------------------------ | ----------------------------------------------------------------------------------------------------- | --------------------------------------------- | ------------ |
| **id**                   | **int**                                                                                               | A unique integer value identifying this task. |              |
| **labeled_data_request** | [**LabeledDataRequest**](https://docs.cvat.ai/docs/api_sdk/sdk/reference/models/labeled-data-request) |                                               | \[optional\] |

There are also optional kwargs that control the function invocation behavior.[Read more here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type: `Tuple[None, urllib3.HTTPResponse]`.

Returns a tuple with 2 values: `(None, raw_response)`.

This endpoint does not have any return value, so `None` is always returned as the first value. The second value is the raw response, which can be useful to get response parameters, such as status code, headers, or raw response data. Read more about invocation parameters and returned values [here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Authentication

accessTokenAuth, basicAuth, csrfAuth, csrfHeaderAuth, sessionAuth, tokenAuth

### HTTP request headers

- **Content-Type**: application/json, multipart/form-data
- **Accept**: Not defined

### HTTP response details

| Status code | Description                    | Response headers |
| ----------- | ------------------------------ | ---------------- |
| **200**     | Annotations have been replaced | \-               |
