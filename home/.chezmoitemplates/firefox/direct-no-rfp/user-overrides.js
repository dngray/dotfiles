/*** MY OVERRIDES ***/
user_pref("_user.js.parrot", "overrides section syntax error");

/* override recipe: RFP is not for me ***/
user_pref("privacy.resistFingerprinting", false); // 4501
user_pref("privacy.resistFingerprinting.letterboxing", false); // 4504 [pointless if not using RFP]
user_pref("webgl.disabled", false); // 4520 [mostly pointless if not using RFP]

/* Set proxy configuration settings */
user_pref("network.proxy.type", 1);
user_pref("network.proxy.socks", "localhost");
user_pref("network.proxy.socks_port", 8881);
user_pref("network.proxy.socks_remote_dns", true);

/* Disable DoH */
user_pref("network.trr.mode", 5); // 0710

/* APPEARANCE ***/
user_pref("browser.tabs.inTitlebar", 0); // Disable title bar
user_pref("sidebar.verticalTabs", true); // [FF136+] [DEFAULT: false]
// user_pref("toolkit.legacyUserProfileCustomizations.stylesheets", true); // [FF68+] allow userChrome/userContent

/* THEME ***/
user_pref("extensions.activeThemeID", "cheers-bold-colorway@mozilla.org");
user_pref("browser.theme.toolbar-theme", 0);
user_pref("browser.theme.content-theme", 0);

/* UX FEATURES ***/
user_pref("extensions.pocket.enabled", false); // Pocket Account [FF46+]

/* 9001: Turn off previews when tabbing ***/
user_pref("browser.ctrlTab.recentlyUsedOrder", false);
/* 9002: Enable root certs for local CA ***/
user_pref("security.enterprise_roots.enabled", true);

/* Disable the Privacy-Preserving Attribution
 * https://github.com/mozilla/explainers/tree/main/ppa-experiment
 * https://github.com/arkenfox/user.js/issues/1854 */
user_pref("dom.private-attribution.submission.enabled", false); // [FF128+]

user_pref("_user.js.parrot", "overrides section successful");
