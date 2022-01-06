# swagger_client.DefaultApi

All URIs are relative to *http://127.0.0.1:5000/*

Method | HTTP request | Description
------------- | ------------- | -------------
[**version_get**](DefaultApi.md#version_get) | **GET** /version | version (open)

# **version_get**
> Version version_get()

version (open)

Version

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.DefaultApi()

try:
    # version (open)
    api_response = api_instance.version_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DefaultApi->version_get: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**Version**](Version.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

