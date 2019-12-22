from spotipy.util import RefreshingCredentials, parse_code_from_url, RefreshingToken
from selenium import webdriver
import time


class UrlHasChanged:
    def __init__(self, old_url):
        self.old_url = old_url

    def __call__(self, driver):
        return driver.current_url != self.old_url





def prompt_for_user_token(
        client_id: str,
        client_secret: str,
        redirect_uri: str,
        scope=None
) -> RefreshingToken:
    """
    Prompt for manual authentication.

    Open a web browser for the user to log in with Spotify.
    Prompt to paste the URL after logging in to parse the `code` URL parameter.

    Parameters
    ----------
    client_id
        client ID of a Spotify App
    client_secret
        client secret
    redirect_uri
        whitelisted redirect URI
    scope
        access rights as a space-separated list

    Returns
    -------
    RefreshingToken
        automatically refreshing user token
    """
    cred = RefreshingCredentials(client_id, client_secret, redirect_uri)
    url = cred.user_authorisation_url(scope)

    print('Opening browser for Spotify login...')


    #webbrowser.open(url)
    driver = webdriver.Firefox()
    driver.get(url)

    while True:
        time.sleep(5)
        current_url = driver.current_url
        if UrlHasChanged(current_url):
            if "/?code=" in current_url:
                break

    driver.quit()
    code = parse_code_from_url(current_url)
    return cred.request_user_token(code, scope)