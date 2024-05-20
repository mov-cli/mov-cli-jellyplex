from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional, Dict, Generator, Any

    from mov_cli import Config
    from mov_cli.http_client import HTTPClient
    from mov_cli.scraper import ScraperOptionsT

from mov_cli import Single, Multi, Metadata, MetadataType

from mov_cli.scraper import Scraper
from mov_cli.utils import EpisodeSelector

from plexapi.myplex import MyPlexAccount
from plexapi.server import PlexServer
from plexapi.exceptions import TwoFactorRequired

__all__ = ("PlexScraper", )

class PlexScraper(Scraper):
    def __init__(self, config: Config, http_client: HTTPClient, options: Optional[ScraperOptionsT] = None) -> None:
        env_config = config.get_env_config()

        self.base_url = env_config("PLEX_SERVER_ID", default = None, cast = str)
        self.username = env_config("PLEX_USERNAME", default = None, cast = str)
        self.password = env_config("PLEX_PASSWORD", default = None, cast = str)

        self.plex: PlexServer = self.__auth()

        super().__init__(config, http_client, options)


    def search(self, query: str, limit: int = 20) -> Generator[Metadata, Any, None]:
        videos = self.plex.search(query, limit = limit)

        for video in videos:
            if video.TYPE in ["movie", "show"]:
                yield Metadata(
                    id = video,
                    title = video.title,
                    type = MetadataType.SINGLE if "movie" == video.TYPE else MetadataType.MULTI,
                    year = video.year,
                )

    def scrape_episodes(self, metadata: Metadata) -> Dict[int, int] | Dict[None, int]:
        scraped_episodes = {}

        seasons = metadata.id.seasons()

        for season in seasons:
            scraped_episodes[season.seasonNumber] = len(season.episodes())

        return scraped_episodes

    def scrape(self, metadata: Metadata, episode: EpisodeSelector) -> Single | Multi:
        if metadata.type == MetadataType.MULTI:
            epi = metadata.id.episode(season = episode.season, episode = episode.episode)

            return Multi(
                url = self.__make_url(epi),
                title = metadata.title,
                episode = episode
            )
        
        return Single(
            url = self.__make_url(metadata.id),
            title = metadata.title,
            year = metadata.year
        )

    def __make_url(self, item):
        key = next(item.iterParts()).key

        return item._server.url(f"{key}?download=1&X-Plex-Token={self.plex.account().authToken}")

    def __auth(self):
        try:
            account = MyPlexAccount(self.username, self.password)
        except TwoFactorRequired:
            code = self.options.get("2FA")
            account = MyPlexAccount(self.username, self.password, code=code)

        plex = account.resource(self.base_url).connect()

        return plex