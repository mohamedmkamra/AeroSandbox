import aerosandbox as asb
import aerosandbox.numpy as np
import pytest

wing_airfoil = asb.Airfoil("naca0010")# asb.Airfoil("sd7037")
tail_airfoil = asb.Airfoil("naca0010")

### Define the 3D geometry you want to analyze/optimize.
# Here, all distances are in meters and all angles are in degrees.
airplane = asb.Airplane(
    name="Peter's Glider",
    xyz_ref=[0, 0, 0],  # CG location
    wings=[
        asb.Wing(
            name="Main Wing",
            symmetric=True,  # Should this wing be mirrored across the XZ plane?
            xsecs=[  # The wing's cross ("X") sections
                asb.WingXSec(  # Root
                    xyz_le=[0, 0, 0],  # Coordinates of the XSec's leading edge, relative to the wing's leading edge.
                    chord=0.18,
                    twist=0,  # degrees
                    airfoil=wing_airfoil,  # Airfoils are blended between a given XSec and the next one.
                ),
                asb.WingXSec(  # Mid
                    xyz_le=[0.01, 0.5, 0],
                    chord=0.16,
                    twist=0,
                    airfoil=wing_airfoil,
                ),
                asb.WingXSec(  # Tip
                    xyz_le=[0.08, 1, 0.1],
                    chord=0.08,
                    twist=-0,
                    airfoil=wing_airfoil,
                ),
            ]
        ),
        asb.Wing(
            name="Horizontal Stabilizer",
            symmetric=True,
            xsecs=[
                asb.WingXSec(  # root
                    xyz_le=[0, 0, 0],
                    chord=0.1,
                    twist=-10,
                    airfoil=tail_airfoil,
                ),
                asb.WingXSec(  # tip
                    xyz_le=[0.02, 0.17, 0],
                    chord=0.08,
                    twist=-10,
                    airfoil=tail_airfoil
                )
            ]
        ).translate([0.6, 0, 0.06]),
        asb.Wing(
            name="Vertical Stabilizer",
            symmetric=False,
            xsecs=[
                asb.WingXSec(
                    xyz_le=[0, 0, 0],
                    chord=0.1,
                    twist=0,
                    airfoil=tail_airfoil,
                ),
                asb.WingXSec(
                    xyz_le=[0.04, 0, 0.15],
                    chord=0.06,
                    twist=0,
                    airfoil=tail_airfoil
                )
            ]
        ).translate([0.6, 0, 0.07])
    ],
    fuselages=[
        asb.Fuselage(
            name="Fuselage",
            xsecs=[
                asb.FuselageXSec(
                    xyz_c=[xi, 0, 0],
                    radius=1 * asb.Airfoil("dae51").local_thickness(x_over_c=xi)
                )
                for xi in np.cosspace(0, 1, 30)
            ]
        )
    ]
)

for i, wing in enumerate(airplane.wings):
    for j, xsec in enumerate(wing.xsecs):
        af = xsec.airfoil
        af.generate_polars(
            cache_filename=f"cache/{af.name}.json",
            xfoil_kwargs=dict(
                xfoil_repanel="naca" in af.name.lower()
            )
        )
        airplane.wings[i].xsecs[j].airfoil = af

op_point = asb.OperatingPoint(
    velocity=100,
    alpha=5,
    beta=0,
)

ab = asb.AeroBuildup(
    airplane,
    op_point,
).run_with_stability_derivatives()

# from pprint import pprint
#
# pprint(ab)

av = asb.AVL(
    airplane,
    op_point
).run()

vl = asb.VortexLatticeMethod(
    airplane,
    op_point
).run()

keys = set()
keys.update(ab.keys())
keys.update(av.keys())
keys = list(keys)
keys.sort()


def println(*data):
    print(" | ".join([
        d.ljust(10) if isinstance(d, str) else f"{d:10.4g}"
        for d in data
    ]))


println(
    'Output',
    'AeroBuild',
    'AVL',
    'VLM',
    'AB & AVL Significantly Different?'
)
print("-" * 80)
for k in keys:
    try:
        println(
            k,
            ab[k],
            av[k],
            vl[k] if k in vl.keys() else '-',
            '' if ab[k] == pytest.approx(av[k], rel=0.5, abs=0.01) else '*'
        )

    except (KeyError, TypeError):
        pass