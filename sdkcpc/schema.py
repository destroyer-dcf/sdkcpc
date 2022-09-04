
{
    
    'compilation': {
        'required': True,
        'type': 'dict',
        'schema': {
            'build': {
                'required': True,
                'type': 'string',
                'regex': '^(?!\s*$).+',
            },
            'version': {
                'type': 'string',
                'empty': False,
                'required': True,
                'regex': '^(?:(0\\.|([1-9]+\\d*)\\.))+(?:(0\\.|([1-9]+\\d*)\\.))+((0|([1-9]+\\d*)))$',
            }
        }
    },
    'general': {
        'required': True,
        'type': 'dict',
        'schema': {
            'name': {
                'type': 'string',
                'empty': False,
                'required': True,
                'regex': '^[a-zA-Z0-9]{1,8}$', # Valida que el nombre de fichero tenga 8 posiciones
            },
            'description': {
                'type': 'string',
                'empty': True,
                'required': True
            },
            'template': {
                'type': 'string',
                'empty': False,
                'required': True,
                'allowed': ["BASIC","8BP"]
            },
            'authors': {
                'type': 'string',
                'empty': False,
                'required': True,
                'regex': '^(?!\s*$).+',
            }
        }
    },
    'config': {
        'required': True,
        'type': 'dict',
        'schema': {
            'concatenate.bas.files': {
                'type': 'string',
                'empty': False,
                'required': True,
                'allowed': ["Yes", "No"]
            },
            'name.bas.file': {
                'type': 'string',
                'empty': False,
                'required': True,
                'regex': '^([a-zA-Z0-9])+(.bas|.BAS)$',
                        #'regex': '^[a-zA-Z0-9]{1,8}\.bas|.BAS$', # Valida que el nombre de fichero tenga 8 posiciones
            }
        }
    },
    'rvm': {
        'required': True,
        'type': 'dict',
        'schema': {
            'model.cpc': {
                'type': 'string',
                'empty': False,
                'required': True,
                'allowed': ["464", "664", "6128"]
            }
        }
    },
    'm4': {
        'required': True,
        'type': 'dict',
        'schema': {
            'ip': {
                'type': 'string',
                'empty': False,
                'required': True,
                'regex':'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
            }
        }
    }
}