#!/usr/bin/env python3
"""Infoset ORM classes.

Manages connection pooling among other things.

"""

# SQLobject stuff
from sqlalchemy import UniqueConstraint, PrimaryKeyConstraint, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import BIGINT, TIMESTAMP, INTEGER
from sqlalchemy.dialects.mysql import FLOAT, VARCHAR
from sqlalchemy import Column
from sqlalchemy import ForeignKey

BASE = declarative_base()


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


class Datapoint(BASE):
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

    last_timestamp = Column(
        BIGINT(unsigned=True), nullable=False, server_default='0')

    ts_modified = Column(
        TIMESTAMP, server_default=text(
            'CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'),)

    ts_created = Column(
        TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
