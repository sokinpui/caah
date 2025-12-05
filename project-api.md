All URIs are relative to _http://localhost_

| Method                                                                                                               | HTTP request                               | Description                                                             |
| -------------------------------------------------------------------------------------------------------------------- | ------------------------------------------ | ----------------------------------------------------------------------- |
| [**create**](https://docs.cvat.ai/docs/api_sdk/sdk/reference/apis/projects-api#create)                               | **POST** /api/projects                     | Create a project                                                        |
| [**create_backup**](https://docs.cvat.ai/docs/api_sdk/sdk/reference/apis/projects-api#create_backup)                 | **POST** /api/projects/backup/             | Recreate a project from a backup                                        |
| [**create_backup_export**](https://docs.cvat.ai/docs/api_sdk/sdk/reference/apis/projects-api#create_backup_export)   | **POST** /api/projects/{id}/backup/export  | Initiate process to backup resource                                     |
| [**create_dataset**](https://docs.cvat.ai/docs/api_sdk/sdk/reference/apis/projects-api#create_dataset)               | **POST** /api/projects/{id}/dataset/       | Import a dataset into a project                                         |
| [**create_dataset_export**](https://docs.cvat.ai/docs/api_sdk/sdk/reference/apis/projects-api#create_dataset_export) | **POST** /api/projects/{id}/dataset/export | Initialize process to export resource as a dataset in a specific format |
| [**destroy**](https://docs.cvat.ai/docs/api_sdk/sdk/reference/apis/projects-api#destroy)                             | **DELETE** /api/projects/{id}              | Delete a project                                                        |
| [**list**](https://docs.cvat.ai/docs/api_sdk/sdk/reference/apis/projects-api#list)                                   | **GET** /api/projects                      | List projects                                                           |
| [**partial_update**](https://docs.cvat.ai/docs/api_sdk/sdk/reference/apis/projects-api#partial_update)               | **PATCH** /api/projects/{id}               | Update a project                                                        |
| [**retrieve**](https://docs.cvat.ai/docs/api_sdk/sdk/reference/apis/projects-api#retrieve)                           | **GET** /api/projects/{id}                 | Get project details                                                     |
| [**retrieve_preview**](https://docs.cvat.ai/docs/api_sdk/sdk/reference/apis/projects-api#retrieve_preview)           | **GET** /api/projects/{id}/preview         | Get a preview image for a project                                       |

## create

> create( project_write_request, x_organization=None, org=None, org_id=None, \*\*kwargs )

Create a project

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
    project_write_request = ProjectWriteRequest(
        name="name_example",
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
        owner_id=1,
        assignee_id=1,
        bug_tracker="bug_tracker_example",
        target_storage=PatchedProjectWriteRequestTargetStorage(None),
        source_storage=PatchedProjectWriteRequestTargetStorage(None),
    ) # ProjectWriteRequest |
    x_organization = "X-Organization_example" # str | Organization unique slug (optional)
    org = "org_example" # str | Organization unique slug (optional)
    org_id = 1 # int | Organization identifier (optional)

    try:
        (data, response) = api_client.projects_api.create(
            project_write_request,
            x_organization=x_organization,
            org=org,
            org_id=org_id,
        )
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling ProjectsApi.create(): %s\n" % e)
```

### Parameters

| Name                      | Type                                                                                                    | Description              | Notes        |
| ------------------------- | ------------------------------------------------------------------------------------------------------- | ------------------------ | ------------ |
| **project_write_request** | [**ProjectWriteRequest**](https://docs.cvat.ai/docs/api_sdk/sdk/reference/models/project-write-request) |                          |              |
| **x_organization**        | **str**                                                                                                 | Organization unique slug | \[optional\] |
| **org**                   | **str**                                                                                                 | Organization unique slug | \[optional\] |
| **org_id**                | **int**                                                                                                 | Organization identifier  | \[optional\] |

There are also optional kwargs that control the function invocation behavior.[Read more here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type: `Tuple[ProjectRead, urllib3.HTTPResponse]`.

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

## create_backup

> create_backup( x_organization=None, cloud_storage_id=None, filename=None, location=None, org=None, org_id=None, project_file_request=None, \*\*kwargs )

Recreate a project from a backup

The backup import process is as follows: The first request POST /api/projects/backup schedules a background job on the server in which the process of creating a project from the uploaded backup is carried out. To check the status of the import process, use GET /api/requests/rq_id, where rq_id is the request ID obtained from the response to the previous request. Once the import completes successfully, the response will contain the ID of the newly created project in the result_id field.

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
    project_file_request = ProjectFileRequest(
        project_file=open('/path/to/file', 'rb'),
    ) # ProjectFileRequest |  (optional)

    try:
        (data, response) = api_client.projects_api.create_backup(
            x_organization=x_organization,
            cloud_storage_id=cloud_storage_id,
            filename=filename,
            location=location,
            org=org,
            org_id=org_id,
            project_file_request=project_file_request,
        )
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling ProjectsApi.create_backup(): %s\n" % e)
```

### Parameters

| Name                     | Type                                                                                                  | Description                          | Notes                                                                    |
| ------------------------ | ----------------------------------------------------------------------------------------------------- | ------------------------------------ | ------------------------------------------------------------------------ |
| **x_organization**       | **str**                                                                                               | Organization unique slug             | \[optional\]                                                             |
| **cloud_storage_id**     | **int**                                                                                               | Storage id                           | \[optional\]                                                             |
| **filename**             | **str**                                                                                               | Backup file name                     | \[optional\]                                                             |
| **location**             | **str**                                                                                               | Where to import the backup file from | \[optional\] if omitted the server will use the default value of “local” |
| **org**                  | **str**                                                                                               | Organization unique slug             | \[optional\]                                                             |
| **org_id**               | **int**                                                                                               | Organization identifier              | \[optional\]                                                             |
| **project_file_request** | [**ProjectFileRequest**](https://docs.cvat.ai/docs/api_sdk/sdk/reference/models/project-file-request) |                                      | \[optional\]                                                             |

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
    id = 1 # int | A unique integer value identifying this project.
    cloud_storage_id = 1 # int | Storage id (optional)
    filename = "filename_example" # str | Backup file name (optional)
    lightweight = True # bool | Makes a lightweight backup (without media files) for tasks whose media is located in cloud storage (optional) if omitted the server will use the default value of True
    location = "cloud_storage" # str | Where need to save downloaded backup (optional)

    try:
        (data, response) = api_client.projects_api.create_backup_export(
            id,
            cloud_storage_id=cloud_storage_id,
            filename=filename,
            lightweight=lightweight,
            location=location,
        )
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling ProjectsApi.create_backup_export(): %s\n" % e)
```

### Parameters

| Name                 | Type     | Description                                                                                        | Notes                                                                 |
| -------------------- | -------- | -------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------- |
| **id**               | **int**  | A unique integer value identifying this project.                                                   |                                                                       |
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

## create_dataset

> create_dataset( id, cloud_storage_id=None, filename=None, format=None, location=None, dataset_file_request=None, \*\*kwargs )

Import a dataset into a project

The request POST /api/projects/id/dataset initiates a background process to import dataset into a project. Please, use the GET /api/requests/<rq_id> endpoint for checking status of the process. The `rq_id` parameter can be found in the response on initiating request.

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
    id = 1 # int | A unique integer value identifying this project.
    cloud_storage_id = 1 # int | Storage id (optional)
    filename = "filename_example" # str | Dataset file name (optional)
    format = "format_example" # str | Desired dataset format name You can get the list of supported formats at: /server/annotation/formats (optional)
    location = "cloud_storage" # str | Where to import the dataset from (optional)
    dataset_file_request = DatasetFileRequest(
        dataset_file=open('/path/to/file', 'rb'),
    ) # DatasetFileRequest |  (optional)

    try:
        (data, response) = api_client.projects_api.create_dataset(
            id,
            cloud_storage_id=cloud_storage_id,
            filename=filename,
            format=format,
            location=location,
            dataset_file_request=dataset_file_request,
        )
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling ProjectsApi.create_dataset(): %s\n" % e)
```

### Parameters

| Name                     | Type                                                                                                  | Description                                                                                          | Notes        |
| ------------------------ | ----------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- | ------------ |
| **id**                   | **int**                                                                                               | A unique integer value identifying this project.                                                     |              |
| **cloud_storage_id**     | **int**                                                                                               | Storage id                                                                                           | \[optional\] |
| **filename**             | **str**                                                                                               | Dataset file name                                                                                    | \[optional\] |
| **format**               | **str**                                                                                               | Desired dataset format name You can get the list of supported formats at: /server/annotation/formats | \[optional\] |
| **location**             | **str**                                                                                               | Where to import the dataset from                                                                     | \[optional\] |
| **dataset_file_request** | [**DatasetFileRequest**](https://docs.cvat.ai/docs/api_sdk/sdk/reference/models/dataset-file-request) |                                                                                                      | \[optional\] |

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

| Status code | Description                | Response headers |
| ----------- | -------------------------- | ---------------- |
| **202**     | Importing has been started | \-               |
| **400**     | Failed to import dataset   | \-               |
| **405**     | Format is not available    | \-               |

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
    id = 1 # int | A unique integer value identifying this project.
    cloud_storage_id = 1 # int | Storage id (optional)
    filename = "filename_example" # str | Desired output file name (optional)
    location = "cloud_storage" # str | Where need to save downloaded dataset (optional)
    save_images = False # bool | Include images or not (optional) if omitted the server will use the default value of False

    try:
        (data, response) = api_client.projects_api.create_dataset_export(
            format,
            id,
            cloud_storage_id=cloud_storage_id,
            filename=filename,
            location=location,
            save_images=save_images,
        )
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling ProjectsApi.create_dataset_export(): %s\n" % e)
```

### Parameters

| Name                 | Type     | Description                                                                                         | Notes                                                                  |
| -------------------- | -------- | --------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| **format**           | **str**  | Desired output format name You can get the list of supported formats at: /server/annotation/formats |                                                                        |
| **id**               | **int**  | A unique integer value identifying this project.                                                    |                                                                        |
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

Delete a project

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
    id = 1 # int | A unique integer value identifying this project.

    try:
        api_client.projects_api.destroy(
            id,)
    except exceptions.ApiException as e:
        print("Exception when calling ProjectsApi.destroy(): %s\n" % e)
```

### Parameters

| Name   | Type    | Description                                      | Notes |
| ------ | ------- | ------------------------------------------------ | ----- |
| **id** | **int** | A unique integer value identifying this project. |       |

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
| **204**     | The project has been deleted | \-               |

## list

> list( x_organization=None, assignee=None, filter=None, name=None, org=None, org_id=None, owner=None, page=None, page_size=None, search=None, sort=None, status=None, \*\*kwargs )

List projects

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
    filter = "filter_example" # str |  JSON Logic filter. This filter can be used to perform complex filtering by grouping rules.  For example, using such a filter you can get all resources created by you:      - {\"and\":[{\"==\":[{\"var\":\"owner\"},\"<user>\"]}]}  Details about the syntax used can be found at the link: https://jsonlogic.com/   Available filter_fields: ['name', 'owner', 'assignee', 'status', 'id', 'updated_date']. (optional)
    name = "name_example" # str | A simple equality filter for the name field (optional)
    org = "org_example" # str | Organization unique slug (optional)
    org_id = 1 # int | Organization identifier (optional)
    owner = "owner_example" # str | A simple equality filter for the owner field (optional)
    page = 1 # int | A page number within the paginated result set. (optional)
    page_size = 1 # int | Number of results to return per page. (optional)
    search = "search_example" # str | A search term. Available search_fields: ('name', 'owner', 'assignee', 'status') (optional)
    sort = "sort_example" # str | Which field to use when ordering the results. Available ordering_fields: ['name', 'owner', 'assignee', 'status', 'id', 'updated_date'] (optional)
    status = "annotation" # str | A simple equality filter for the status field (optional)

    try:
        (data, response) = api_client.projects_api.list(
            x_organization=x_organization,
            assignee=assignee,
            filter=filter,
            name=name,
            org=org,
            org_id=org_id,
            owner=owner,
            page=page,
            page_size=page_size,
            search=search,
            sort=sort,
            status=status,
        )
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling ProjectsApi.list(): %s\n" % e)
```

### Parameters

| Name               | Type    | Description                                                                                                                                                                                                                                                                                                                                                                                                           | Notes        |
| ------------------ | ------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------ |
| **x_organization** | **str** | Organization unique slug                                                                                                                                                                                                                                                                                                                                                                                              | \[optional\] |
| **assignee**       | **str** | A simple equality filter for the assignee field                                                                                                                                                                                                                                                                                                                                                                       | \[optional\] |
| **filter**         | **str** | JSON Logic filter. This filter can be used to perform complex filtering by grouping rules. For example, using such a filter you can get all resources created by you: - {"and":\[{"==":\[{"var":"owner"}," "\]}\]} Details about the syntax used can be found at the link: [https://jsonlogic.com/](https://jsonlogic.com/) Available filter_fields: \[’name’, ‘owner’, ‘assignee’, ‘status’, ‘id’, ‘updated_date’\]. | \[optional\] |
| **name**           | **str** | A simple equality filter for the name field                                                                                                                                                                                                                                                                                                                                                                           | \[optional\] |
| **org**            | **str** | Organization unique slug                                                                                                                                                                                                                                                                                                                                                                                              | \[optional\] |
| **org_id**         | **int** | Organization identifier                                                                                                                                                                                                                                                                                                                                                                                               | \[optional\] |
| **owner**          | **str** | A simple equality filter for the owner field                                                                                                                                                                                                                                                                                                                                                                          | \[optional\] |
| **page**           | **int** | A page number within the paginated result set.                                                                                                                                                                                                                                                                                                                                                                        | \[optional\] |
| **page_size**      | **int** | Number of results to return per page.                                                                                                                                                                                                                                                                                                                                                                                 | \[optional\] |
| **search**         | **str** | A search term. Available search_fields: (’name’, ‘owner’, ‘assignee’, ‘status’)                                                                                                                                                                                                                                                                                                                                       | \[optional\] |
| **sort**           | **str** | Which field to use when ordering the results. Available ordering_fields: \[’name’, ‘owner’, ‘assignee’, ‘status’, ‘id’, ‘updated_date’\]                                                                                                                                                                                                                                                                              | \[optional\] |
| **status**         | **str** | A simple equality filter for the status field                                                                                                                                                                                                                                                                                                                                                                         | \[optional\] |

There are also optional kwargs that control the function invocation behavior.[Read more here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type: `Tuple[PaginatedProjectReadList, urllib3.HTTPResponse]`.

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

> partial_update( id, patched_project_write_request=None, \*\*kwargs )

Update a project

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
    id = 1 # int | A unique integer value identifying this project.
    patched_project_write_request = PatchedProjectWriteRequest(
        name="name_example",
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
        owner_id=1,
        assignee_id=1,
        bug_tracker="bug_tracker_example",
        target_storage=PatchedProjectWriteRequestTargetStorage(None),
        source_storage=PatchedProjectWriteRequestTargetStorage(None),
        organization_id=1,
    ) # PatchedProjectWriteRequest |  (optional)

    try:
        (data, response) = api_client.projects_api.partial_update(
            id,
            patched_project_write_request=patched_project_write_request,
        )
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling ProjectsApi.partial_update(): %s\n" % e)
```

### Parameters

| Name                              | Type                                                                                                                   | Description                                      | Notes        |
| --------------------------------- | ---------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------ | ------------ |
| **id**                            | **int**                                                                                                                | A unique integer value identifying this project. |              |
| **patched_project_write_request** | [**PatchedProjectWriteRequest**](https://docs.cvat.ai/docs/api_sdk/sdk/reference/models/patched-project-write-request) |                                                  | \[optional\] |

There are also optional kwargs that control the function invocation behavior.[Read more here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type: `Tuple[ProjectRead, urllib3.HTTPResponse]`.

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

Get project details

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
    id = 1 # int | A unique integer value identifying this project.

    try:
        (data, response) = api_client.projects_api.retrieve(
            id,)
        pprint(data)
    except exceptions.ApiException as e:
        print("Exception when calling ProjectsApi.retrieve(): %s\n" % e)
```

### Parameters

| Name   | Type    | Description                                      | Notes |
| ------ | ------- | ------------------------------------------------ | ----- |
| **id** | **int** | A unique integer value identifying this project. |       |

There are also optional kwargs that control the function invocation behavior.[Read more here](https://docs.cvat.ai/docs/api_sdk/sdk/lowlevel-api/#sending-requests).

### Returned values

Returned type: `Tuple[ProjectRead, urllib3.HTTPResponse]`.

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

Get a preview image for a project

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
    id = 1 # int | A unique integer value identifying this project.

    try:
        api_client.projects_api.retrieve_preview(
            id,)
    except exceptions.ApiException as e:
        print("Exception when calling ProjectsApi.retrieve_preview(): %s\n" % e)
```

### Parameters

| Name   | Type    | Description                                      | Notes |
| ------ | ------- | ------------------------------------------------ | ----- |
| **id** | **int** | A unique integer value identifying this project. |       |

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
| **200**     | Project image preview           | \-               |
| **404**     | Project image preview not found | \-               |
