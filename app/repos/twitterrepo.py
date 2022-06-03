from typing import List

import twitter

# TODO(rkesik): TwitterRepo need to be implemented
class TwiterRepo:
    def __init__(self, errors: list = None) -> None:
        self.client = twitter.Api(
            consumer_key=...,
            consumer_secret=...,
            access_token_key=...,
            access_token_secret=...,
        )
        self.errors = errors or list()

    async def get_followers(self, handle: str, errors: List[str] = None) -> List[str]:
        # TODO: to be implemented
        return ["rkesik"]
        ...
