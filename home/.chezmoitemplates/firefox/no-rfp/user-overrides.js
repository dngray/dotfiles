/*** MY OVERRIDES ***/
user_pref("_user.js.parrot", "overrides section syntax error");

/* override recipe: RFP is not for me ***/
user_pref("privacy.resistFingerprinting", false); // 4501
user_pref("privacy.resistFingerprinting.letterboxing", false); // 4504 [pointless if not using RFP]
user_pref("webgl.disabled", false); // 4520 [mostly pointless if not using RFP]

/* Disable DoH */
user_pref("network.trr.mode", 5); // 0710

/* APPEARANCE ***/
user_pref("toolkit.legacyUserProfileCustomizations.stylesheets", true); // [FF68+] allow userChrome/userContent
user_pref("browser.tabs.inTitlebar", 0); // Disable title bar

/* THEME ***/
user_pref("extensions.activeThemeID", "foto-balanced-colorway@mozilla.org");
user_pref("browser.theme.toolbar-theme", 0);
user_pref("browser.theme.content-theme", 1);

/* UX FEATURES ***/
user_pref("extensions.pocket.enabled", false); // Pocket Account [FF46+]

/* 9001: Turn off previews when tabbing ***/
user_pref("browser.ctrlTab.recentlyUsedOrder", false);
/* 9002: Lazy loading: Tridactyl cannot capture key presses until web pages are loaded. ***/
user_pref("browser.sessionstore.restore_tabs_lazily", false);
/* 9003: Enable root certs for local CA ***/
user_pref("security.enterprise_roots.enabled", true);

user_pref("_user.js.parrot", "overrides section successful");
