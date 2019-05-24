import json

from pretf import tf


def main(params):

    name = f'pretf-test-{params.envname}'

    bucket = yield tf('resource.aws_s3_bucket.test', {
        'bucket': name,
        'acl': 'private',
        'server_side_encryption_configuration': {
            'rule': {
                'apply_server_side_encryption_by_default': {
                    'sse_algorithm': 'AES256',
                },
            },
        },
    })

    policy = yield tf('data.aws_iam_policy_document.lambda', {
        'statement': {
            'effect': 'Allow',
            'actions': [
                's3:ListBucket',
                's3:PutObject',
            ],
            'resources': [
                bucket.arn,
                f'{bucket.arn}/*',
            ],
        }
    })