/*** MY OVERRIDES ***/
user_pref("_user.js.parrot", "overrides section syntax error");

/* override recipe: enable session restore ***/
user_pref("browser.startup.page", 3); // 0102
  // user_pref("browser.privatebrowsing.autostart", false); // 0110 required if you had it set as true
  // user_pref("browser.sessionstore.privacy_level", 0); // 1003 optional to restore cookies/formdata
user_pref("privacy.clearOnShutdown.history", false); // 2811
  // user_pref("privacy.cpd.history", false); // 2820 optional to match when you use Ctrl-Shift-Del
user_pref("privacy.clearOnShutdown_v2.historyFormDataAndDownloads", false); // [FF128+] [DEFAULT: true]

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
