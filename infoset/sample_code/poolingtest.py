#!/usr/bin/env python3
"""Infoset ingest cache daemon.

Extracts agent data from cache directory files.

"""

# Standard libraries
from datetime import datetime
import os

# SQLobject stuff
from sqlalchemy import UniqueConstraint, PrimaryKeyConstraint, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import BIGINT, DATETIME, INTEGER
from sqlalchemy.dialects.mysql import FLOAT, VARBINARY
from sqlalchemy import Table, Column, create_engine
from sqlalchemy import Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, backref
Base = declarative_base()

# Infoset libraries
from infoset.cache import cache
from infoset.utils import jm_configuration
from infoset.utils import log


class Data(Base):
    """Class defining the iset_data table of the database."""

    __tablename__ = 'iset_data'
    __table_args__ = (
        PrimaryKeyConstraint(
            'idx_datapoint', 'idx_agent'),
        {
            'mysql_engine': 'InnoDB',
            'mysql_charset': 'utf8mb48',
        }
        )

    idx_datapoint = Column(BIGINT(unsigned=True), nullable=False, default=1)
    idx_agent = Column(BIGINT(unsigned=True), nullable=False, default=1)
    timestamp = Column(BIGINT(unsigned=True), nullable=False, default=1)
    value = Column(FLOAT, default=1)
    enabled = Column(INTEGER(unsigned=True), default=1)


class Agent(Base):
    """Class defining the iset_agent table of the database."""

    __tablename__ = 'iset_agent'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb48'
    }

    idx = Column(
        BIGINT(unsigned=True), primary_key=True,
        autoincrement=True, nullable=False, default=1)
    uid = Column(VARBINARY(512), unique=True, nullable=True, default=None)
    name = Column(VARBINARY(512), nullable=True, default=None)
    description = Column(VARBINARY(512), nullable=True, default=None)
    hostname = Column(VARBINARY(512), nullable=True, default=None)
    enabled = Column(INTEGER(unsigned=True), default=1)
    last_timestamp = Column(BIGINT(unsigned=True), nullable=False, default=1)
    ts_modified = Column(DateTime, onupdate=func.utc_timestamp())
    ts_created = Column(DateTime, default=datetime.utcnow)


class DataPoint(Base):
    """Class defining the iset_datapoint table of the database."""

    __tablename__ = 'iset_datapoint'
    __table_args__ = (
        UniqueConstraint('idx', 'idx_agent'),
        {
            'mysql_engine': 'InnoDB',
            'mysql_charset': 'utf8mb48',
        }
        )

    idx = Column(
        BIGINT(unsigned=True), primary_key=True,
        autoincrement=True, nullable=False, default=1)
    idx_agent = Column(BIGINT(unsigned=True), nullable=False, default=1)
    did = Column(VARBINARY(512), unique=True, nullable=True, default=None)
    agent_label = Column(VARBINARY(512), nullable=True, default=None)
    agent_source = Column(VARBINARY(512), nullable=True, default=None)
    enabled = Column(INTEGER(unsigned=True), default=1)
    uncharted_value = Column(VARBINARY(512), nullable=True, default=None)
    base_type = Column(INTEGER(unsigned=True), default=1)
    value = Column(FLOAT, default=1)
    last_timestamp = Column(BIGINT(unsigned=True), nullable=False, default=1)
    ts_modified = Column(DateTime, onupdate=func.utc_timestamp())
    ts_created = Column(DateTime, default=datetime.utcnow)


def main():
    """Process agent data.

    Args:
        None

    Returns:
        None

    """
    # Get configuration
    log.check_environment()

    config_directory = os.environ['INFOSET_CONFIGDIR']
    config = jm_configuration.ConfigServer(config_directory)


if __name__ == "__main__":
    main()
