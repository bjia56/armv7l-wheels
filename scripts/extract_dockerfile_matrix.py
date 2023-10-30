#!/usr/bin/env python3

import json
import os
import yaml


BUILDSPEC_FILE = "build.yaml"

# assume we are running within the package dir
with open(BUILDSPEC_FILE, "r") as file:
    buildspec = yaml.safe_load(file)

out = []

if isinstance(buildspec.get("source"), str):
    out.append({
        "key": 0,
        "file": buildspec["source"],
        "common": False
    })
else:
    idx = 1
    for source in buildspec.get("source", []):
        if isinstance(source, str):
            out.append({
                "key": idx,
                "file": source,
                "common": False
            })
        else:
            out.append({
                "key": idx,
                **source
            })

        idx += 1


print(json.dumps(out))