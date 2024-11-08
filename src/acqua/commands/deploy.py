#!/usr/bin/env python3.9
# coding:utf-8
# Copyright (C) 2024 All rights reserved.
# FILENAME:    ~~/src/acqua/commands/deploy.py
# VERSION:     0.1.2
# CREATED:     2024-10-24 14:29
# AUTHOR:      Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from typing import Dict, List

### Third-party packages ###
from click import command, option
from docker import DockerClient, from_env
from docker.errors import APIError, DockerException
from rich import print as rich_print
from rich.progress import track

### Local modules ###
from acqua.configs import NETWORK, SERVICES
from acqua.types import Chain, Service, ServiceName


@command
@option("--devnet", cls=Chain, is_flag=True, type=bool, variants=("mainnet", "testnet"))
@option("--mainnet", cls=Chain, is_flag=True, type=bool, variants=("devnet", "testnet"))
@option("--testnet", cls=Chain, is_flag=True, type=bool, variants=("devnet", "mainnet"))
def deploy(
  devnet: bool,
  mainnet: bool,
  testnet: bool,
) -> None:
  """Deploy cluster."""
  client: DockerClient
  try:
    client = from_env()
    if not client.ping():
      raise DockerException
  except DockerException:
    rich_print("[red bold]Unable to connect to docker daemon.")
    return

  ### Setup Node Network ###
  node_selector: Dict[ServiceName, bool] = {
    "acqua-sui": mainnet,
    "acqua-sui-devnet": devnet,
    "acqua-sui-testnet": testnet,
  }
  node_name: ServiceName = "acqua-sui"
  try:
    node_name = next(filter(lambda value: value[1], node_selector.items()))[0]
  except StopIteration:
    pass

  ### Setup Cluster Network ###
  try:
    client.networks.create(NETWORK, check_duplicate=True)
  except APIError:
    pass

  ### Launch middlewares ###
  middleware_selector = {"acqua-postgres": True}
  middlewares: Dict[ServiceName, Service] = {
    key: value
    for key, value in SERVICES.items()
    if value.service_type == "middleware"
    if middleware_selector[key]
  }
  for name, middleware in track(middlewares.items(), f"Deploy middleware services".ljust(42)):
    flags: List[str] = list(middleware.command.values())
    environment: List[str] = middleware.env_vars
    ports: Dict[str, int] = {p.split(":")[0]: int(p.split(":")[1]) for p in middleware.ports}
    client.containers.run(
      middleware.image,
      command=flags,
      detach=True,
      environment=environment,
      name=name,
      network=NETWORK,
      ports=ports,  # type: ignore
    )


  ### Launch Node Daemon ###
  node: Service = SERVICES[node_name]
  for _ in track(range(1), f"Deploy { node_name }".ljust(42)):
    flags: List[str] = list(node.command.values())
    ports: Dict[str, int] = {port.split(":")[0]: int(port.split(":")[1]) for port in node.ports}
    client.containers.run(
      node.image,
      command=flags,
      detach=True,
      environment=node.env_vars,
      name=node_name,
      network=NETWORK,
      ports=ports,  # type: ignore
    )



__all__ = ("deploy",)
