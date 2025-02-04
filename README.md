<div align="center">

  # 🪼📺 mov-cli-jellyplex 
  <sub>A mov-cli v4 plugin for watching content from a media server hosting jellyfin or plex.</sub>

</div>

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
jelly = "mov-cli-jellyplex"
```

## Usage 🖱️
1. Set your environment variables

> See this [page](https://github.com/mov-cli/mov-cli/wiki/Configuration#environment-variables) on how to edit them.

These environment variables should be set:
- Jellyfin
  ```env
  JELLY_URL = "http://ip/"
  JELLY_USERNAME = "example"
  JELLY_PASSWORD = "example"
  ```

- Plex
  ```env
  PLEX_SERVER_ID="example"
  PLEX_USERNAME="example"
  PLEX_PASSWORD="example"
  ```

2. Usage

**Jellyfin**:
```sh
mov-cli -s jelly {query}
```

**Plex**:
```sh
mov-cli -s jelly.plex {query}
```

> [!NOTE]
> You can also override the jelly namespace to only use `jelly` instead of `jelly.plex`:
> ```toml
> [mov-cli.scrapers]
> jelly = "jellyplex.plex"
>
> [mov-cli.plugins]
> jellyplex = "mov-cli-jellyplex"
>```
