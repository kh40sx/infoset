#!/usr/bin/env python3
"""Infoset ingest cache daemon.

Extracts agent data from cache directory files.

"""

# Standard libraries
from datetime import datetime
import os

# SQLobject stuff
from sqlalchemy import UniqueConstraint, PrimaryKeyConstraint, func, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import BIGINT, TIMESTAMP, INTEGER
from sqlalchemy.dialects.mysql import FLOAT, VARCHAR
from sqlalchemy import Table, Column, create_engine
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, backref

BASE = declarative_base()

# Infoset libraries
from infoset.cache import cache
from infoset.utils import jm_configuration
from infoset.utils import log


class Data(BASE):
    """Class defining the iset_data table of the database."""

    __tablename__ = 'iset_data'
    __table_args__ = (
        PrimaryKeyConstraint(
            'idx_datapoint', 'timestamp'),
        {
            'mysql_engine': 'InnoDB'
        }
        )

    idx_datapoint = Column(
        BIGINT(unsigned=True), ForeignKey('iset_datapoint.idx'),
        nullable=False, server_default='1')

    idx_agent = Column(
        BIGINT(unsigned=True), ForeignKey('iset_agent.idx'),
        nullable=False, server_default='1')

    timestamp = Column(BIGINT(unsigned=True), nullable=False, default='1')

    value = Column(FLOAT, default=None)

    enabled = Column(INTEGER(unsigned=True), server_default='1')


class Agent(BASE):
    """Class defining the iset_agent table of the database."""

    __tablename__ = 'iset_agent'
    __table_args__ = {
        'mysql_engine': 'InnoDB'
    }

    idx = Column(
        BIGINT(unsigned=True), primary_key=True,
        autoincrement=True, nullable=False)

    id = Column(VARCHAR(64), unique=True, nullable=True, default=None)

    name = Column(VARCHAR(64), nullable=True, default=None)

    description = Column(VARCHAR(64), nullable=True, default=None)

    hostname = Column(VARCHAR(75), nullable=True, default=None)

    enabled = Column(INTEGER(unsigned=True), server_default='1')

    last_timestamp = Column(
        BIGINT(unsigned=True), nullable=False, server_default='0')

    ts_modified = Column(
        TIMESTAMP, server_default=text(
            'CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'),)

    ts_created = Column(
        TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))


class DataPoint(BASE):
    """Class defining the iset_datapoint table of the database."""

    __tablename__ = 'iset_datapoint'
    __table_args__ = (
        UniqueConstraint('idx', 'idx_agent'),
        {
            'mysql_engine': 'InnoDB'
        }
        )

    idx = Column(
        BIGINT(unsigned=True), primary_key=True,
        autoincrement=True, nullable=False)

    idx_agent = Column(
        BIGINT(unsigned=True), ForeignKey('iset_agent.idx'),
        nullable=False, server_default='1')

    id = Column(VARCHAR(64), unique=True, nullable=True, default=None)

    agent_label = Column(VARCHAR(64), nullable=True, default=None)

    agent_source = Column(VARCHAR(128), nullable=True, default=None)

    enabled = Column(INTEGER(unsigned=True), server_default='1')

    uncharted_value = Column(VARCHAR(128), nullable=True, default=None)

    base_type = Column(INTEGER(unsigned=True), server_default='1')

    value = Column(FLOAT, server_default='1')

    last_timestamp = Column(
        BIGINT(unsigned=True), nullable=False, server_default='0')

    ts_modified = Column(
        TIMESTAMP, server_default=text(
            'CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'),)

    ts_created = Column(
        TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))


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

    # Create tables
    db_uri = ('mysql+pymysql://%s:%s@%s/%s') % (
        config.db_username(), config.db_password(),
        config.db_hostname(), config.db_name())
    print(db_uri)
    engine = create_engine(db_uri, echo=True)
    BASE.metadata.create_all(engine)


if __name__ == "__main__":
    main()
