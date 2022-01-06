# swagger_client.PublicationsApi

All URIs are relative to *http://127.0.0.1:5000/*

Method | HTTP request | Description
------------- | ------------- | -------------
[**authorids_idtype_uuid_get**](PublicationsApi.md#authorids_idtype_uuid_get) | **GET** /authorids/{idtype}/{uuid} | get users specific author ID (open only to self)
[**authorids_idtype_uuid_put**](PublicationsApi.md#authorids_idtype_uuid_put) | **PUT** /authorids/{idtype}/{uuid} | update user&#x27;s specific author ID (open only to self)
[**authorids_uuid_get**](PublicationsApi.md#authorids_uuid_get) | **GET** /authorids/{uuid} | get user&#x27;s author IDs (Scopus, Orcid etc.; open only to self)

# **authorids_idtype_uuid_get**
> str authorids_idtype_uuid_get(idtype, uuid)

get users specific author ID (open only to self)

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.PublicationsApi()
idtype = swagger_client.AuthorIdType() # AuthorIdType | 
uuid = 'uuid_example' # str | 

try:
    # get users specific author ID (open only to self)
    api_response = api_instance.authorids_idtype_uuid_get(idtype, uuid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PublicationsApi->authorids_idtype_uuid_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **idtype** | [**AuthorIdType**](.md)|  | 
 **uuid** | **str**|  | 

### Return type

**str**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **authorids_idtype_uuid_put**
> str authorids_idtype_uuid_put(idtype, uuid, idval)

update user's specific author ID (open only to self)

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.PublicationsApi()
idtype = swagger_client.AuthorIdType() # AuthorIdType | 
uuid = 'uuid_example' # str | 
idval = 'idval_example' # str | 

try:
    # update user's specific author ID (open only to self)
    api_response = api_instance.authorids_idtype_uuid_put(idtype, uuid, idval)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PublicationsApi->authorids_idtype_uuid_put: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **idtype** | [**AuthorIdType**](.md)|  | 
 **uuid** | **str**|  | 
 **idval** | **str**|  | 

### Return type

**str**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **authorids_uuid_get**
> list[AuthorId] authorids_uuid_get(uuid)

get user's author IDs (Scopus, Orcid etc.; open only to self)

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.PublicationsApi()
uuid = 'uuid_example' # str | 

try:
    # get user's author IDs (Scopus, Orcid etc.; open only to self)
    api_response = api_instance.authorids_uuid_get(uuid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PublicationsApi->authorids_uuid_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **uuid** | **str**|  | 

### Return type

[**list[AuthorId]**](AuthorId.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

