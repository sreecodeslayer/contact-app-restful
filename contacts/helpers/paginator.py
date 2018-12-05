"""Simple helper to paginate query
"""
from flask import url_for, request

DEFAULT_PAGE_SIZE = 10
DEFAULT_PAGE_NUMBER = 1


def paginate(query, schema, field=None):
    '''
    Returns the pagination object that include:
    iter_pages, next, prev, has_next, has_prev, next_num, prev_num.
    '''
    page = int(request.args.get('page', DEFAULT_PAGE_NUMBER))
    per_page = int(request.args.get('perPage', DEFAULT_PAGE_SIZE))
    paginated_obj = query.paginate(page=page, per_page=per_page)

    return {
        'total': paginated_obj.total,
        'pages': paginated_obj.pages,
        'next': paginated_obj.next_num,
        'prev': paginated_obj.prev_num,
        'results': schema.dump(paginated_obj.items).data
    }
