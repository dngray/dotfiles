/*** MY OVERRIDES ***/
user_pref("_user.js.parrot", "overrides section syntax error");

/* 4501: enable privacy.resistFingerprinting [FF41+]
 * [SETUP-WEB] RFP can cause some website breakage: mainly canvas, use a site exception via the urlbar
 * RFP also has a few side effects: mainly timezone is UTC0, and websites will prefer light theme
 * [1] https://bugzilla.mozilla.org/418986 ***/
user_pref("privacy.resistFingerprinting", false);

/* Set proxy configuration settings */
user_pref("network.proxy.type", 1);
user_pref("network.proxy.socks", "localhost");
user_pref("network.proxy.socks_port", 8881);
user_pref("network.proxy.socks_remote_dns", true);

/* Disable DoH */
user_pref("network.trr.mode", 5); // 0710

/* APPEARANCE ***/
user_pref("toolkit.legacyUserProfileCustomizations.stylesheets", true); // [FF68+] allow userChrome/userContent
user_pref("browser.tabs.inTitlebar", 0); // Disable title bar

/* THEME ***/
user_pref("extensions.activeThemeID", "cheers-bold-colorway@mozilla.org");
user_pref("browser.theme.toolbar-theme", 0);
user_pref("browser.theme.content-theme", 0);

/* UX FEATURES ***/
user_pref("extensions.pocket.enabled", false); // Pocket Account [FF46+]

/* 9001: Turn off previews when tabbing ***/
user_pref("browser.ctrlTab.recentlyUsedOrder", false);
/* 9002: Lazy loading: Tridactyl cannot capture key presses until web pages are loaded. ***/
user_pref("browser.sessionstore.restore_tabs_lazily", false);
/* 9003: Enable root certs for local CA ***/
user_pref("security.enterprise_roots.enabled", true);

user_pref("_user.js.parrot", "overrides section successful");
