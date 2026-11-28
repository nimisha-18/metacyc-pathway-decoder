# MetaCyc Pathway Decoder

MetaCyc Pathway Decoder is a Python package designed to retrieve readable names for MetaCyc pathway identifiers using the BioCyc Web Services API. It simplifies the process of translating pathway IDs into their corresponding names, making pathway annotation tables easier to interpret and use in downstream analyses.

## Motivation (Yeah, I was suffering!)

Retrieving pathway information can involve additional setup, including access to BioCyc services and the installation of Pathway Tools. However, researchers working with functional profiling and metagenomic datasets may only need the readable names corresponding to pathway identifiers.

MetaCyc Pathway Decoder aims to provide a lightweight solution for this specific requirement, without requiring users to install the full Pathway Tools software.

## Features

1. Retrieve readable names for individual MetaCyc pathway IDs.
2. Access pathway information through the BioCyc Web Services API.
3. Support authenticated BioCyc sessions.
4. Handle unsuccessful API requests and invalid pathway identifiers.
5. Preserve pathway identifiers alongside their retrieved names.
6. Provide a foundation for bulk pathway-name retrieval.

## Requirements

- Python 3.10 or later.
- A registered BioCyc account with access to the relevant web service.
- Internet connectivity.

**Authentication requirements:** Users must have a registered BioCyc account to establish an authenticated session with the BioCyc Web Services API. Account registration and access are subject to BioCyc's requirements.

Credentials should be entered locally and should never be hardcoded into scripts, committed to repositories, or shared. The package does not store user credentials.

## Installation

`pip install metacyc-pathway-decoder`

*Note: It's on PyPI now.*

## Authentication

Both package functions require an authenticated `requests.Session` object.

Users can establish an authenticated session using their own BioCyc credentials:

`import requests`
`import getpass`

`session = requests.Session()`

`email = input("BioCyc registered email: ")`
`password = getpass.getpass("BioCyc password: ")`

`login_url = "https://websvc.biocyc.org/credentials/login/"`

`login_response = session.post(
    login_url,
    data={
        "email": email,
        "password": password
    },
    timeout=30
)`

`login_response.raise_for_status()`

The authenticated session can then be passed to the package functions.

## Basic Usage

1. Retrieve a single pathway name

`from metacyc_pathway_decoder import get_pathway_name`

`pathway_name = get_pathway_name(
    "PWY-3781",
    session
)`
`print(pathway_name)`

2. Retrieve multiple pathway names

`from metacyc_pathway_decoder import get_pathway_names`

`pathway_ids = [
    "PWY-3781",
    "PWY-5973",
    "PWY-7219"
]`

`results = get_pathway_names(
    pathway_ids,
    session,
    delay=1,
    verbose=True
)`

`print(results)`

The bulk retrieval function returns a list of dictionaries containing:

- `Pathway_ID`: Original pathway identifier.
- `Pathway_Name`: Retrieved pathway name or `None` if unavailable.
- `Status`: Retrieval status (`success`, `name_not_found` or `failed`).
- `Error`: Error message, if retrieval failed.

The `delay` parameter controls the pause between successive API requests, while verbose enables or disables progress reporting.

## Function Inputs

### `get_pathway_name()`

| Parameter | Description |
| -------- | -------- |
| pathway_id | MetaCyc pathway identifier supplied as a string|
| session | An authenticated requests.Session object |

### `get_pathway_names()`

| Parameter | Description |
| -------- | -------- |
| pathway_ids | Collection of MetaCyc pathway identifiers |
| session | An authenticated requests.Session object |
| delay | Pause between successive requests, in seconds. Defaults to 1 |
| verbose | Enables or disables progress reporting. Defaults to True |

## Output and Error Handling

### Single pathway retrieval (get_pathway_name):
- Returns the corresponding pathway name as a string.
- Returns None if the pathway or its common name is not found.
- Raises exceptions for unsuccessful HTTP requests, authentication issues, and invalid XML responses.

### Bulk pathway retrieval (get_pathway_names):
- Returns a list of dictionaries containing pathway IDs, retrieved names, statuses, and error messages.
- Preserves individual results even when some pathway requests fail.
- Allows users to identify unsuccessful requests without losing the remaining results.

## Dependencies

- requests

The package also uses Python standard-library modules for XML parsing and request handling.

## License

MIT License