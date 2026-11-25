import xml.etree.ElementTree as ET


def get_pathway_name(pathway_id, session):
    """
    Retrieve the readable name of a MetaCyc pathway.

    Parameters
    ----------
    pathway_id : str
        MetaCyc pathway identifier, e.g. 'PWY-3781'.

    session : requests.Session
        Authenticated BioCyc requests session.

    Returns
    -------
    str or None
        Retrieved pathway name, or None if no name is found.
    """

    response = session.get(
        "https://websvc.biocyc.org/getxml",
        params={
            "id": f"META:{pathway_id}",
            "detail": "full"
        },
        timeout=30
    )

    response.raise_for_status()

    content_type = response.headers.get("Content-Type", "")

    if "xml" not in content_type.lower():
        
        if "account-required" in response.url.lower():
            raise PermissionError(
            "BioCyc authentication required or session expired. "
            "Please authenticate your session again."
            )

        raise ValueError(
            f"Expected XML response, received {content_type!r}. "
            f"Response URL: {response.url}"
        )

    try:
        root = ET.fromstring(response.content)

    except ET.ParseError as error:
        raise ValueError(
            f"Invalid XML response for pathway {pathway_id}"
        ) from error

    pathway = root.find(".//Pathway")

    if pathway is None:
        return None

    common_name = pathway.find("common-name")

    if common_name is not None:
        return "".join(common_name.itertext()).strip()

    return None
