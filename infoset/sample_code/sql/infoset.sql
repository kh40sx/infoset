# Create the database from scratch
drop database infoset;
create database infoset;
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
  id VARCHAR(64),
  name VARCHAR(64) DEFAULT NULL,
  description VARCHAR(64) DEFAULT NULL,
  hostname VARCHAR(75) DEFAULT NULL,
  enabled INTEGER UNSIGNED DEFAULT 1,
  last_contacted BIGINT UNSIGNED DEFAULT NULL,
  ts_modified TIMESTAMP NULL ON UPDATE CURRENT_TIMESTAMP,
  ts_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY (id),
  PRIMARY KEY (idx)
) ENGINE=InnoDB COMMENT='Agent Table' AUTO_INCREMENT=1 ;
#CREATE TRIGGER agent_insert_check BEFORE INSERT ON iset_agent
#  FOR EACH ROW
#  SET NEW.ts_created = CURRENT_TIMESTAMP;

# ----------------------------------------------------------------------

# Create table for datapoints
CREATE TABLE iset_datapoint (
  idx BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  idx_agent BIGINT UNSIGNED NOT NULL DEFAULT 1,
  id VARCHAR(64),
  agent_label VARCHAR(64) DEFAULT NULL,
  agent_source VARCHAR(128) DEFAULT NULL,
  enabled INTEGER UNSIGNED DEFAULT 1,
  base_type INTEGER UNSIGNED DEFAULT 1,
  multiplier FLOAT DEFAULT 1,
  last_timestamp BIGINT UNSIGNED DEFAULT 0,
  ts_modified TIMESTAMP NULL ON UPDATE CURRENT_TIMESTAMP,
  ts_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY (id),
  UNIQUE KEY (idx, idx_agent),
  PRIMARY KEY (idx)
) ENGINE=InnoDB COMMENT='Data Point Table' AUTO_INCREMENT=1 ;
#CREATE TRIGGER datapoint_insert_check BEFORE INSERT ON iset_datapoint
#  FOR EACH ROW
#  SET NEW.ts_created = CURRENT_TIMESTAMP;

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
