/*** MY OVERRIDES ***/
user_pref("_user.js.parrot", "overrides section syntax error");

/* --- SHARED SETTINGS FOR ALL PROFILES --- */
/* Disable DoH */
user_pref("network.trr.mode", 5); // 0710

/* APPEARANCE ***/
user_pref("browser.tabs.inTitlebar", 0); // Disable title bar
user_pref("sidebar.verticalTabs", true); // [FF136+] [DEFAULT: false]

/* UX FEATURES ***/
user_pref("extensions.pocket.enabled", false); // Pocket Account [FF46+]

/* 9001: Turn off previews when tabbing ***/
user_pref("browser.ctrlTab.recentlyUsedOrder", false);
/* 9002: Enable root certs for local CA ***/
user_pref("security.enterprise_roots.enabled", true);

/* Disable the Privacy-Preserving Attribution
 * https://github.com
 * https://github.com */
user_pref("dom.private-attribution.submission.enabled", false); // [FF128+]


/* --- PROXY SETTINGS (DIRECT PROFILES ONLY) --- */
{{ if .is_direct -}}
/* Set proxy configuration settings */
user_pref("network.proxy.type", 1);
user_pref("network.proxy.socks", "localhost");
user_pref("network.proxy.socks_port", 8881);
user_pref("network.proxy.socks_remote_dns", true);
{{ end -}}


/* --- HISTORY RETENTION (RFP ACTIVE OR DEFAULT PROFILE ONLY) --- */
{{ if or .rfp (not .is_direct) -}}
/* keep tabs and history between reboots */
user_pref("browser.startup.page", 3); // 0102
user_pref("privacy.clearHistory.browsingHistoryAndDownloads", false);
user_pref("privacy.clearHistory.formdata", true);
user_pref("privacy.clearOnShutdown_v2.browsingHistoryAndDownloads", false);
user_pref("privacy.clearOnShutdown_v2.downloads", true);
user_pref("privacy.clearOnShutdown_v2.formdata", true);
user_pref("privacy.clearSiteData.browsingHistoryAndDownloads", false);
user_pref("privacy.clearSiteData.formdata", true);
{{ end -}}


/* --- RESIST FINGERPRINTING LOGIC --- */
{{ if .rfp -}}
/* Use resistFingerprinting on 128 */
user_pref("privacy.resistFingerprinting", true);
user_pref("privacy.resistFingerprinting.letterboxing", true);
user_pref("webgl.disabled", true);
user_pref("privacy.spoof_english", 2);
{{ else -}}
/* override recipe: RFP is not for me ***/
user_pref("privacy.resistFingerprinting", false); // 4501
user_pref("privacy.resistFingerprinting.letterboxing", false); // 4504 [pointless if not using RFP]
user_pref("webgl.disabled", false); // 4520 [mostly pointless if not using RFP]
{{ end -}}


/* --- THEMES --- */
{{ if .is_direct -}}
/* THEME (All Direct Profiles) */
user_pref("extensions.activeThemeID", "cheers-bold-colorway@mozilla.org");
user_pref("browser.theme.toolbar-theme", 0);
user_pref("browser.theme.content-theme", 0);
{{ else if not .rfp -}}
/* THEME (Default No-RFP Profile Only) */
user_pref("extensions.activeThemeID", "foto-balanced-colorway@mozilla.org");
user_pref("browser.theme.toolbar-theme", 0);
user_pref("browser.theme.content-theme", 1);
{{ end -}}

user_pref("_user.js.parrot", "overrides section successful");
