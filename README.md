<div align="center">

  # example-plugin 
  <sub>A boilerplate for creating mov-cli v4 plugins.</sub>

</div>

## Installation for development.
Here's how to install and add the plugin to mov-cli for development.

1. Clone the repo.
```sh
git clone https://github.com/mov-cli/example-plugin.git
cd example-plugin
```

2. Install in editable mode.
```sh
make install-editable
```
> **or** ``pip install -e . --config-settings editable_mode=compat``

3. Add the plugin to mov-cli.
```sh
mov-cli -e
```
```toml
[mov-cli.plugins]
namespace = "package_name" # check out the wiki for more: https://github.com/mov-cli/mov-cli/wiki/Plugins#%EF%B8%8F-how-to-install-plugins
```

4. Create away. 😊

<br>

> The [mov-cli-test](https://github.com/mov-cli/mov-cli-test) and [mov-cli-youtube](https://github.com/mov-cli/mov-cli-youtube) plugins are great resources for learning the ins and outs of mov-cli plugin development.
