import connexion
import six

from ..models.enhance_request import EnhanceRequest  # noqa: E501
from ..models.enhance_response import EnhanceResponse  # noqa: E501
from ..models.status import Status  # noqa: E501
from .. import util

from nlp_api.core import metatags


def can_enhance():  # noqa: E501
    """can_enhance

    return the status of the NLP engine # noqa: E501


    :rtype: Status
    """
    status = metatags.get_status()
    # return 'do some magic!'
    return status


def enhance(body):  # noqa: E501
    """enhance

    send the request to enhance # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: EnhanceResponse
    """
    if connexion.request.is_json:
        body = EnhanceRequest.from_dict(connexion.request.get_json())  # noqa: E501
    response = metatags.enhance(body)
    #return 'do some magic!'
    return response
