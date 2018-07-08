import json
import logging

from pynamodb.exceptions import DeleteError, DoesNotExist


# TODO add pagination
# TODO return just the columns needed, vs everything
def ls(model):
    """Return all of the organizations in the DB."""
    results = model.scan()

    return {
        'statusCode': 200,
        'body': json.dumps({'items': [dict(r) for r in results]})
    }


# TODO what happens on dupe slug?
def create(model, body):
    entry = model(body)
    entry.save()

    return {
        'statusCode': 201
    }


def replace(model, key, body):
    delete(model, key)
    create(model, body)

    return {
        'statusCode': 200
    }


def retrieve(model, key):
    try:
        entry = model.get(hash_key=key)
    except DoesNotExist:
        return {
            'statusCode': 404,
            'body': json.dumps({'error_message': 'Organization not found'})
        }

    return {
        'statusCode': 200,
        'body': json.dumps(dict(entry))
    }


# TODO check for duplicate org name + fail
def update(model, key, body):
    try:
        entry = model.get(hash_key=key)
    except DoesNotExist:
        return {
            'statusCode': 404,
            'body': json.dumps({'error_message': 'Organization not found'})
        }

    key_changed = False
    field_changed = False

    for k in entry:
        if k in body and body[k] != entry[k]:
            # TODO check if it's a key and set key_changed if needed
            # if it's a key:
            #     key_changed = True
            entry[k] = body[k]
            field_changed = True

    # If there are new fields, perform the update
    for k in body:
        if k not in entry:
            entry[k] = body[k]
            field_changed = True

    if key_changed:
        return replace(model, key, entry)
    elif field_changed:
        entry.save()
    else:
        logging.info('Nothing changed, not updating')

    return {
        'statusCode': 200
    }


def delete(model, key):
    try:
        entry = model.get(hash_key=key)
    except DoesNotExist:
        return {
            'statusCode': 404,
            'body': json.dumps({'error_message': f"'{key}' not found"})
        }

    try:
        entry.delete()
    except DeleteError:
        return {
            'statusCode': 400,
            'body': json.dumps({'error_message': f"Unable to delete '{key}'"})
        }

    return {
        'statusCode': 204
    }
