import json

import testinger
from testinger import TestCase
from testinger.web import client, WebTestCase
from testinger.tools import step, no_test, raises, scenario

scenarios = [{"code" : 200, "response_key" : "success", "value" : "data has sended"}]

class ExTest(TestCase):

    @step('Check response status for code {code}')
    @scenario(scenarios)
    @no_test
    def get_user_friends(self):
        """
           Get user friends
        """
        client = None
        response = client.get('/api/device/friends/upload')
        # test object is mockup with data in actual scenario 
        assert response.status_code == self.test_obj.code
        with raises(AttributeError):
             json_response = json.loads(response.text)
        # you may disable log messages with flag (log = False on run method)
        self.log("Message to print")
        json_response = json.loads(response.content)
        assert self.test_obj.response_key in json_response
        try:
             assert json_response[self.test_obj.response_key] == self.test_obj.value
        except AssertionError:
             self.fail("Doesn't work")

class WebTest(WebTestCase):
    # version with special test class to web applications

    __stage__ = 'Friends Test'

    @step('Check response status for code {code}')
    @client('/api/device/friends/upload', mime = 'json')
    @scenario(scenarios)
    def get_user_friends(self):
        print("executed without args")
        assert self.status_code == self.test_obj.code
        assert self.test_obj.response_key in  self.data
        assert self.data[self.test_obj.response_key] == self.test_obj.value

    @step('Check response status for code {code}')
    @client('/api/device/friends/upload', mime = 'json')
    @scenario(scenarios)
    def get_user_friends_args(self, code, response_key, value):
        print("executed with args")
        assert self.status_code == code
        assert response_key in self.data
        assert self.data[response_key] == value

    @no_test
    def no_test_method(self):
        print("is wery bad when u see this on running test")

if __name__ == "__main__":
    testinger.main()