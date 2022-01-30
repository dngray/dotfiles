# vim: filetype=fish
# .config/fish/conf.d/gpg

## Recommended by GPG agent to resolve issues with not being able to use gpg2.
set -gx GPG_TTY (tty)

## gpg config with Yubikey
## https://opensource.com/article/19/4/gpg-subkeys-ssh
set -gx SSH_AUTH_SOCK (gpgconf --list-dirs agent-ssh-socket)

gpgconf --launch gpg-agent
gpg-connect-agent updatestartuptty /bye >/dev/null
