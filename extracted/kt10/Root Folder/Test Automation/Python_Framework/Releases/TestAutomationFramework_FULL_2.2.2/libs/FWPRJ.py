"""
DGTO index extracted from a FWPRJ XML file.

This module parses a device-specific `.fwprj` file and builds two in-memory
collections of DGTO descriptors:

- **Standard DGTOs**: regular datapoints defined under `<DgtoCnf>/<Detail>`.
- **Phantom DGTOs**: datapoints backed by a variable address/offset, defined under
  `<PhantomDgtoCnf>/<Detail>`.

Expected XML schema excerpts:
    <DgtoCnf>
      <Detail>
        <DGTODesc>
          <Dgto>
            <Data>...</Data>      <!-- integer or 0x-prefixed hex -->
          </Dgto>
          <Desc>...</Desc>        <!-- human-readable name -->
        </DGTODesc>
        ...
      </Detail>
    </DgtoCnf>

    <PhantomDgtoCnf>
      <Detail>
        <DGTODesc>
          <Dgto>
            <Data>...</Data>
            <Address>...</Address>
            <Offset>...</Offset>
          </Dgto>
          <Desc>...</Desc>
        </DGTODesc>
        ...
      </Detail>
    </PhantomDgtoCnf>

Changelog:
[2.2.2] - 2025-11-04
  First public release of the DGTO index reader.
"""

__version__ = "2.2.2"
__author__ = "Ruggeri Nicolò"

from xml.etree import ElementTree


def convert_hex_to_dgto(dgto_hex: int) -> str:
    """
    Sw Spec : Na\n

    :param dgto_hex: represent the address of given DGTO [str]\n
    :returns: DGTO esa  the DGTO code in string format "D-G-T-O"\n

    description : Function to convert hex DGTO value (address) to DGTO code in string format "D-G-T-O"\n
    remarks : none\n
    """
    if dgto_hex < 0 or dgto_hex > 65535:
        raise Exception("ERROR! dgto_hex has to be 0 <= dgto_hex <= 65535 (16 bit unsigned)")

    D = dgto_hex & 0xF000
    D = D >> 12

    G = dgto_hex & 0x0F00
    G = G >> 8

    T = dgto_hex & 0x00E0
    T = T >> 5

    O = dgto_hex & 0x001F

    DGTO = F"{D}-{G}-{T}-{O}"

    return DGTO


class FWPRJ:
    """Parse and expose DGTO descriptors from a .fwprj file.

    Args:
        path: Path to the `.fwprj` file to parse.

    Raises:
        FileNotFoundError: If `path` does not exist.
        ElementTree.ParseError: If the XML is malformed.
        AttributeError: If expected nodes are missing from the XML structure.
        ValueError: If numeric fields contain invalid literals.

    """

    _standard_dgto_list = []
    _phantom_dgto_list = []


    def __init__(self, path: str) -> None:
        print("Starting DGTO List initialization from .fwprj file...")
        xml = ElementTree.parse(path)

        # --- Standard DGTOs ---
        dgtos_standard_list = xml.find("DgtoCnf").find("Detail")

        self._standard_dgto_list: list[dict] = []
        for dgto_standard in dgtos_standard_list.findall("DGTODesc"):
            dgto_code_hex = int(dgto_standard.find("Dgto").find("Data").text)
            dgto_code_DGTO = convert_hex_to_dgto(dgto_code_hex)
            dgto_name = dgto_standard.find("Desc").text.strip()

            self._standard_dgto_list.append(
                    {
                        "name":       dgto_name,
                        "code":       dgto_code_DGTO,
                        "code_value": dgto_code_hex,
                    }
            )

        # --- Phantom DGTOs ---
        dgtos_phantom_list = xml.find("PhantomDgtoCnf")

        if dgtos_phantom_list is not None:
            dgtos_phantom_list = dgtos_phantom_list.find("Detail")
            self._phantom_dgto_list: list[dict] = []
            for dgto_phantom in dgtos_phantom_list.findall("DGTODesc"):
                dgto_code_hex = int(dgto_phantom.find("Dgto").find("Data").text)
                dgto_code_DGTO = convert_hex_to_dgto(dgto_code_hex)
                dgto_name = dgto_phantom.find("Desc").text.strip()
                dgto_address = int(dgto_phantom.find("Dgto").find("Address").text)
                dgto_offset = int(dgto_phantom.find("Dgto").find("Offset").text)

                self._phantom_dgto_list.append(
                        {
                            "name":       dgto_name,
                            "code":       dgto_code_DGTO,
                            "code_value": dgto_code_hex,
                            "address":    dgto_address,
                            "offset":     dgto_offset,
                        }
                )
        else:
            print("No Phantom found.")


    def searchStandardDGTO(self, dgto: str) -> tuple[str, str, int]:
        """Get a standard DGTO by name or D-G-T-O code.

        Args:
            dgto: DGTO identifier, either the human-readable name or the code
                in `D-G-T-O` format.

        Returns:
            A tuple `(name, code, code_value)` if found,
            otherwise A tuple `(None, None, None)`.

            - `name` (str): Human-readable DGTO name.
            - `code` (str): D-G-T-O formatted code string.
            - `code_value` (int): Underlying integer value of the code.

        """
        for data in self._standard_dgto_list:
            if data["name"] == dgto or data["code"] == dgto:
                return data["name"], data["code"], data["code_value"]

        return None, None, None


    def searchPhantomDGTO(self, dgto: str) -> tuple[str, str, int, int, int]:
        """Get a phantom DGTO by name or D-G-T-O code.

        Args:
            dgto: DGTO identifier, either the human-readable name or the code
                in `D-G-T-O` format.

        Returns:
            A tuple `(name, code, code_value, address, offset)` if found,
            otherwise A tuple `(None, None, None, None, None)`.

            - `name` (str): Human-readable DGTO name.
            - `code` (str): D-G-T-O formatted code string.
            - `code_value` (int): Underlying integer value of the code.
            - `address` (int): Variable address for the phantom datapoint.
            - `offset` (int): Offset within the variable address.

        """
        for data in self._phantom_dgto_list:
            if data["name"] == dgto or data["code"] == dgto:
                return (
                    data["name"],
                    data["code"],
                    data["code_value"],
                    data["address"],
                    data["offset"],
                )

        return None, None, None, None, None
