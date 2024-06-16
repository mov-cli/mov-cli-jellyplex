<div align="center">

  # 🪼📺 mov-cli-jellyplex 
  <sub>A mov-cli v4 plugin for watching content from a media server hosting jellyfin or plex.</sub>

</div>

> [!NOTE]
> WIP, Currently only Jellyfin works

## Installation 🛠️
Here's how to install and add the plugin to mov-cli.

1. Install it.
### PIP
```sh
pip install mov-cli-jellyplex
```

### AUR
```sh
yay -S python-mov-cli-jellyplex
```

2. Then add the plugin to your mov-cli config.
```sh
mov-cli -e
```
```toml
[mov-cli.plugins]
ms = "mov-cli-jellyplex"
```

## Usage 🖱️
1. Set your environment variables

> See this [page](https://github.com/mov-cli/mov-cli/wiki/Configuration#environment-variables) on how to edit them.

These environment variables should be set:
```env
JELLY_URL = "http://ip/"
JELLY_USERNAME = "example"
JELLY_PASSWORD = "example"
```

2. Usage
```sh
mov-cli -s jellyplex {query}
```