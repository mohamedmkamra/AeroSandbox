import aerosandbox.numpy as np
from aerosandbox.geometry.airplane import Airplane
from aerosandbox.geometry.wing import Wing, WingXSec
from aerosandbox.geometry.fuselage import Fuselage, FuselageXSec
from aerosandbox.geometry.propulsor import Propulsor
from aerosandbox.geometry.airfoil.airfoil import Airfoil
from aerosandbox.geometry.airfoil.kulfan_airfoil import KulfanAirfoil
from textwrap import indent, dedent

# noindent

_openvsp_version = "3.36.0"


def wrap_script(
    script: str,
    set_geom_draw_type_to_shade: bool = True,
) -> str:
    """
    Wraps the internal parts of a VSPScript file with a main() function.

    Example:
        >>> print(wrap_script("hello\nworld"))
        // This file was automatically generated by AeroSandbox 4.2.0
        // using syntax tested on OpenVSP 3.36.0.

        void main()
        {
            hello
            world
        }

    Args:
        script: The script to wrap.

    Returns: The script, wrapped with a main() function.

    """
    script = (
        script
        + """\
    
//==== Check For API Errors ====//
while ( GetNumTotalErrors() > 0 )
{
    ErrorObj err = PopLastError();
    Print( err.GetErrorString() );
}
"""
    )

    if set_geom_draw_type_to_shade:
        script = (
            script
            + """\

{
    array<string> @geomids = FindGeoms();
    
    for (uint i = 0; i < geomids.length(); i++)
    {
        SetGeomDrawType( geomids[i], GEOM_DRAW_SHADE );
    }
}
        
"""
        )

    import aerosandbox as asb

    return f"""\
// This *.vspscript file was automatically generated by AeroSandbox {asb.__version__} 
// using syntax tested on OpenVSP {_openvsp_version}.
// To run this script, open OpenVSP and go to File -> Run Script...

void main()
{{
{indent(script, "    ")}
}}
"""


if __name__ == "__main__":

    print(wrap_script("hello\nworld"))  # Expected:
    # // This file was automatically generated by AeroSandbox 4.2.0
    # // using syntax tested on OpenVSP 3.36.0.
    #
    # void main()
    # {
    #     hello
    #     world
    #
    #
    #     //==== Check For API Errors ====//
    #     while ( GetNumTotalErrors() > 0 )
    #     {
    #         ErrorObj err = PopLastError();
    #         Print( err.GetErrorString() );
    #     }
    #
