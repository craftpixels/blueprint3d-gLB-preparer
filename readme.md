# Blueprint3d GLB preparer

## Overview
The open source Blueprint3D JS floor planner requires GLB models to be prepared in a certain way before loading into the scene. Your meshes have to be 1 unit and aligned to the coordinate center to show up as a 1cm object within the 3D scene. This Blender add-on script automates preparation of your GLB models for use within Blueprint3D app.

## Features
- Imports a GLB file into Blender.
- Adjusts the position and scale of the mesh to center it.
- Computes the bounding box and center of the mesh.
- Exports the modified mesh as a GLB file.

## Prerequisites
Before using this script, ensure you have:
- Blender installed (Version 3.x  recommended)
- Python 3 installed (bundled with Blender)
- Basic understanding of Blender's scripting environment

## Screenshot


## Usage
Run the script from Blender’s scripting editor or via command line:
```sh
blender --background --python script.py -- "path/to/input.glb" 200 "output.glb"
```
### Parameters:
- `path/to/input.glb` - Path to the input GLB model.
- `200` - Desired width of the model after scaling.
- `output.glb` - Path to the exported GLB model.

## How It Works
1. Deletes all existing objects in the scene.
2. Imports the specified GLB model.
3. Identifies all mesh components and resets transformations.
4. Computes the bounding box dimensions and centralizes the object.
5. Applies transformation adjustments to ensure proper centering.
6. Exports the processed model as a GLB file.

## Customization
- Modify `data` dictionary to specify custom transformations.
- Adjust `scaleRatio` in `constructTransformationMatrix` to control scaling behavior.


## Disclaimer
We were the official commercial implementation partner for the blueprint3D Js repo until the year 2024. We still develop & support 3D floor planners based on BP3D. Contact us on madz@craftpixels.in for more details.
