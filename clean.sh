#!/bin/bash
TO_CLEAN=(
    "__pycache__/"
    "env/"
    "build/"
    "src/Pyamp.egg-info/"
)
for item in "${TO_CLEAN[@]}"; do
    rm -rf "$item"
done
