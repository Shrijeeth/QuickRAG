# pylint: disable=unused-argument

import logging

from fastapi import FastAPI


async def startup(app: FastAPI):
    logging.info("Starting application lifecycle")


async def shutdown(app: FastAPI):
    logging.info("Shutting down application lifecycle")


async def lifespan(app: FastAPI):
    await startup(app)
    yield
    await shutdown(app)
