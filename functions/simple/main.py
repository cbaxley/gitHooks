import asyncio
import json
import urllib.parse as urlparse


async def test_async_generator():
    for i in range(5):
        yield i
        print(i)
        await asyncio.sleep(0.01)


def handle(event, context):
    resolver = Resolver(event)
    resolver.run()

    return {
        "isBase64Encoded": False,
        "statusCode": 200,
        "headers": {},
        "body": ""
    }


class Resolver:
    classname = 'null_event'
    event_string = ''

    def __init__(self, event):
        self.event = event

    def run(self):
        self.get_event_string()
        self.set_classname()
        self.get_class()
        self.handler.run(self.event)

    def get_event_string(self):
        try:
            self.event_string = self.event['headers']['X-GitHub-Event']
        except KeyError:
            pass

    def set_classname(self):
        self.classname = self.snake_to_studly(self.event_string)

    def get_class(self):
        print(f'Setting handler to : "{self.classname}"')
        try:
            self.handler = globals()[self.classname]()
        except:
            self.handler = NullEvent()

    def snake_to_studly(self, snake):
        return ''.join([*map(str.title, snake.split('_'))])

    pass


class NullEvent:
    def set_payload(self):
        self.payload = json.loads(urlparse.parse_qs(self.event['body'])['payload'][0])

    def run(self, event):
        print('No handler defined for event')
        pass


class PullRequest(NullEvent):
    def set_pull_request(self):
        self.pull_request = self.payload['pull_request']

    def run(self, event):
        self.event = event
        self.set_payload()
        self.set_pull_request()
        for key, value in self.pull_request.items():
            print(key)
        # payload = json.loads(body)
        # print(payload)
