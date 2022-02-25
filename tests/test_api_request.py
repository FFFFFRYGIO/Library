import pytest

import api_request as program

BOOK_PARAMS_1 = {
    'intitle': 'frankenstein',
    'inauthor': 'shelley',
}
BOOK_PARAMS_2 = {
    'isbn': '9780262533287',
}
BOOK_PARAMS_3 = {
    'inpublisher': '2014-03',
    'iccn': '20',
}
BOOK_PARAMS_4 = {
    'subject': 'Young Adult Fiction',
}


@pytest.mark.parametrize('params, result', [
    (BOOK_PARAMS_1, 149),
    (BOOK_PARAMS_2, 1),
    (BOOK_PARAMS_3, -1),
    (BOOK_PARAMS_4, 1),
                                            ])
def test_api(params, result):
    # if function returns query
    query = program.generate_query(params)
    assert len(query)
    # if query returns good amount of books
    response = program.get_api_request(params)
    if result != -1:
        res_result = response['totalItems']
    else:
        res_result = response
    assert res_result == result
