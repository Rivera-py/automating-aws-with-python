# -*- coding: utf-8 -*-

"""Manage Route 53 with this class."""

import uuid


class DomainManager:
    """Create a DomainManager object."""

    def __init__(self, session):
        """Grab the Route 53 client for managging."""
        self.session = session
        self.client = self.session.client('route53')

    def find_hosted_zone(self, domain_name):
        """Look for an existing zone which matches domain_name."""
        paginator = self.client.get_paginator('list_hosted_zones')

        for page in paginator.paginate():
            for zone in page['HostedZones']:
                if domain_name.endswith(zone['Name'][:-1]):
                    return zone

        return None

    def create_hosted_zone(self, domain_name):
        """If it does not exist create the zone."""
        zone_name = ".".join(domain_name.split('.')[-2:]) + "."

        return self.client.create_hosted_zone(
            Name=zone_name,
            CallerReference=str(uuid.uuid4())
        )

    def create_s3_domain_record(self, zone, domain_name, endpoint):
        """Create domain record if it doesn't exist."""
        return self.client.change_resource_record_sets(
            HostedZoneID=zone['Id'],
            ChangeBatch={
                'Comment': 'Created by webotron',
                'Changes': [{
                    'Action': 'UPSERT',
                    'ResourceRecordSet': {
                        'Name': domain_name,
                        'Type': 'A',
                        'AliasTarget': {
                            'HostedZoneId': endpoint.zone,
                            'DNSName': endpoint.host,
                            'EvaluateTargetHealth': False
                        }
                    }
                }]
            }
        )
