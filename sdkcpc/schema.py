{
    'build': {
        'required': True,
        'type': 'date'
    },
    'version': {
        'required': True,
        'type': 'string'
    },
    'project': {
        'required': True,
        'type': 'dict',
        'schema': {
            'general': {
                'required': True,
                'type': 'dict',
                'schema': {
                    'name': {
                        'type': 'string',
                        'empty': False,
                        'required': True,
                        'regex': '^([a-zA-Z0-9]{1,8})*[^\s]\1*$', # Valida que el nombre de fichero tenga 8 posiciones
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
                    'author': {
                        'type': 'string',
                        'empty': False,
                        'required': True
                    }
                }
            },
            'configurations': {
                'required': True,
                'type': 'dict',
                'schema': {
                    'concatenate_bas_files': {
                        'type': 'boolean',
                        'empty': False,
                        'required': True
                    },
                    # 'validate_83_files': {
                    #     'type': 'boolean',
                    #     'empty': True,
                    #     'required': True
                    # },
                    'name_bas_file': {
                        'type': 'string',
                        'empty': False,
                        'required': True,
                        'regex': '^([a-zA-Z0-9])+(.bas|.BAS)$',
                        #'regex': '^[a-zA-Z0-9]{1,8}\.bas|.BAS$', # Valida que el nombre de fichero tenga 8 posiciones
                    }
                }
            },
            'dsk_image': {
                'required': True,
                'type': 'dict',
                'schema': {
                    'name': {
                        'type': 'string',
                        'empty': False,
                        'required': True,
                        'regex': '^([a-zA-Z0-9_-])+(.dsk|.DSK)$',
                    },
                    'generate': {
                        'type': 'boolean',
                        'empty': True,
                        'required': True
                    }
                }
            },
            'cdt_image': {
                'required': True,
                'type': 'dict',
                'schema': {
                    'name': {
                        'type': 'string',
                        'empty': False,
                        'required': True,
                        'regex': '^([a-zA-Z0-9_-])+(.cdt|.CDT)$',
                    },
                    'generate': {
                        'type': 'boolean',
                        'empty': True,
                        'required': True
                    },
                    'order_files': {
                        'type': 'list',
                        'empty': True,
                        'required': False,
                        'schema' : {'type': 'string'}
                    }
                }
            }
        }
    },
    'emulator': {
        'required': True,
        'type': 'dict',
        'schema': {
            'rvm': {
                'required': True,
                'type': 'dict',
                'schema': {
                    'model': {
                        'type': 'integer',
                        'empty': False,
                        'required': True,
                        'allowed': [464, 664, 6128]
                    },
                    'path': {
                        'type': 'string',
                        'empty': True,
                        'required': True
                    }
                }
            },
            'm4board': {
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
    }
}