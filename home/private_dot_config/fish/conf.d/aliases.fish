# vim: filetype=fish
# .config/fish/conf.d/aliases.fish

set -l bash_aliases "$HOME/.bashrc.d/80_aliases"
set -l fish_compiled "$HOME/.config/fish/conf.d/.aliases.compiled.fish"

# Only rebuild the native file if the Bash source file is newer
if test -f $bash_aliases
    if not test -f $fish_compiled; or test $bash_aliases -nt $fish_compiled
        # Fast text stream translation safely ignoring template loops
        echo "# Generated from $bash_aliases" >$fish_compiled

        # Strip out any lingering Bash-specific if/for template syntax,
        # convert backticks to Fish subshells, and write cleanly.
        sed -E \
            -e 's/`pwd -P`/\(pwd -P\)/g' \
            -e '/^if /d' -e '/^fi$/d' -e '/^for /d' -e '/^done$/d' \
            $bash_aliases >>$fish_compiled

        # Append clean Fish search overrides to fix the dangling Bash pipe bug
        echo 'function h; history | grep $argv; end' >>$fish_compiled
        echo 'function f; find . | grep $argv; end' >>$fish_compiled
        echo 'function p; ps aux | grep $argv; end' >>$fish_compiled
    end
    source $fish_compiled
end
