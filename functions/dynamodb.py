import json
import logging

from pynamodb.exceptions import DeleteError, DoesNotExist


# TODO add pagination
# TODO return just the columns needed, vs everything; use an index
def ls(model):
    """Return all of the organizations in the DB."""
    results = model.scan()
    print(results)

    return {
        'statusCode': 200,
        'body': json.dumps({'items': [dict(r) for r in results]})
    }


# TODO don't add dupe
def create(model, body):
    entry = model(**body)
    entry.save()

    return {
        'statusCode': 201
    }


# TODO make use of the batch operations
# https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_BatchWriteItem.html
# def create_many(model, body):
#     with model.batch_write() as batch:
#         entry = model(**body)
#         batch.save(entry)
#
#     return {
#         'statusCode': 201
#     }


def retrieve(model, key):
    try:
        entry = model.get(hash_key=key)
    except DoesNotExist:
        return {
            'statusCode': 404,
            'body': json.dumps({'error_message': f"'{key}' not found"})
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
            'body': json.dumps({'error_message': f"'{key}' not found"})
        }

    keys_changed = False
    fields_changed = False

    for k in entry:
        if k in body and body[k] != entry[k]:
            setattr(entry, k, body[k])
            fields_changed = True

    # If there are new fields, perform the update
    for k in body:
        if k == 'id':  # This assumes that 'id' is the only Dynamo primary key
            keys_changed = True
        if k not in entry:
            setattr(entry, k, body[k])
            fields_changed = True

    if fields_changed:
        entry.save()
        if keys_changed:
            delete(model, key)
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
