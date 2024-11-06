#!/usr/bin/env python3.9
# coding:utf-8
# Copyright (C) 2024 All rights reserved.
# FILENAME:    ~~/src/acqua/types/jsonrpc_response.py
# VERSION:     0.1.1
# CREATED:     2024-11-07 02:00
# AUTHOR:      Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from typing import Literal

### Third-party packages ###
from pydantic import BaseModel, StrictInt, StrictStr


class JsonrpcResponse(BaseModel):
  jsonrpc: Literal["2.0"]
  id: StrictInt | StrictStr
  result: StrictStr


__all__ = ("JsonrpcResponse",)
