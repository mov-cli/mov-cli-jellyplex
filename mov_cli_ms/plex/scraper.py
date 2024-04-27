from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional, Dict, Generator, Any

    from mov_cli import Config
    from mov_cli.http_client import HTTPClient
    from mov_cli.scraper import ScraperOptionsT

from mov_cli import Single, Multi, Metadata

from mov_cli.scraper import Scraper
from mov_cli.utils import EpisodeSelector

__all__ = ("PlexScraper", )

class PlexScraper(Scraper):
    def __init__(self, config: Config, http_client: HTTPClient, options: Optional[ScraperOptionsT] = None) -> None:
        self.base_url = ...

        super().__init__(config, http_client, options)

    def search(self, query: str, limit: int = 20) -> Generator[Metadata, Any, None]:
        ...

    def scrape_metadata_episodes(self, metadata: Metadata) -> Dict[int, int] | Dict[None, int]:
        ...
    
    def scrape(self, metadata: Metadata, episode: EpisodeSelector) -> Single | Multi:
        ...