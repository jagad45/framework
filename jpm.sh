#!/usr/bin/env bash
pyinstaller --onefile --name "jagad-console" --collect-submodules "jagad" \
    --hidden-import "requests" --hidden-import "pathlib" --hidden-import "rich" \
    --add-data "config.json:json" \
    jagad-console
cp -rf config.json dist/
cp -rf system dist
