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

class SshKeyPair(object):
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
        'private_openssh': 'str',
        'public_openssh': 'str'
    }

    attribute_map = {
        'private_openssh': 'private_openssh',
        'public_openssh': 'public_openssh'
    }

    def __init__(self, private_openssh=None, public_openssh=None):  # noqa: E501
        """SshKeyPair - a model defined in Swagger"""  # noqa: E501
        self._private_openssh = None
        self._public_openssh = None
        self.discriminator = None
        if private_openssh is not None:
            self.private_openssh = private_openssh
        if public_openssh is not None:
            self.public_openssh = public_openssh

    @property
    def private_openssh(self):
        """Gets the private_openssh of this SshKeyPair.  # noqa: E501


        :return: The private_openssh of this SshKeyPair.  # noqa: E501
        :rtype: str
        """
        return self._private_openssh

    @private_openssh.setter
    def private_openssh(self, private_openssh):
        """Sets the private_openssh of this SshKeyPair.


        :param private_openssh: The private_openssh of this SshKeyPair.  # noqa: E501
        :type: str
        """

        self._private_openssh = private_openssh

    @property
    def public_openssh(self):
        """Gets the public_openssh of this SshKeyPair.  # noqa: E501


        :return: The public_openssh of this SshKeyPair.  # noqa: E501
        :rtype: str
        """
        return self._public_openssh

    @public_openssh.setter
    def public_openssh(self, public_openssh):
        """Sets the public_openssh of this SshKeyPair.


        :param public_openssh: The public_openssh of this SshKeyPair.  # noqa: E501
        :type: str
        """

        self._public_openssh = public_openssh

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
        if issubclass(SshKeyPair, dict):
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
        if not isinstance(other, SshKeyPair):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
