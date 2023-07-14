# vim: filetype=fish
# .config/fish/conf.d/gpg

## Recommended by GPG agent to resolve issues with not being able to use gpg2.
set -gx GPG_TTY (tty)

gpgconf --launch gpg-agent
gpg-connect-agent updatestartuptty /bye >/dev/null
