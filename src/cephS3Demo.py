'''
Created on Apr 7, 2017

@author: MXQ
'''

import boto
import boto.s3.connection
access_key = 'SW4HV11JYW7008D02I1A'
secret_key = 'WCeqmcvNsz5TpCIR2nnGYhUJp09ASqgYL6fEfpcv'

conn = boto.connect_s3(
        aws_access_key_id = access_key,
        aws_secret_access_key = secret_key,
        host = '25.0.90.57', port = 7480,
        is_secure=False,               # uncomment if you are not using ssl
        calling_format = boto.s3.connection.OrdinaryCallingFormat(),
        )
print conn.aws_access_key_id
bucket = conn.get_bucket("wltest", validate=True, headers=None)

hello_key = bucket.get_key('EF229080F3B7C04DB95529E83402B0D1')
hello_key.set_canned_acl('public-read')
hello_url = hello_key.generate_url(0, query_auth=False, force_http=True)
print hello_url


