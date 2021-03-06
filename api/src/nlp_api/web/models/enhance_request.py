# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from ..models.base_model_ import Model
from .. import util


class EnhanceRequest(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, metatags: List[str]=None, url: str=None, text: str=None):  # noqa: E501
        """EnhanceRequest - a model defined in Swagger

        :param metatags: The metatags of this EnhanceRequest.  # noqa: E501
        :type metatags: List[str]
        :param url: The url of this EnhanceRequest.  # noqa: E501
        :type url: str
        :param text: The text of this EnhanceRequest.  # noqa: E501
        :type text: str
        """
        self.swagger_types = {
            'metatags': List[str],
            'url': str,
            'text': str
        }

        self.attribute_map = {
            'metatags': 'metatags',
            'url': 'url',
            'text': 'text'
        }
        self._metatags = metatags
        self._url = url
        self._text = text

    @classmethod
    def from_dict(cls, dikt) -> 'EnhanceRequest':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The EnhanceRequest of this EnhanceRequest.  # noqa: E501
        :rtype: EnhanceRequest
        """
        return util.deserialize_model(dikt, cls)

    @property
    def metatags(self) -> List[str]:
        """Gets the metatags of this EnhanceRequest.

        the list of metatags to be extracted from the text  # noqa: E501

        :return: The metatags of this EnhanceRequest.
        :rtype: List[str]
        """
        return self._metatags

    @metatags.setter
    def metatags(self, metatags: List[str]):
        """Sets the metatags of this EnhanceRequest.

        the list of metatags to be extracted from the text  # noqa: E501

        :param metatags: The metatags of this EnhanceRequest.
        :type metatags: List[str]
        """
        if metatags is None:
            raise ValueError("Invalid value for `metatags`, must not be `None`")  # noqa: E501

        self._metatags = metatags

    @property
    def url(self) -> str:
        """Gets the url of this EnhanceRequest.

        the URL of the webpage containing the text  # noqa: E501

        :return: The url of this EnhanceRequest.
        :rtype: str
        """
        return self._url

    @url.setter
    def url(self, url: str):
        """Sets the url of this EnhanceRequest.

        the URL of the webpage containing the text  # noqa: E501

        :param url: The url of this EnhanceRequest.
        :type url: str
        """
        if url is None:
            raise ValueError("Invalid value for `url`, must not be `None`")  # noqa: E501

        self._url = url

    @property
    def text(self) -> str:
        """Gets the text of this EnhanceRequest.

        the text to be enhanced with metatags  # noqa: E501

        :return: The text of this EnhanceRequest.
        :rtype: str
        """
        return self._text

    @text.setter
    def text(self, text: str):
        """Sets the text of this EnhanceRequest.

        the text to be enhanced with metatags  # noqa: E501

        :param text: The text of this EnhanceRequest.
        :type text: str
        """
        if text is None:
            raise ValueError("Invalid value for `text`, must not be `None`")  # noqa: E501

        self._text = text
