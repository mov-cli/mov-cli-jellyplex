from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional, Dict, Generator, Any

    from mov_cli import Config
    from mov_cli.http_client import HTTPClient
    from mov_cli.scraper import ScraperOptionsT

from dataclasses import dataclass, field

from mov_cli import Single, Multi, Metadata, MetadataType

from mov_cli.scraper import Scraper
from mov_cli.utils import EpisodeSelector

from plexapi.myplex import MyPlexAccount
from plexapi.server import PlexServer
from plexapi.exceptions import TwoFactorRequired
from plexapi.video import Movie, Show
from plexapi.exceptions import Unauthorized

__all__ = (
    "PlexScraper",
    "PlexMetadata",
)


@dataclass
class PlexMetadata(Metadata):
    id: int
    video: Movie | Show = field(default=None)


class PlexScraper(Scraper):
    def __init__(
        self,
        config: Config,
        http_client: HTTPClient,
        options: Optional[ScraperOptionsT] = None,
    ) -> None:
        env_config = config.get_env_config()

        self.base_url = env_config("PLEX_SERVER_ID", default = None)
        self.username = env_config("PLEX_USERNAME", default = None)
        self.password = env_config("PLEX_PASSWORD", default = None)

        self.__authenticated_plex_server: Optional[PlexServer] = None

        super().__init__(config, http_client, options)

    def search(self, query: str, limit: Optional[int]) -> Generator[PlexMetadata, Any, None]:
        limit = 20 if limit is None else limit

        plex_server = self.__get_plex_server()

        if query in ["all+", "*"]:
            videos = plex_server.library.all()
        else:
            videos = plex_server.search(query, limit=limit)

        for id, video in enumerate(videos):
            if video.TYPE in ["movie", "show"]:
                yield PlexMetadata(
                    id = id,
                    title = video.title + f" ({video.librarySectionTitle})",
                    type = MetadataType.SINGLE if "movie" == video.TYPE else MetadataType.MULTI,
                    image_url = video.posterUrl,
                    year = video.year,
                    video = video
                )

    def scrape_episodes(self, metadata: PlexMetadata) -> Dict[int, int] | Dict[None, int]:
        scraped_episodes = {}

        seasons = metadata.video.seasons()

        for season in seasons:
            scraped_episodes[season.seasonNumber] = len(season.episodes())

        return scraped_episodes

    def scrape(self, metadata: PlexMetadata, episode: EpisodeSelector) -> Single | Multi:
        if metadata.type == MetadataType.MULTI:
            epi = metadata.video.episode(
                season = episode.season,
                episode = episode.episode
            )

            return Multi(
                url = self.__make_url(epi),
                title = metadata.title,
                episode = episode
            )

        return Single(
            url = self.__make_url(metadata.video),
            title = metadata.title,
            year = metadata.year
        )

    def __make_url(self, item) -> str:
        plex_server = self.__get_plex_server()

        key = next(item.iterParts()).key

        return item._server.url(
            f"{key}?download=1&X-Plex-Token={plex_server.account().authToken}"
        )

    def __get_plex_server(self) -> PlexServer:

        if self.__authenticated_plex_server is None:

            if self.base_url is None:
                raise Exception("You haven't set the 'PLEX_SERVER_ID' env!")

            if self.username is None:
                raise Exception("You haven't set the 'PLEX_USERNAME' env!")

            if self.password is None:
                raise Exception("You haven't set the 'PLEX_PASSWORD' env!")

            try:
                account = MyPlexAccount(self.username, self.password)

            except TwoFactorRequired:
                code = self.options.get("2FA")
                account = MyPlexAccount(self.username, self.password, code=code)

            except Unauthorized as e:
                raise Exception(
                    f"Failed to authenticate plex credentials! Error: {e}"
                )

            plex = account.resource(self.base_url).connect()

            self.__authenticated_plex_server = plex

        return self.__authenticated_plex_server