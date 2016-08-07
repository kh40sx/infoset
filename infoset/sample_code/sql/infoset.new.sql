# Create the database from scratch
drop database infoset;
create database infoset
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_general_ci;
USE infoset;

# ----------------------------------------------------------------------

# Create table for collected data
CREATE TABLE iset_data (
  idx_datapoint BIGINT UNSIGNED NOT NULL DEFAULT 1,
  idx_agent BIGINT UNSIGNED NOT NULL DEFAULT 1,
  timestamp BIGINT UNSIGNED NOT NULL,
  value FLOAT DEFAULT NULL,
  enabled INTEGER UNSIGNED DEFAULT 1,
  PRIMARY KEY (idx_datapoint, timestamp)
) ENGINE=InnoDB COMMENT='Data Table' AUTO_INCREMENT=1 ;

# ----------------------------------------------------------------------

# Create table for agents
CREATE TABLE iset_agent (
  idx BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  id VARBINARY(512),
  name VARBINARY(512) DEFAULT NULL,
  description VARBINARY(512) DEFAULT NULL,
  hostname VARBINARY(512) DEFAULT NULL,
  enabled INTEGER UNSIGNED DEFAULT 1,
  last_timestamp BIGINT UNSIGNED DEFAULT 0,
  ts_modified DATETIME NULL ON UPDATE CURRENT_TIMESTAMP,
  ts_created DATETIME DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY (id),
  PRIMARY KEY (idx)
) ENGINE=InnoDB COMMENT='Agent Table' AUTO_INCREMENT=1 ;

# Insert the very first agent, the infoset server
INSERT INTO iset_agent (id, name, hostname) VALUES ("INFOSET", "INFOSET", "INFOSET")

# ----------------------------------------------------------------------

# Create table for datapoints
CREATE TABLE iset_datapoint (
  idx BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  idx_agent BIGINT UNSIGNED NOT NULL DEFAULT 1,
  id VARBINARY(512),
  agent_label VARBINARY(512) DEFAULT NULL,
  agent_source VARBINARY(512) DEFAULT NULL,
  enabled INTEGER UNSIGNED DEFAULT 1,
  uncharted_value VARBINARY(512) DEFAULT NULL,
  base_type INTEGER UNSIGNED DEFAULT 1,
  multiplier FLOAT DEFAULT 1,
  last_timestamp BIGINT UNSIGNED DEFAULT 0,
  ts_modified DATETIME NULL ON UPDATE CURRENT_TIMESTAMP,
  ts_created DATETIME DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY (id),
  UNIQUE KEY (idx, idx_agent),
  PRIMARY KEY (idx)
) ENGINE=InnoDB COMMENT='Data Point Table' AUTO_INCREMENT=1 ;

# ----------------------------------------------------------------------
# FOREIGN KEYS
# ----------------------------------------------------------------------

# Create foreign key for iset_data table (1 of 2)
ALTER TABLE iset_data
ADD CONSTRAINT FK_idx_datapoint_iset_datapoint_idx
FOREIGN KEY (idx_datapoint) REFERENCES iset_datapoint(idx)
ON UPDATE CASCADE
ON DELETE CASCADE;

# Create foreign key for iset_data table (2 of 2)
ALTER TABLE iset_data
ADD CONSTRAINT FK_idx_agent_iset_agent_idx
FOREIGN KEY (idx_agent) REFERENCES iset_agent(idx)
ON UPDATE CASCADE
ON DELETE CASCADE;

# Create foreign key for iset_datapoint table
ALTER TABLE iset_datapoint
ADD CONSTRAINT FK_iset_datapoint_iset_agent_idx
FOREIGN KEY (idx_agent) REFERENCES iset_agent(idx)
ON UPDATE CASCADE
ON DELETE CASCADE;
