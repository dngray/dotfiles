# vim: filetype=fish
# .config/fish/conf.d/aliases.fish

set -l bash_aliases "$HOME/.bashrc.d/80_aliases"

if test -f $bash_aliases
    source $bash_aliases
end
