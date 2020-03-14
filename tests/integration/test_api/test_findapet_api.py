import app


def test_index():
    tester = app.app.test_client()
    response = tester.get('/', content_type='html/text')
    assert response.status_code==200
    assert b'Glen of Imaal Terrier' in response.data





