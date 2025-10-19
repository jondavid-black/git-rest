import os


LICENSE_URLS = {
    "MIT": "https://raw.githubusercontent.com/spdx/license-list-data/refs/heads/main/text/MIT.txt",
    "Apache-2.0": "https://raw.githubusercontent.com/spdx/license-list-data/refs/heads/main/text/Apache-2.0.txt",
    "GPL-3.0": "https://raw.githubusercontent.com/spdx/license-list-data/refs/heads/main/text/GPL-3.0-only.txt",
    "BSD-3-Clause": "https://raw.githubusercontent.com/spdx/license-list-data/refs/heads/main/text/BSD-3-Clause.txt",
    "MPL-2.0": "https://raw.githubusercontent.com/spdx/license-list-data/refs/heads/main/text/MPL-2.0.txt",
    "CC-BY-4.0": "https://raw.githubusercontent.com/spdx/license-list-data/refs/heads/main/text/CC-BY-4.0.txt",
}

class LicenseNotFoundError(Exception):
    pass


import requests

def get_license_text(license_name: str) -> str:
    """Fetch the official license text for a supported license name from SPDX GitHub."""
    key = license_name.strip().upper().replace(" ", "-")
    for known, url in LICENSE_URLS.items():
        if key == known.upper():
            try:
                response = requests.get(url, timeout=5)
                response.raise_for_status()
                return response.text
            except Exception as e:
                raise LicenseNotFoundError(f"Could not fetch license '{license_name}': {e}")
    raise LicenseNotFoundError(f"License '{license_name}' is not supported.")
