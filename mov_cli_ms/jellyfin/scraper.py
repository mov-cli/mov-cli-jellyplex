from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional, Dict, Generator, Any

    from mov_cli import Config
    from mov_cli.http_client import HTTPClient
    from mov_cli.scraper import ScraperOptionsT

from platform import uname

from mov_cli.scraper import Scraper
from mov_cli.utils import EpisodeSelector
from mov_cli.errors import MovCliException
from mov_cli import Single, Multi, Metadata, MetadataType

__all__ = ("JellyfinScraper",)


class JellyfinScraper(Scraper):
    def __init__(
        self,
        config: Config,
        http_client: HTTPClient,
        options: Optional[ScraperOptionsT] = None,
    ) -> None:
        env_config = config.get_env_config()

        self.base_url = env_config("JELLY_URL", default=None, cast=str)
        self.username = env_config("JELLY_USERNAME", default=None, cast=str)
        self.password = env_config("JELLY_PASSWORD", default=None, cast=str)

        self.uuid = uname().node  # NOTE: To prevent of multiple device detections

        super().__init__(config, http_client, options)

        self.new_headers, self.user_id, self.api_key = self.__get_auth()

    def __get_auth(self):
        auth_data = {"username": self.username, "Pw": self.password}

        headers = self.config.http_headers.copy()

        authorization = f'MediaBrowser Client="mov-cli", Device="mov-cli", DeviceId="{self.uuid}", Version="mov-cli-ms"'

        headers["Authorization"] = authorization

        authbyname = self.http_client.post(
            self.base_url + "/Users/AuthenticateByName",
            headers = headers,
            json = auth_data,
            include_default_headers = False,
        )

        if authbyname.is_error:
            raise InvalidLogin(self.username)

        r = authbyname.json()

        token = r["AccessToken"]
        user_id = r["User"]["Id"]

        headers["Authorization"] = f'{authorization}, Token="{token}"'

        return headers, user_id, token

    def search(self, query: str, limit: Optional[int]) -> Generator[Metadata, Any, None]:
        limit = 20 if limit is None else limit

        uri = f"/Users/{self.user_id}/Items?recursive=true&searchTerm={query}"

        if query in ["all+", "*"]:
            uri = f"/Users/{self.user_id}/Items?recursive=true"

        items = self.http_client.get(
            self.base_url + uri, headers=self.new_headers, include_default_headers=False
        ).json()["Items"][:limit]

        for item in items:
            if item["Type"] not in ["Series", "Movie"]:
                continue

            yield Metadata(
                id = item["Id"],
                title = item["Name"],
                type= MetadataType.SINGLE if item["Type"] == "Movie" else MetadataType.MULTI,
                year = item["PremiereDate"][:4]
            )

    def scrape_episodes(self, metadata: Metadata) -> Dict[int, int] | Dict[None, int]:
        episodes_dict = {}

        items = self.http_client.get(
            self.base_url + f"/Shows/{metadata.id}/Seasons?isSpecialSeason=false",
            headers = self.new_headers,
            include_default_headers = False,
        ).json()["Items"]

        for i in range(len(items)):
            item = items[i]

            id = item.get("Id")

            episodes = self.http_client.get(
                self.base_url + f"/Shows/{metadata.id}/Episodes?seasonId={id}",
                headers = self.new_headers,
                include_default_headers = False
            ).json()["Items"]

            episodes_dict[i + 1] = len(episodes)

        return episodes_dict

    def scrape(self, metadata: Metadata, episode: EpisodeSelector) -> Single | Multi:
        if metadata.type == MetadataType.MULTI:
            season_id = self.http_client.get(
                self.base_url + f"/Shows/{metadata.id}/Seasons?isSpecialSeason=false",
                headers = self.new_headers,
                include_default_headers = False,
            ).json()["Items"][episode.season - 1]["Id"]

            itemId = self.http_client.get(
                self.base_url + f"/Shows/{metadata.id}/Episodes?seasonId={season_id}",
                headers = self.new_headers,
                include_default_headers = False,
            ).json()["Items"][episode.episode - 1]["Id"]

            url = f"{self.base_url}/Items/{itemId}/Download?api_key={self.api_key}"

            return Multi(
                url = url, 
                title = metadata.title,
                episode = episode
            )

        itemId = metadata.id

        url = f"{self.base_url}/Items/{itemId}/Download?api_key={self.api_key}"

        return Single(
            url = url, 
            title = metadata.title, 
            year = metadata.year
        )

class InvalidLogin(MovCliException):
    """Raises when the jellyfin scraper fails while auth with server."""

    def __init__(self, user: str) -> None:
        super().__init__(
            f"Invalid Login for user: {user}",
        )
