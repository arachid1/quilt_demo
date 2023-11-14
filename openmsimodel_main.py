import quilt3
import pandas as pd
import os
import datetime
from pathlib import Path

from gemd import (
    MaterialTemplate,
    ProcessTemplate,
    MeasurementTemplate,
    ParameterTemplate,
    RealBounds,
)
from gemd.json import GEMDJson
from openmsimodel.science_kit.science_kit import ScienceKit
from openmsimodel.tools.structures.materials_sequence import MaterialsSequence
from openmsimodel.entity.gemd.material import Material
from openmsimodel.entity.gemd.process import Process
from openmsimodel.entity.gemd.measurement import Measurement
from openmsimodel.entity.gemd.ingredient import Ingredient
from openmsimodel.db.open_db import OpenDB
from openmsimodel.graph.open_graph import OpenGraph


def main():
    version = "2.0"
    message = "second version"
    username = "arachid1"
    data_name = "openmsimodel_example"
    pkg_name = f"{username}/{data_name}"
    version = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    pkg_dir = f"/srv/hemi01-j01/quilt_demo/registry/openmsimodel_data_registry/{data_name}_{version}.pkl"

    if os.path.exists(pkg_dir):
        with open(pkg_dir, "rb") as f:
            pkg = quilt3.Package.load(f)
    else:
        pkg = quilt3.Package()

    science_kit = ScienceKit(root=str(Path().absolute() / "openmsimodel_data"))

    # building gemd objects
    alloy_ingredient = Ingredient("Alloy Ingredient")
    polishing_process = Process("Polishing", template=ProcessTemplate("Heating"))
    polished_alloy = Material("Polished Alloy", template=MaterialTemplate("Alloy"))
    polishing_block = MaterialsSequence(
        name=f"Polishing Alloy",
        science_kit=science_kit,
        material=polished_alloy,
        ingredients=[alloy_ingredient],
        process=polishing_process,
        measurements=[],
    )
    polishing_block.link_within()

    # dumping science_kit assets
    science_kit.dump_function = GEMDJson().thin_dumps
    for asset in science_kit.assets:
        science_kit.out(asset)

    for root, dirs, files in os.walk(science_kit.root):
        for file in files:
            file_path = os.path.join(root, file)

            logical_key = os.path.relpath(file_path, science_kit.root)

            pkg.set(logical_key, file_path)
            pkg.set_meta({"my_version": version, "my_message": message})

    pkg.build(pkg_name)

    with open(pkg_dir, "wb") as f:
        pkg.dump(f)


# 'file:///srv/hemi01-j01/htmdec/birdshot/gemd/data/AAA_final/unstructured/thin/MaterialSpec_Alloy%20%28AAA07-VAM-B%29_0bfe1a77-7d31-441e-a7f3-d30e91464955_.json'

if __name__ == "__main__":
    main()
