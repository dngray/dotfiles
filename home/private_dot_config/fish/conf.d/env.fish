# vim: filetype=fish
# .config/fish/conf.d/env.fish

# Environmental Variables
## User Directories
## https://wiki.archlinux.org/index.php/XDG_Base_Directory_support
set -gx XDG_CONFIG_HOME $HOME/.config
set -gx XDG_CACHE_HOME $HOME/.cache
set -gx XDG_DATA_HOME $HOME/.local/share

## Set default FZF command
## https://medium.com/@sidneyliebrand/how-fzf-and-ripgrep-improved-my-workflow-61c7ca212861
set -gx FZF_DEFAULT_COMMAND "rg --files --no-ignore-vcs --hidden"

## Default editor
if test $hostname = "toolbox"
    set -gx EDITOR "/usr/bin/nvim"
    set -gx SVN_EDITOR "/usr/bin/nvim"
else
    set -gx EDITOR "flatpak run io.neovim.nvim"
    set -gx SVN_EDITOR "flatpak run io.neovim.nvim"
end

set -gx MC_SKIN "$XDG_CONFIG_HOME/selenized/other-apps/mc/selenized.ini"
set -gx TERM xterm-256color

set -gx VAULT_ADDR "https://vault.den.home.arpa"

set -gx PATH "$PATH:$HOME/.local/bin"
