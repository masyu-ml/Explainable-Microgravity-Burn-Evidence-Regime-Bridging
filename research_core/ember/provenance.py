from __future__ import annotations
from typing import Any, Dict


def provenance(source_id: str, level: str, claim: str, url: str, note: str = "") -> Dict[str, Any]:
    return {
        "source_id": source_id,
        "level": level,
        "claim": claim,
        "url": url,
        "note": note,
    }


THICK_PMMA_SOURCE = provenance(
    "NASA_NTRS_20200000557",
    "NASA_OBSERVED",
    "10-mm thick PMMA concurrent flame-spread tests at 40-100 kPa and 0.2 m/s in 1-g were compared with Saffire II microgravity; mixed-convection scaling was developed.",
    "https://ntrs.nasa.gov/citations/20200000557",
)

ROD_BLOWOFF_SOURCE = provenance(
    "NASA_NTRS_20170006615",
    "NASA_OBSERVED",
    "PMMA rod blowoff in 1-g was compared with BASS-II microgravity; blockage, normalized thermal length, and buoyant stretch corrections were reported.",
    "https://ntrs.nasa.gov/citations/20170006615",
)

BASS_II_SOURCE = provenance(
    "NASA_PSI_25",
    "NASA_OBSERVED",
    "BASS-II is an ISS microgravity combustion investigation with 130 experimental-table records and associated files; variables include flow, oxygen, material, and geometry.",
    "https://psi.nasa.gov/physci/repo/data/investigations/PSI-25",
)

LUCI_SOURCE = provenance(
    "NASA_NTRS_20250010653",
    "NASA_OBSERVED",
    "LUCI performed extended-duration simulated lunar-gravity burns of PMMA and SIBAL on a rotating sounding rocket.",
    "https://ntrs.nasa.gov/citations/20250010653",
)

LUNAR_TEST_SOURCE = provenance(
    "NASA_NTRS_20250002114",
    "NASA_OBSERVED",
    "NASA is developing a lunar-gravity material flammability test method using partial-gravity testing and Damkohler-number reasoning.",
    "https://ntrs.nasa.gov/citations/20250002114",
)
