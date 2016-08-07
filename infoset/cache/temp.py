
    def _insert_datapoint(metadata):
        """Insert new datapoint into database.

        Args:
            metadata: Tuple of datapoint metadata.
                (uid, did, label, source, description)
                uid: Agent UID
                did: Datapoint ID
                label: Datapoint label created by agent
                source: Source of the data (subsystem being tracked)
                description: Description provided by agent config file (unused)
                base_type = SNMP base type (Counter32, Counter64, Gauge etc.)

        Returns:
            None

        """
        # Initialize key variables
        (uid, did, label, source, _, base_type) = metadata

        # Get agent index value
        agent_object = agent.Get(uid)
        idx_agent = agent_object.idx()

        # Prepare SQL query to read a record from the database.
        sql_query = (
            'INSERT INTO iset_datapoint '
            '(id, idx_agent, agent_label, agent_source, base_type ) VALUES '
            '("%s", %d, "%s", "%s", %d)'
            '') % (did, idx_agent, label, source, base_type)

        # Do query and get results
        database = db.Database()
        database.modify(sql_query, 1032)


