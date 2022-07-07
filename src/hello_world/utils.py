from typing import Union, Optional, Dict


def Response(
    status_code: Optional[int] = 200,
    body: Optional[Union[str, bytes, None]] = None,
    content_type: Optional[str] = "application/json",
    headers: Optional[Dict] = {},
    isBase64Encoded: Optional[bool] = False,
) -> Dict:
    """_summary_

    Args:
        status_code: int
            Http status code, example 200
        content_type: str
            Optionally set the Content-Type header, example "application/json". Note this will be merged into any
            provided http headers
        body: Union[str, bytes, None]
            Optionally set the response body. Note: bytes body will be automatically base64 encoded
        headers: dict
            Optionally set specific http headers. Setting "Content-Type" hear would override the `content_type` value.

    Returns:
        Dict: _description_
    """
    headers.update({"content-type": content_type})

    return {
        "statusCode": status_code,
        "body": body,
        "headers": headers,
        "isBase64Encoded": isBase64Encoded,
    }