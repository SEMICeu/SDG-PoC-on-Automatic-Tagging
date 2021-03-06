# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from ..models.base_model_ import Model
from ..models.meta_tag import MetaTag  # noqa: F401,E501
from .. import util


class EnhanceResponse(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, metatags: List[MetaTag]=None):  # noqa: E501
        """EnhanceResponse - a model defined in Swagger

        :param metatags: The metatags of this EnhanceResponse.  # noqa: E501
        :type metatags: List[MetaTag]
        """
        self.swagger_types = {
            'metatags': List[MetaTag]
        }

        self.attribute_map = {
            'metatags': 'metatags'
        }
        self._metatags = metatags

    @classmethod
    def from_dict(cls, dikt) -> 'EnhanceResponse':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The EnhanceResponse of this EnhanceResponse.  # noqa: E501
        :rtype: EnhanceResponse
        """
        return util.deserialize_model(dikt, cls)

    @property
    def metatags(self) -> List[MetaTag]:
        """Gets the metatags of this EnhanceResponse.

        Array of metatags  # noqa: E501

        :return: The metatags of this EnhanceResponse.
        :rtype: List[MetaTag]
        """
        return self._metatags

    @metatags.setter
    def metatags(self, metatags: List[MetaTag]):
        """Sets the metatags of this EnhanceResponse.

        Array of metatags  # noqa: E501

        :param metatags: The metatags of this EnhanceResponse.
        :type metatags: List[MetaTag]
        """
        if metatags is None:
            raise ValueError("Invalid value for `metatags`, must not be `None`")  # noqa: E501

        self._metatags = metatags
