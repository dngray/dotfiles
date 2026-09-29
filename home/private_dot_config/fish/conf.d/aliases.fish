# vim: filetype=fish
# ~/.config/fish/conf.d/aliases.fish
#
# The two files below are shared verbatim with bash, so they must stay
# POSIX-alias-only. If either ever gains bash-only syntax, fish rejects the whole
# file and every alias vanishes at once. Add shell-agnostic aliases there, not here.

set -l shared "$HOME/.bashrc.d"

test -f $shared/80_aliases; and source $shared/80_aliases
test -f $shared/85_aliases_vault; and source $shared/85_aliases_vault

# Fish-specific implementations (the bash h/f/p live in ~/.bashrc.d/90_bash_funcs)

# fish's history is already a search engine, so there is no pipe here.
function h --description 'search shell history'
    history search $argv
end

function f --description 'find files by name'
    set -l pattern (string join ' ' $argv)
    if command -q fd
        fd $pattern
    else
        find . -name "*$pattern*"
    end
end

# string match is a builtin, so there is no searching process to filter out.
# -e makes the pattern a substring match; -i because fish has no smart-case.
function p --description 'search running processes'
    if test (count $argv) -eq 0
        ps aux
        return
    end
    ps aux | string match -i -e -- (string join ' ' $argv)
end
