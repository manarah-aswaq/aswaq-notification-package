# works in Python 2 & 3
import datetime

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
    BASE_URL = "http://localhost:8000/"
    CREATE_NOTIFICATIONS_URL = "notifications/api/notifications-requests/"
    CANCEL_NOTIFICATIONS_URL = "notifications/api/notifications-requests/%s/cancel_notification/"
    CREATE_GROUP_URL = "notifications/api/user-token-group/"
    REMOVE_GROUP_TOKEN_URL = "notifications/api/user-token-group/%s/remove_from_group/"
    ADD_GROUP_TOKEN_URL = "notifications/api/user-token-group/%s/add_to_group/"

    def __init__(self, api_token):
        """
        Set the authorization key for the api
        :param api_token: Api token from the api
        """
        self.api_token = "Token " + api_token

    def send_notifications(self, send_date=None, text=None, image=None, title=None, user_tokens=None,
                           tokens_group_name=None, click_action=None):
        """
        Send notification request to be scheduled on the notifications WS, can be sent to either list of user tokens
        or group of user token
        :param send_date:Date to be sent (leave empty for datetime.datetime.utcnow())
        :param text:Notification body to be sent
        :param image: Notification icon
        :param title:Notification title
        :param click_action:action to be triggered clickin notification
        :param user_tokens: <List> or <Tuple> of recipients  (Tokens from firebase)
        :param tokens_group_name: Token group to send the notification to instead of user tokens
        :return:
        """
        assert not isinstance(user_tokens, str)
        data = {
            "send_date": send_date or str(datetime.datetime.utcnow()),
            "text": text or "",
            "image": image or "",
            "title": title or "",
            "click_action": click_action or "",
        }
        if user_tokens:
            data['user_tokens'] = user_tokens
        if tokens_group_name:
            data['user_token_group'] = tokens_group_name

        result = requests.post(self.BASE_URL + self.CREATE_NOTIFICATIONS_URL, json=data,
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
        result = requests.post(self.BASE_URL + self.CANCEL_NOTIFICATIONS_URL % reference_id,
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

        result = requests.post(self.BASE_URL + self.CREATE_GROUP_URL, json=data,
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
        result = requests.post(self.BASE_URL + self.REMOVE_GROUP_TOKEN_URL % group_name, json=data,
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
        result = requests.post(self.BASE_URL + self.ADD_GROUP_TOKEN_URL % group_name, json=data,
                               headers={'Authorization': self.api_token})
        return self.proccess_results(result)
