from urlparse import urljoin


def get_url(response, url):
    """
    Simple helper that consolidates urls
    :param response: Response object that contains base part of url (e.g. http://example.com/)
    :param url: Second part of url (e.g. /author?name=example)
    :return: returns consolidated and formatted full url (e.g. http://example.com/author?name=example)
    """
    return urljoin(response.url, url.strip())
