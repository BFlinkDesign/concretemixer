#!/bin/bash
# Export MudMixer auger to STL format
# Requires OpenSCAD installed

SCAD_FILE="mudmixer_auger.scad"
STL_FILE="mudmixer_auger.stl"

# Generate with high quality
openscad -o $STL_FILE -D '$fn=200' $SCAD_FILE

echo "Exported: $STL_FILE"
echo "Dimensions: 2.5" OD x 36.0" length"
