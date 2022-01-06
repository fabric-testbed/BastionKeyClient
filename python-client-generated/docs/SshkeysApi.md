# swagger_client.SshkeysApi

All URIs are relative to *http://127.0.0.1:5000/*

Method | HTTP request | Description
------------- | ------------- | -------------
[**bastionkeys_get**](SshkeysApi.md#bastionkeys_get) | **GET** /bastionkeys | Get a list of bastion keys that were created, deactivated or expired since specified date in UTC (open to Bastion hosts)
[**sshkey_keyid_delete**](SshkeysApi.md#sshkey_keyid_delete) | **DELETE** /sshkey/{keyid} | Delete a specified key based on key UUID (open only to self)
[**sshkey_keyid_get**](SshkeysApi.md#sshkey_keyid_get) | **GET** /sshkey/{keyid} | get metadata, including expiration date for this key based on key UUID (open only to self)
[**sshkey_keytype_post**](SshkeysApi.md#sshkey_keytype_post) | **POST** /sshkey/{keytype} | Add a user-provided ssh public key of specified type. (open only to self)
[**sshkey_keytype_put**](SshkeysApi.md#sshkey_keytype_put) | **PUT** /sshkey/{keytype} | Generate a new SSH key of specified type. Return both public and private portions. (open only to self)
[**sshkey_uuid_keyid_get**](SshkeysApi.md#sshkey_uuid_keyid_get) | **GET** /sshkey/{uuid}/{keyid} | Get a specific key of a given user (open to any valid user)
[**sshkeys_get**](SshkeysApi.md#sshkeys_get) | **GET** /sshkeys | Get a list of all active/non-expired keys of this user (open to self)

# **bastionkeys_get**
> list[SshKeyBastion] bastionkeys_get(secret, since_date)

Get a list of bastion keys that were created, deactivated or expired since specified date in UTC (open to Bastion hosts)

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.SshkeysApi()
secret = 'secret_example' # str | 
since_date = 'since_date_example' # str | 

try:
    # Get a list of bastion keys that were created, deactivated or expired since specified date in UTC (open to Bastion hosts)
    api_response = api_instance.bastionkeys_get(secret, since_date)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SshkeysApi->bastionkeys_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **secret** | **str**|  | 
 **since_date** | **str**|  | 

### Return type

[**list[SshKeyBastion]**](SshKeyBastion.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **sshkey_keyid_delete**
> str sshkey_keyid_delete(keyid)

Delete a specified key based on key UUID (open only to self)

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.SshkeysApi()
keyid = 'keyid_example' # str | 

try:
    # Delete a specified key based on key UUID (open only to self)
    api_response = api_instance.sshkey_keyid_delete(keyid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SshkeysApi->sshkey_keyid_delete: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **keyid** | **str**|  | 

### Return type

**str**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **sshkey_keyid_get**
> SshKeyLong sshkey_keyid_get(keyid)

get metadata, including expiration date for this key based on key UUID (open only to self)

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.SshkeysApi()
keyid = 'keyid_example' # str | 

try:
    # get metadata, including expiration date for this key based on key UUID (open only to self)
    api_response = api_instance.sshkey_keyid_get(keyid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SshkeysApi->sshkey_keyid_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **keyid** | **str**|  | 

### Return type

[**SshKeyLong**](SshKeyLong.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **sshkey_keytype_post**
> str sshkey_keytype_post(keytype, public_openssh, description)

Add a user-provided ssh public key of specified type. (open only to self)

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.SshkeysApi()
keytype = swagger_client.SshKeyType() # SshKeyType | 
public_openssh = 'public_openssh_example' # str | 
description = 'description_example' # str | 

try:
    # Add a user-provided ssh public key of specified type. (open only to self)
    api_response = api_instance.sshkey_keytype_post(keytype, public_openssh, description)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SshkeysApi->sshkey_keytype_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **keytype** | [**SshKeyType**](.md)|  | 
 **public_openssh** | **str**|  | 
 **description** | **str**|  | 

### Return type

**str**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **sshkey_keytype_put**
> SshKeyPair sshkey_keytype_put(keytype, comment, description)

Generate a new SSH key of specified type. Return both public and private portions. (open only to self)

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.SshkeysApi()
keytype = swagger_client.SshKeyType() # SshKeyType | 
comment = 'comment_example' # str | 
description = 'description_example' # str | 

try:
    # Generate a new SSH key of specified type. Return both public and private portions. (open only to self)
    api_response = api_instance.sshkey_keytype_put(keytype, comment, description)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SshkeysApi->sshkey_keytype_put: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **keytype** | [**SshKeyType**](.md)|  | 
 **comment** | **str**|  | 
 **description** | **str**|  | 

### Return type

[**SshKeyPair**](SshKeyPair.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **sshkey_uuid_keyid_get**
> list[SshKeyLong] sshkey_uuid_keyid_get(uuid, keyid)

Get a specific key of a given user (open to any valid user)

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.SshkeysApi()
uuid = 'uuid_example' # str | 
keyid = 'keyid_example' # str | 

try:
    # Get a specific key of a given user (open to any valid user)
    api_response = api_instance.sshkey_uuid_keyid_get(uuid, keyid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SshkeysApi->sshkey_uuid_keyid_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **uuid** | **str**|  | 
 **keyid** | **str**|  | 

### Return type

[**list[SshKeyLong]**](SshKeyLong.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **sshkeys_get**
> list[SshKeyLong] sshkeys_get()

Get a list of all active/non-expired keys of this user (open to self)

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.SshkeysApi()

try:
    # Get a list of all active/non-expired keys of this user (open to self)
    api_response = api_instance.sshkeys_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SshkeysApi->sshkeys_get: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[SshKeyLong]**](SshKeyLong.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

