manga_validator = {
    'validator': {
        '$jsonSchema': {
            'description': 'A manga that is being tracked by my program',
            'required': ['name', 'url', 'current_chapter', 'chapters'],
            'additionalProperties': False,
            'properties': {
                '_id': {},
                'name': {
                    'bsonType': 'string',
                    'description': 'name of the anime',
                },
                'url': {
                    'bsonType': 'string',
                    'description': 'cut off url after .com/ (or .ext/) for example https://animeheaven.me/'
                },
                'current_chapter': {
                    'bsonType': 'int',
                    'description': 'Next unread chapter'
                },
                'chapters': {
                    'bsonType': 'array',
                    'description': 'list of chapters',
                    'minItems': 0,
                    'uniqueItems': True,
                    'items': {
                        'bsonType': 'objectId'
                    }
                },
            }
        }
    }
}

chapter_validator = {
    'validator': {
        '$jsonSchema': {
            'description': 'individual chapter of an anime',
            'required': ['name', 'url', 'chapter_number', 'read'],
            'additionalProperties': False,
            'properties': {
                '_id': {},
                'name': {
                    'bsonType': 'string',
                    'description': 'name of the anime',
                },
                'url': {
                    'bsonType': 'string',
                    'description': 'cut off url after .com/ (or .ext/) for example https://animeheaven.me/'
                },
                'chapter_number': {
                    'bsonType': 'int',
                    'description': 'number of chapter in series'
                },
                'read': {
                    'bsonType': 'bool',
                    'description': 'true if episode has been watched'
                },
            }
        }
    }
}

