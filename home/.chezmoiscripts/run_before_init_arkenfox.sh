#!/usr/bin/env bash

CHEZMOI_ROOT="$XDG_DATA_HOME/chezmoi/home"
TEMPLATE_DIR="$CHEZMOI_ROOT/.chezmoitemplates/firefox"
ARKENFOX_DIR_NAME="arkenfox"
ARKENFOX_DIR="$TEMPLATE_DIR/$ARKENFOX_DIR_NAME"
ARKENFOX_NO_RFP_DIR_NAME="no-rfp"
ARKENFOX_NO_RFP_DIR="$TEMPLATE_DIR/$ARKENFOX_NO_RFP_DIR_NAME"
DIRECT_DIR_NAME="direct"
DIRECT_DIR="$TEMPLATE_DIR/$DIRECT_DIR_NAME"
DIRECT_NO_RFP_DIR_NAME="direct-no-rfp"
DIRECT_NO_RFP_DIR="$TEMPLATE_DIR/$DIRECT_NO_RFP_DIR_NAME"
SCRIPT_FILE="$ARKENFOX_DIR/updater.sh"

# Download method priority: curl -> wget
DOWNLOAD_METHOD=''
if command -v curl >/dev/null; then
  DOWNLOAD_METHOD='curl --max-redirs 3 -o'
elif command -v wget >/dev/null; then
  DOWNLOAD_METHOD='wget --max-redirect 3 -O'
else
  echo -e "${RED}This script requires curl or wget.\nProcess aborted${NC}"
  exit 1
fi

download_file() { # expects URL as argument ($1)
  declare -r tf=$(mktemp)

  $DOWNLOAD_METHOD "${tf}" "$1" && echo "$tf" || echo '' # return the temp-filename or empty string on error
}

update_updater() {
  declare -r tmpfile="$(download_file 'https://raw.githubusercontent.com/arkenfox/user.js/master/updater.sh')"
  [ -z "${tmpfile}" ] && echo -e "${RED}Error! Could not download updater.sh${NC}" && return 1 # check if download failed

  mv "${tmpfile}" "$SCRIPT_FILE"
  chmod u+x "$SCRIPT_FILE"
  "$SCRIPT_FILE" "$@" -d
  exit 0
}

update_profile() {
  if [ ! -f "$1"/user.js ]; then
    printf "user.js not found getting one\n"

    "$SCRIPT_FILE" "-b" "-d" "-s" \
    -o "$1"/user-overrides.js \
    -p "$1"
  else
    printf "$2/user.js found, reusing\n"
  fi
}

if [ ! -f "$SCRIPT_FILE" ]; then
  printf "updater.sh not found getting one\n"
  update_updater "$@"
elif [ "$(find "$SCRIPT_FILE" -mtime +120)" ]; then
  printf "File updater.sh exists and is older than 120 days, getting a new one\n"
  rm "$SCRIPT_FILE"
  update_updater "$@"
fi

update_profile "$ARKENFOX_DIR" "$ARKENFOX_DIR_NAME"
update_profile "$ARKENFOX_NO_RFP_DIR" "$ARKENFOX_NO_RFP_DIR_NAME"
update_profile "$DIRECT_DIR" "$DIRECT_DIR_NAME"
update_profile "$DIRECT_NO_RFP_DIR" "$DIRECT_NO_RFP_DIR_NAME"
