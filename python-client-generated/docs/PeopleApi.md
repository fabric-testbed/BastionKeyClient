# swagger_client.PeopleApi

All URIs are relative to *http://127.0.0.1:5000/*

Method | HTTP request | Description
------------- | ------------- | -------------
[**people_get**](PeopleApi.md#people_get) | **GET** /people | list of people (open to any valid user)
[**people_uuid_get**](PeopleApi.md#people_uuid_get) | **GET** /people/{uuid} | person details by UUID (open only to self)
[**people_whoami_get**](PeopleApi.md#people_whoami_get) | **GET** /people/whoami | Details about self from OIDC Claim sub provided in ID token; Creates new entry; (open only to self)
[**uuid_oidc_claim_sub_get**](PeopleApi.md#uuid_oidc_claim_sub_get) | **GET** /uuid/oidc_claim_sub | get person UUID based on their OIDC claim sub (open to any valid user)

# **people_get**
> list[PeopleShort] people_get(person_name=person_name)

list of people (open to any valid user)

List of people

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.PeopleApi()
person_name = 'person_name_example' # str | Search People by Name (ILIKE) (optional)

try:
    # list of people (open to any valid user)
    api_response = api_instance.people_get(person_name=person_name)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PeopleApi->people_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **person_name** | **str**| Search People by Name (ILIKE) | [optional] 

### Return type

[**list[PeopleShort]**](PeopleShort.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **people_uuid_get**
> PeopleLong people_uuid_get(uuid)

person details by UUID (open only to self)

Person details by UUID

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.PeopleApi()
uuid = 'uuid_example' # str | People identifier as UUID

try:
    # person details by UUID (open only to self)
    api_response = api_instance.people_uuid_get(uuid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PeopleApi->people_uuid_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **uuid** | **str**| People identifier as UUID | 

### Return type

[**PeopleLong**](PeopleLong.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **people_whoami_get**
> list[PeopleLong] people_whoami_get()

Details about self from OIDC Claim sub provided in ID token; Creates new entry; (open only to self)

Details about self based on key OIDC Claim sub contained in ID token; Creates new entry

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.PeopleApi()

try:
    # Details about self from OIDC Claim sub provided in ID token; Creates new entry; (open only to self)
    api_response = api_instance.people_whoami_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PeopleApi->people_whoami_get: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[PeopleLong]**](PeopleLong.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **uuid_oidc_claim_sub_get**
> str uuid_oidc_claim_sub_get(oidc_claim_sub)

get person UUID based on their OIDC claim sub (open to any valid user)

person UUID based on their OIDC claim sub

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.PeopleApi()
oidc_claim_sub = 'oidc_claim_sub_example' # str | 

try:
    # get person UUID based on their OIDC claim sub (open to any valid user)
    api_response = api_instance.uuid_oidc_claim_sub_get(oidc_claim_sub)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PeopleApi->uuid_oidc_claim_sub_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **oidc_claim_sub** | **str**|  | 

### Return type

**str**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

