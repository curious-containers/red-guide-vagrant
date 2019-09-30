#!/usr/bin/env python3

import json

SSH_SERVER = 'avocado01.f4.htw-berlin.de'
SSH_AUTH = {'username': '{{ssh_username}}', 'password': '{{ssh_password}}'}
DATA_DIR = '/data/ldap/histopathologic/original_read_only/PCAM_extracted'
AGENCY_URL = 'https://agency.f4.htw-berlin.de/cc'
LEARNING_RATES = [0.0001, 0.0005]


batches = []

for i, learning_rate in enumerate(LEARNING_RATES):
    batch = {
        'inputs': {
            'data_dir': {
                'class': 'Directory',
                'connector': {
                    'command': 'red-connector-ssh',
                    'mount': True,
                    'access': {
                        'host': SSH_SERVER,
                        'auth': SSH_AUTH,
                        'dirPath': DATA_DIR
                    }
                }
            },
            'learning_rate': learning_rate,
            'steps_per_epoch': 1,
            'num_epochs': 1,
            'log_dir': {
                'class': 'Directory',
                'connector': {
                    'command': 'red-connector-ssh',
                    'mount': True,
                    'access': {
                        'host': SSH_SERVER,
                        'auth': SSH_AUTH,
                        'dirPath': 'cnn-training/log',
                        'writable': True
                    }
                }
            },
            'log_file_name': 'training_{}.log'.format(i)
        },
        'outputs': {
            'weights_file': {
                'class': 'File',
                'connector': {
                    'command': 'red-connector-ssh',
                    'access': {
                        'host': SSH_SERVER,
                        'auth': SSH_AUTH,
                        'filePath': 'cnn-training/weights/weights_{}.h5'.format(i),
                    }
                }
            }
        }
    }
    batches.append(batch)

with open('cnn-training.cwl.json') as f:
    cli = json.load(f)

red = {
    'redVersion': '8',
    'cli': cli,
    'batches': batches,
    'container': {
        'engine': 'docker',
        'settings': {
            'image': {
                'url': 'docker.io/curiouscontainers/cnn',
            },
            'ram': 32000,
            'gpus': {
                'vendor': 'nvidia',
                'count': 1
            }
        }
    },
    'execution': {
        'engine': 'ccagency',
        'settings': {
            'access': {
              'url': AGENCY_URL,
              'auth': {
                  'username': '{{agency_username}}',
                  'password': '{{agency_password}}'
              }
            }
        }
    }
}

with open('cnn-training.red.json', 'w') as f:
    json.dump(red, f, indent=4)
