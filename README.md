<div align="center">

  # mov-cli-ms
  <sub>A mov-cli v4 plugin for watching content from your media server.</sub>

</div>

> [!NOTE]
> WIP, Currently only Jellyfin works

## Installation 🛠️
Here's how to install and add the plugin to mov-cli.

1. Install it.
### PIP
```sh
pip install mov-cli-ms
```

### Arch
```sh
yay -S python-mov-cli-ms
```

2. Then add the plugin to your mov-cli config.
```sh
mov-cli -e
```
```toml
[mov-cli.plugins]
ms = "mov-cli-ms"
```

## Usage 🖱️
```sh
mov-cli -s ms {query} -- --url "jellyfin url" --username "your jellyfin username" --password "your jellyfin password"
```
