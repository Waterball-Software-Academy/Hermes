from lotify.client import Client

import properties

client = Client(
    client_id=properties.LINE_NOTIFY_CLIENT_ID,
    client_secret=properties.LINE_NOTIFY_CLIENT_SECRET,
    redirect_uri=properties.LINE_NOTIFY_REDIRECT_URL
)


def get_lotify_client():
    return client
