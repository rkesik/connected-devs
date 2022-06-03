from typing import Optional, List

from github import Github
from github.GithubException import UnknownObjectException


class GitHubRepo:
    def __init__(self, errors: list = None) -> None:
        self.client = Github()
        self.errors = errors or list()

    def get_organizations(self, handle: str, errors: list = None) -> List[str]:
        # TODO(rkesik): add more specific exceptions handling
        # TODO(rkesik): PyGithub is not async so here we are waiting becauase under the hood requests is being used
        errors = errors or self.errors
        try:
            user = self.client.get_user(handle)
            names = [org.name for org in user.get_orgs()]
        except UnknownObjectException as e:
            errors.append(f"User {handle} not found.")
        except Exception as e:
            errors.append(f"Error: {e}")
        return names
