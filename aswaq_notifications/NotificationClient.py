# works in Python 2 & 3
import datetime
import warnings

import requests


class _Singleton(type):
    """ A metaclass that creates a Singleton base class when called. """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(_Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Singleton(_Singleton('SingletonMeta', (object,), {})): pass


class NotificationClient(Singleton):
    """
    Wrapper for notifications API
    """
    CREATE_NOTIFICATIONS_URL = "notifications/api/notifications-requests/"
    CANCEL_NOTIFICATIONS_URL = "notifications/api/notifications-requests/%s/cancel_notification/"
    CREATE_GROUP_URL = "notifications/api/user-token-group/"
    REMOVE_GROUP_TOKEN_URL = "notifications/api/user-token-group/%s/remove_from_group/"
    ADD_GROUP_TOKEN_URL = "notifications/api/user-token-group/%s/add_to_group/"

    def __init__(self, api_token, base_url):
        """
        Set the authorization key for the api
        :param api_token: Api token from the api
        """
        self.api_token = "Token " + api_token
        self.base_url = base_url

    def send_notifications(self,
                           title,
                           body,
                           message_data,
                           send_date=None,
                           user_tokens=None,
                           ios_user_tokens=None,
                           android_user_tokens=None,
                           tokens_group_name=None):
        """
        Send notification request to be scheduled on the notifications WS, can be sent to either list of user tokens
        or group of user token
        :param send_date:Date to be sent (leave empty for datetime.datetime.utcnow())
        :param message_data:Notification json data
        :param user_tokens: <List> or <Tuple> of recipients  (Tokens from firebase) (deprecated)
        :param ios_user_tokens: <List> or <Tuple> of recipients  (Ios Tokens from firebase)
        :param android_user_tokens: <List> or <Tuple> of recipients  (android Tokens from firebase)
        :param tokens_group_name: Token group to send the notification to instead of user tokens
        :return:
        """
        assert not isinstance(ios_user_tokens, str)
        assert message_data
        data = {
            "send_date": send_date or str(datetime.datetime.utcnow()),
            "message_data": message_data,
            "title": title,
            "body": body
        }
        if user_tokens:
            assert not isinstance(user_tokens, str)
            warnings.warn(
                "using 'user_token' deprecated and will be removed in the"
                " next version, use 'ios_user_tokens' and/or android_user_tokens instead",
                DeprecationWarning)
            data['user_tokens'] = user_tokens
        if ios_user_tokens:
            assert not isinstance(ios_user_tokens, str)
            if 'user_tokens' not in data:
                data['user_tokens'] = {}
            data['user_tokens']['IOS'] = ios_user_tokens
        if android_user_tokens:
            assert not isinstance(android_user_tokens, str)
            if 'user_tokens' not in data:
                data['user_tokens'] = {}
            data['user_tokens']['AND'] = android_user_tokens
        if tokens_group_name:
            data['user_token_group'] = tokens_group_name

        result = requests.post(self.base_url + self.CREATE_NOTIFICATIONS_URL, json=data,
                               headers={'Authorization': self.api_token})
        return self.proccess_results(result)

    @staticmethod
    def proccess_results(result):
        """
        Handel formatting the api results
        :param result:Data returned from API
        :return:
        """
        try:
            return {
                "status": str(result.status_code),
                'result': result.json()
            }
        except:
            return {
                "status": str(result.status_code),
                'result': result.content
            }

    def cancel_notification(self, reference_id):
        """
        Cancel scheduled Notification
        :param reference_id: Notification reference ID
        :return:
        """
        result = requests.post(self.base_url + self.CANCEL_NOTIFICATIONS_URL % reference_id,
                               headers={'Authorization': self.api_token})
        return self.proccess_results(result)

    def create_tokens_group(self, name=None, user_tokens=None):
        """
        Create user token group
        :param name:group name
        :param user_tokens:<List> or <Tuple> of recipients  (Tokens from firebase)
        :return:
        """
        assert not isinstance(user_tokens, str)
        assert isinstance(name, str)
        data = {"name": name or "", 'user_tokens': user_tokens or []}

        result = requests.post(self.base_url + self.CREATE_GROUP_URL, json=data,
                               headers={'Authorization': self.api_token})
        return self.proccess_results(result)

    def remove_token_from_group(self, group_name, user_tokens):
        """
        Remove users to token group
        :param group_name:token group name to remove the token from
        :param user_tokens:<List> or <Tuple> of tokens to be removed from the group  (Tokens from firebase)
        :return:
        """
        assert not isinstance(user_tokens, str)
        data = {'user_tokens': user_tokens or []}
        result = requests.post(self.base_url + self.REMOVE_GROUP_TOKEN_URL % group_name, json=data,
                               headers={'Authorization': self.api_token})
        return self.proccess_results(result)

    def add_token_to_group(self, group_name, user_tokens):
        """
        Add users to token group
        :param group_name:token group name to add the token from
        :param user_tokens:<List> or <Tuple> of tokens to be added to the group (Tokens from firebase)
        :return:
        """
        assert not isinstance(user_tokens, str)
        data = {'user_tokens': user_tokens or []}
        result = requests.post(self.base_url + self.ADD_GROUP_TOKEN_URL % group_name, json=data,
                               headers={'Authorization': self.api_token})
        return self.proccess_results(result)
