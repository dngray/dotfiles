/*** MY OVERRIDES ***/
user_pref("_user.js.parrot", "overrides section syntax error");

/* Set proxy configuration settings */
user_pref("network.proxy.type", 1);
user_pref("network.proxy.socks", "localhost");
user_pref("network.proxy.socks_port", 8881);
user_pref("network.proxy.socks_remote_dns", true);

/* Use resistFingerprinting on 128 */
user_pref("privacy.resistFingerprinting", true);
user_pref("privacy.resistFingerprinting.letterboxing", true); // optional
user_pref("webgl.disabled", true); // optional
user_pref("privacy.spoof_english", 2); // optional
   // ^ I have en-US app lang and a non-matching en-** OS
  //  so my locale without spoof_english is the same as OS which is not desirable

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

/* Disable the Privacy-Preserving Attribution
 * https://github.com/mozilla/explainers/tree/main/ppa-experiment
 * https://github.com/arkenfox/user.js/issues/1854 */
user_pref("dom.private-attribution.submission.enabled", false); // [FF128+]

user_pref("_user.js.parrot", "overrides section successful");
