#!/usr/bin/env python3.9
# coding:utf-8
# Copyright (C) 2024 All rights reserved.
# FILENAME:    ~~/src/acqua/configs.py
# VERSION:     0.1.1
# CREATED:     2024-10-24 14:29
# AUTHOR:      Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from pathlib import Path
from typing import Any, Dict, Optional

### Standard packages ###
from pydantic import TypeAdapter
from yaml import Loader, load

### Local modules ###
from acqua.types import Build, BuildEnum, Service, ServiceName

BUILDS: Dict[BuildEnum, Build]
NETWORK: str
SERVICES: Dict[ServiceName, Service]


file_path: Path = Path(__file__).resolve()
with open(str(file_path).replace("configs.py", "schemas.yml"), "rb") as stream:
  schema: Optional[Dict[str, Any]] = load(stream, Loader=Loader)
  if schema:
    BUILDS = TypeAdapter(Dict[BuildEnum, Build]).validate_python(schema["builds"])
    NETWORK = schema.get("network", "acqua")
    SERVICES = TypeAdapter(Dict[ServiceName, Service]).validate_python(schema["services"])

__all__ = ("BUILDS", "NETWORK", "SERVICES")
