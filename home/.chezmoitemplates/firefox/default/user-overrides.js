/*** MY OVERRIDES ***/
user_pref("_user.js.parrot", "overrides section syntax error");

/* override recipe: enable session restore ***/
user_pref("browser.startup.page", 3); // 0102
  // user_pref("browser.privatebrowsing.autostart", false); // 0110 required if you had it set as true
  // user_pref("places.history.enabled", true); // 0862 required if you had it set as false
  // user_pref("browser.sessionstore.privacy_level", 0); // 1021 optional [to restore extras like cookies/formdata]
user_pref("privacy.clearOnShutdown.history", false); // 2803
  // user_pref("privacy.clearOnShutdown.cookies", false); // 2803 optional
  // user_pref("privacy.clearOnShutdown.formdata", false); // 2803 optional
user_pref("privacy.cpd.history", false); // 2804 to match when you use Ctrl-Shift-Del
  // user_pref("privacy.cpd.cookies", false); // 2804 optional
  // user_pref("privacy.cpd.formdata", false); // 2804 optional

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

user_pref("_user.js.parrot", "overrides section successful");
