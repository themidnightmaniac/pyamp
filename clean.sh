#!/bin/bash
TO_CLEAN=(
    "env/"
    "build/"
    "src/Pyamp.egg-info/"
)
TO_CLEAN+=( $(find . -name __pycache__) )
for item in "${TO_CLEAN[@]}"; do
    rm -rf "$item"
done
