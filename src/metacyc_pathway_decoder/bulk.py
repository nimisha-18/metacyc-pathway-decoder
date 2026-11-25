import time
from .decoder import get_pathway_name

def get_pathway_names(pathway_ids, session, delay=1, verbose=True):
    """
    Retrieve readable names for multiple MetaCyc pathway IDs.

    Parameters
    ----------
    pathway_ids : iterable
        Collection of MetaCyc pathway identifiers.

    session : requests.Session
        Authenticated BioCyc session.

    delay : float
        Pause between requests, in seconds. Defaults to 1.

    Returns
    -------
    list
        List of dictionaries containing pathway IDs, names, statuses,
        and error messages.
    """
    if not isinstance(delay, (int, float)) or isinstance(delay, bool):
        raise TypeError("Delay must be a numeric value.")

    if delay < 0:
        raise ValueError("Delay cannot be negative.")
        
    results = []

    for index, pathway_id in enumerate(pathway_ids):

        try:
            name = get_pathway_name(pathway_id, session)

            results.append({
                "Pathway_ID": pathway_id,
                "Pathway_Name": name,
                "Status": "success" if name else "name_not_found",
                "Error": None
            })

        except Exception as error:

            results.append({
                "Pathway_ID": pathway_id,
                "Pathway_Name": None,
                "Status": "failed",
                "Error": str(error)
            })

        if verbose:
            print(f"Processed {index + 1}/{len(pathway_ids)}: {pathway_id}")

        if index < len(pathway_ids) - 1:
            time.sleep(delay)

    return results