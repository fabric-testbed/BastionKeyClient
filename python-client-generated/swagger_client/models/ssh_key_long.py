# coding: utf-8

"""
    User Information Service

    FABRIC User Information Service  # noqa: E501

    OpenAPI spec version: 1.1.0
    Contact: ibaldin@renci.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class SshKeyLong(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'key_uuid': 'str',
        'public_key': 'str',
        'ssh_key_type': 'str',
        'comment': 'str',
        'description': 'str',
        'fingerprint': 'str',
        'fabric_key_type': 'SshKeyType',
        'created_on': 'str',
        'expires_on': 'str',
        'deactivated_on': 'str',
        'deactivation_reason': 'str'
    }

    attribute_map = {
        'key_uuid': 'key_uuid',
        'public_key': 'public_key',
        'ssh_key_type': 'ssh_key_type',
        'comment': 'comment',
        'description': 'description',
        'fingerprint': 'fingerprint',
        'fabric_key_type': 'fabric_key_type',
        'created_on': 'created_on',
        'expires_on': 'expires_on',
        'deactivated_on': 'deactivated_on',
        'deactivation_reason': 'deactivation_reason'
    }

    def __init__(self, key_uuid=None, public_key=None, ssh_key_type=None, comment=None, description=None, fingerprint=None, fabric_key_type=None, created_on=None, expires_on=None, deactivated_on=None, deactivation_reason=None):  # noqa: E501
        """SshKeyLong - a model defined in Swagger"""  # noqa: E501
        self._key_uuid = None
        self._public_key = None
        self._ssh_key_type = None
        self._comment = None
        self._description = None
        self._fingerprint = None
        self._fabric_key_type = None
        self._created_on = None
        self._expires_on = None
        self._deactivated_on = None
        self._deactivation_reason = None
        self.discriminator = None
        if key_uuid is not None:
            self.key_uuid = key_uuid
        if public_key is not None:
            self.public_key = public_key
        if ssh_key_type is not None:
            self.ssh_key_type = ssh_key_type
        if comment is not None:
            self.comment = comment
        if description is not None:
            self.description = description
        if fingerprint is not None:
            self.fingerprint = fingerprint
        if fabric_key_type is not None:
            self.fabric_key_type = fabric_key_type
        if created_on is not None:
            self.created_on = created_on
        if expires_on is not None:
            self.expires_on = expires_on
        if deactivated_on is not None:
            self.deactivated_on = deactivated_on
        if deactivation_reason is not None:
            self.deactivation_reason = deactivation_reason

    @property
    def key_uuid(self):
        """Gets the key_uuid of this SshKeyLong.  # noqa: E501


        :return: The key_uuid of this SshKeyLong.  # noqa: E501
        :rtype: str
        """
        return self._key_uuid

    @key_uuid.setter
    def key_uuid(self, key_uuid):
        """Sets the key_uuid of this SshKeyLong.


        :param key_uuid: The key_uuid of this SshKeyLong.  # noqa: E501
        :type: str
        """

        self._key_uuid = key_uuid

    @property
    def public_key(self):
        """Gets the public_key of this SshKeyLong.  # noqa: E501


        :return: The public_key of this SshKeyLong.  # noqa: E501
        :rtype: str
        """
        return self._public_key

    @public_key.setter
    def public_key(self, public_key):
        """Sets the public_key of this SshKeyLong.


        :param public_key: The public_key of this SshKeyLong.  # noqa: E501
        :type: str
        """

        self._public_key = public_key

    @property
    def ssh_key_type(self):
        """Gets the ssh_key_type of this SshKeyLong.  # noqa: E501


        :return: The ssh_key_type of this SshKeyLong.  # noqa: E501
        :rtype: str
        """
        return self._ssh_key_type

    @ssh_key_type.setter
    def ssh_key_type(self, ssh_key_type):
        """Sets the ssh_key_type of this SshKeyLong.


        :param ssh_key_type: The ssh_key_type of this SshKeyLong.  # noqa: E501
        :type: str
        """

        self._ssh_key_type = ssh_key_type

    @property
    def comment(self):
        """Gets the comment of this SshKeyLong.  # noqa: E501


        :return: The comment of this SshKeyLong.  # noqa: E501
        :rtype: str
        """
        return self._comment

    @comment.setter
    def comment(self, comment):
        """Sets the comment of this SshKeyLong.


        :param comment: The comment of this SshKeyLong.  # noqa: E501
        :type: str
        """

        self._comment = comment

    @property
    def description(self):
        """Gets the description of this SshKeyLong.  # noqa: E501


        :return: The description of this SshKeyLong.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this SshKeyLong.


        :param description: The description of this SshKeyLong.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def fingerprint(self):
        """Gets the fingerprint of this SshKeyLong.  # noqa: E501


        :return: The fingerprint of this SshKeyLong.  # noqa: E501
        :rtype: str
        """
        return self._fingerprint

    @fingerprint.setter
    def fingerprint(self, fingerprint):
        """Sets the fingerprint of this SshKeyLong.


        :param fingerprint: The fingerprint of this SshKeyLong.  # noqa: E501
        :type: str
        """

        self._fingerprint = fingerprint

    @property
    def fabric_key_type(self):
        """Gets the fabric_key_type of this SshKeyLong.  # noqa: E501


        :return: The fabric_key_type of this SshKeyLong.  # noqa: E501
        :rtype: SshKeyType
        """
        return self._fabric_key_type

    @fabric_key_type.setter
    def fabric_key_type(self, fabric_key_type):
        """Sets the fabric_key_type of this SshKeyLong.


        :param fabric_key_type: The fabric_key_type of this SshKeyLong.  # noqa: E501
        :type: SshKeyType
        """

        self._fabric_key_type = fabric_key_type

    @property
    def created_on(self):
        """Gets the created_on of this SshKeyLong.  # noqa: E501


        :return: The created_on of this SshKeyLong.  # noqa: E501
        :rtype: str
        """
        return self._created_on

    @created_on.setter
    def created_on(self, created_on):
        """Sets the created_on of this SshKeyLong.


        :param created_on: The created_on of this SshKeyLong.  # noqa: E501
        :type: str
        """

        self._created_on = created_on

    @property
    def expires_on(self):
        """Gets the expires_on of this SshKeyLong.  # noqa: E501


        :return: The expires_on of this SshKeyLong.  # noqa: E501
        :rtype: str
        """
        return self._expires_on

    @expires_on.setter
    def expires_on(self, expires_on):
        """Sets the expires_on of this SshKeyLong.


        :param expires_on: The expires_on of this SshKeyLong.  # noqa: E501
        :type: str
        """

        self._expires_on = expires_on

    @property
    def deactivated_on(self):
        """Gets the deactivated_on of this SshKeyLong.  # noqa: E501


        :return: The deactivated_on of this SshKeyLong.  # noqa: E501
        :rtype: str
        """
        return self._deactivated_on

    @deactivated_on.setter
    def deactivated_on(self, deactivated_on):
        """Sets the deactivated_on of this SshKeyLong.


        :param deactivated_on: The deactivated_on of this SshKeyLong.  # noqa: E501
        :type: str
        """

        self._deactivated_on = deactivated_on

    @property
    def deactivation_reason(self):
        """Gets the deactivation_reason of this SshKeyLong.  # noqa: E501


        :return: The deactivation_reason of this SshKeyLong.  # noqa: E501
        :rtype: str
        """
        return self._deactivation_reason

    @deactivation_reason.setter
    def deactivation_reason(self, deactivation_reason):
        """Sets the deactivation_reason of this SshKeyLong.


        :param deactivation_reason: The deactivation_reason of this SshKeyLong.  # noqa: E501
        :type: str
        """

        self._deactivation_reason = deactivation_reason

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(SshKeyLong, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, SshKeyLong):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
