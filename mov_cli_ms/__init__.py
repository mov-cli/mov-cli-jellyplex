from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mov_cli.plugins import PluginHookData

from .jellyfin.scraper import *

plugin: PluginHookData = {
    "version": 1, # plugin hook version
    "package_name": "mov-cli-ms", # pypi package name
    "scrapers": {
        "DEFAULT": JellyfinScraper, 
        "jellyfin": JellyfinScraper
    }
}

__version__ = "1.0.0"