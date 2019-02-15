from ScoutSuite.providers.aws.configs.regions import RegionalServiceConfig, RegionConfig, api_clients


########################################
# DynamoDBRegionConfig
########################################

class DynamoDBRegionConfig(RegionConfig):
    """
    DynamoDB configuration for a single AWS region
    """

    def parse_table(self, global_params, region, table):
        """
        Parse a single table and fetch additional attributes

        :param global_params:           Parameters shared for all regions
        :param region:                  Name of the AWS region
        :param table:                   Table

        """

        api_client = api_clients[region]
        table_details = api_client.describe_table(TableName=table)['Table']
        table_details['name'] = table

        table_details['manual_backups'] = api_client.list_backups(TableName=table)['BackupSummaries']

        continous_backup = api_client.describe_continuous_backups(TableName=table)['ContinuousBackupsDescription']
        continous_backup = continous_backup['PointInTimeRecoveryDescription']['PointInTimeRecoveryStatus']
        if continous_backup == 'ENABLED':
            table_details['automatic_backups_enabled'] = True
        else:
            table_details['automatic_backups_enabled'] = False

        self.tables[len(self.tables)] = table_details


########################################
# DynamoDBConfig
########################################

class DynamoDBConfig(RegionalServiceConfig):
    """
    DynamoDB configuration for all AWS regions
    """

    region_config_class = DynamoDBRegionConfig

    def __init__(self, service_metadata, thread_config=4):
        super(DynamoDBConfig, self).__init__(service_metadata, thread_config)
