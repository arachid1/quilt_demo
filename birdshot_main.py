import quilt3
import pandas as pd
import os
from pathlib import Path
from gemd import MaterialRun


def main():
    # quilt3.config("http://localhost:3000")
    username = "arachid1"
    data_name = "birdshot"
    pkg_name = f"{username}/{data_name}"
    pkg_dir = f"/srv/hemi01-j01/quilt_demo/registry/{data_name}.pkl"
    with open(pkg_dir, "rb") as f:
        pkg = quilt3.Package.load(f)
    parent_physical_path = (
        "/srv/hemi01-j01/htmdec/birdshot/gemd/data/AAA_final/unstructured/thin"
    )

    # Loop through each file in the folder
    for root, dirs, files in os.walk(parent_physical_path):
        for file in files:
            # Construct the full file path
            file_path = os.path.join(root, file)

            # Create a logical key based on the file structure
            logical_key = os.path.relpath(file_path, parent_physical_path)

            # Add the file to the package
            pkg.set(logical_key, file_path)

    pkg.build(pkg_name)

    # with open(pkg_dir, "wb") as f:
    #     pkg.dump(f)

    # with open(pkg_dir, "rb") as f:
    #     loaded_pkg = quilt3.Package.load(f)

    # data = loaded_pkg[logical_key].get()
    # print(data)


# 'file:///srv/hemi01-j01/htmdec/birdshot/gemd/data/AAA_final/unstructured/thin/MaterialSpec_Alloy%20%28AAA07-VAM-B%29_0bfe1a77-7d31-441e-a7f3-d30e91464955_.json'

if __name__ == "__main__":
    main()
