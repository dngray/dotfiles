# ~/.config/fish/config.fish

# Ensure XDG variables have a fallback if Bash hasn't initialized them yet
set -q XDG_CONFIG_HOME; or set -gx XDG_CONFIG_HOME $HOME/.config

# ==============================================================================
# INTERACTIVE TERMINAL UTILITIES
# ==============================================================================
if status is-interactive

    # Prompt Initialization
    if type -q starship
        starship init fish | source
    end

    # Security (Window-specific TTY tracking with headless fallback)
    if tty >/dev/null 2>&1
        set -gx GPG_TTY (tty)
    end

    # Robust Dircolors Parser with local file fallback
    if type -q dircolors
        if test -f $XDG_CONFIG_HOME/dircolors/dir_colors
            eval (dircolors -c $XDG_CONFIG_HOME/dircolors/dir_colors | string collect)
        else
            eval (dircolors -c | string collect)
        end
    end

    # Modern, native colored man pages via less ANSI color variables
    set -gx LESS_TERMCAP_md (set_color -o 5fafd7) # Bold headers
    set -gx LESS_TERMCAP_us (set_color -u afafd7) # Underline options
    set -gx LESS_TERMCAP_so (set_color 949494) # Standout/Search highlights
    set -gx LESS_TERMCAP_mb (set_color -o red) # Blinking text
    set -gx LESS_TERMCAP_me (set_color normal) # Reset text
    set -gx LESS_TERMCAP_se (set_color normal) # Reset standout
    set -gx LESS_TERMCAP_ue (set_color normal) # Reset underline

    # Native Fish array configuration for pagers
    set -gx LESS -R -s
    set -gx MANPAGER "less -R -s"
    set -gx GROFF_NO_SGR 1 # Fix formatting on Fedora/RedHat systems
end
