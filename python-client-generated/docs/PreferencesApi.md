# swagger_client.PreferencesApi

All URIs are relative to *http://127.0.0.1:5000/*

Method | HTTP request | Description
------------- | ------------- | -------------
[**preferences_preftype_uuid_get**](PreferencesApi.md#preferences_preftype_uuid_get) | **GET** /preferences/{preftype}/{uuid} | get user preferences of specific type (settings, permissions or interests; open only to self)
[**preferences_preftype_uuid_put**](PreferencesApi.md#preferences_preftype_uuid_put) | **PUT** /preferences/{preftype}/{uuid} | update user preferences by type (open only to self)
[**preferences_uuid_get**](PreferencesApi.md#preferences_uuid_get) | **GET** /preferences/{uuid} | get all user preferences as an object (open only to self)

# **preferences_preftype_uuid_get**
> object preferences_preftype_uuid_get(preftype, uuid)

get user preferences of specific type (settings, permissions or interests; open only to self)

User preferences (returns sane defaults if user valid, but preferences not available)

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.PreferencesApi()
preftype = swagger_client.PreferenceType() # PreferenceType | 
uuid = 'uuid_example' # str | 

try:
    # get user preferences of specific type (settings, permissions or interests; open only to self)
    api_response = api_instance.preferences_preftype_uuid_get(preftype, uuid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PreferencesApi->preferences_preftype_uuid_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **preftype** | [**PreferenceType**](.md)|  | 
 **uuid** | **str**|  | 

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **preferences_preftype_uuid_put**
> str preferences_preftype_uuid_put(uuid, preftype)

update user preferences by type (open only to self)

Update specific type of user preferences

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.PreferencesApi()
uuid = 'uuid_example' # str | 
preftype = swagger_client.PreferenceType() # PreferenceType | 

try:
    # update user preferences by type (open only to self)
    api_response = api_instance.preferences_preftype_uuid_put(uuid, preftype)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PreferencesApi->preferences_preftype_uuid_put: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **uuid** | **str**|  | 
 **preftype** | [**PreferenceType**](.md)|  | 

### Return type

**str**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **preferences_uuid_get**
> Preferences preferences_uuid_get(uuid)

get all user preferences as an object (open only to self)

Get all preferences for a user

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.PreferencesApi()
uuid = 'uuid_example' # str | 

try:
    # get all user preferences as an object (open only to self)
    api_response = api_instance.preferences_uuid_get(uuid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PreferencesApi->preferences_uuid_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **uuid** | **str**|  | 

### Return type

[**Preferences**](Preferences.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

