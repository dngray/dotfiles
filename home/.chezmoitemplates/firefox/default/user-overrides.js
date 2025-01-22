/*** MY OVERRIDES ***/
user_pref("_user.js.parrot", "overrides section syntax error");

/* override recipe: enable session restore ***/
user_pref("browser.startup.page", 3); // 0102

/* keep tabs and history between reboots */
user_pref("privacy.clearHistory.browsingHistoryAndDownloads", false);
user_pref("privacy.clearHistory.formdata", true);
user_pref("privacy.clearOnShutdown_v2.browsingHistoryAndDownloads", false);
user_pref("privacy.clearOnShutdown_v2.downloads", true);
user_pref("privacy.clearOnShutdown_v2.formdata", true);
user_pref("privacy.clearSiteData.browsingHistoryAndDownloads", false);
user_pref("privacy.clearSiteData.formdata", true);

/* Use resistFingerprinting on 128 */
user_pref("privacy.resistFingerprinting", true);
user_pref("privacy.resistFingerprinting.letterboxing", true);
user_pref("webgl.disabled", true);
user_pref("privacy.spoof_english", 2);

/* Disable DoH */
user_pref("network.trr.mode", 5); // 0710

/* APPEARANCE ***/
user_pref("browser.tabs.inTitlebar", 0); // Disable title bar
user_pref("sidebar.verticalTabs", true); // [FF136+] [DEFAULT: false]
// user_pref("toolkit.legacyUserProfileCustomizations.stylesheets", true); // [FF68+] allow userChrome/userContent

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
