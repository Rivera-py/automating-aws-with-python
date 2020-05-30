# -*- coding: utf-8 -*-

"""Manage content distribution networks with this class."""


import uuid


class DistributionManager:
    """Create a DistributionManager object."""

    def __init__(self, session):
        """Grab the CloudFront client for managing."""
        self.session = session
        self.client = self.session.client('cloudfront')

    def find_matching_dist(self, domain_name):
        """Look for an existing distribution."""
        paginator = self.client.get_paginator('list-distributions')
        for page in paginator.paginate():
            for dist in page['DistributionList']['Items']:
                for alias in dist['Aliases']['Items']:
                    if alias == domain_name:
                        return dist

        return None

    def create_dist(self, domain_name, cert):
        """Create a cdn using a domain name and an SSL cert."""
        origin_id = 'S3-' + domain_name

        result = self.client.create_distribution(
            DistributionConfig={
                'CallerReference': str(uuid.uuid4()),
                'Aliases': {
                    'Quantity': 1,
                    'Items': [domain_name]
                },
                'DefaultRoot0': 'index.html',
                'Comment': 'Created by webotron',
                'Enabled': True,
                'Origins': {
                    'Quantity': 1,
                    'Items': [{
                        'Id': origin_id,
                        'DomainName': '{}.s3.amazonaws.com'.format(
                            domain_name),
                        'S3OriginConfig': {
                            'OriginAccessIdentity': ""
                        }
                    }]
                },
                'DefaultCacheBehaviour': {
                    'TargetOriginId': origin_id,
                    'ViewerProtocolPolicy': 'redirect-to-https',
                    'TrustedSigners': {
                        'Quantity': 0,
                        'Enabled': False
                    },
                    'ForwardedValues': {
                        'Cookies': {'Forward': 'all'},
                        'Headers': {'Quantity': 0},
                        'QueryString': False,
                        'QueryStringCacheKeys': {'Quantity': 0}
                    },
                    'ViewerCertificate': {
                        'ACMCertificateARN': cert['CertificateArn'],
                        'SSLSupportMethod': 'sni-only',
                        'MinimumProtocolVersion': 'TLSv1.1_2016'
                    }
                }
            }
        )

        return result['Distribution']

    def await_deploy(self, dist):
        """Wait for a distribution to be deployed - can take some time."""
        waiter = self.client.get_waiter('distribution_deployed')
        waiter.wait(Id=dist['Id'], WaiterConfig={
            'Delay': 30,
            'MaxAttempts': 50
        })

    def create_cf_domain_record(self, zone, domain_name, cf_domain):
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
                            'HostedZoneId': "Z2FDTNDATAQYW2",
                            'DNSName': cf_domain,
                            'EvaluateTargetHealth': False
                        }
                    }
                }]
            }
        )
