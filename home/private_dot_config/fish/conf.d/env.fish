# vim: filetype=fish
# .config/fish/conf.d/env.fish

# Environmental Variables
## User Directories
## https://wiki.archlinux.org/index.php/XDG_Base_Directory_support
set -gx XDG_CONFIG_HOME $HOME/.config
set -gx XDG_CACHE_HOME $HOME/.cache
set -gx XDG_DATA_HOME $HOME/.local/share
set -gx XDG_STATE_HOME $HOME/.local/state

## Set default FZF command
## https://medium.com/@sidneyliebrand/how-fzf-and-ripgrep-improved-my-workflow-61c7ca212861
set -gx FZF_DEFAULT_COMMAND "rg --files --no-ignore-vcs --hidden"

## Default editor
set -gx EDITOR nvim
set -gx SVN_EDITOR nvim

set -gx MC_SKIN "$XDG_DATA_HOME/mc/skins/nord16M.ini"
set -gx TERM xterm-256color

set -gx ANDROID_SDK_ROOT "$HOME/Android/Sdk"

set -gx PATH "$PATH:$HOME/.local/bin $HOME/.asdf/bin $HOME/.asdf/shims $HOME/.npm-global/bin $ANDROID_SDK_ROOT/platform-tools $HOME/.cargo/bin"
set -gx NPM_CONFIG_PREFIX "$HOME/.npm-global"
set -gx VAULT_ADDR "https://vault.den.home.arpa"
