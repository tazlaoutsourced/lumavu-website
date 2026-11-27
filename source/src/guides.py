# Guide pages: the "best IPTV player" pillar, the iPhone Duo cluster, how-to pages, and the rewritten Jellyfin
# and iPhone Duo pages. Facts about other apps come only from their App Store listings, release notes or
# developer sites, read on CHECKED, and the copy says where each fact came from.
#
# House rules for Lumavu copy: it's a player only. Don't mention what people watch (no "channels", no
# "providers", nothing free to watch). Always list iPhone Duo with the other devices. Download links go to STORE.

import compare
from compare import STORE, CTA, TRY, TIVIMATE, SMARTERS

CHECKED = "27 November 2026"
SITE_UPDATED = "2026-11-27"

PILLAR = "best-iptv-player-iphone-ipad-apple-tv.html"
DUO = "best-iptv-player-iphone-duo.html"
DUO_APPS = "iphone-duo-video-player-apps.html"
M3U = "m3u-player-iphone.html"
XTREAM = "xtream-codes-player-apple-tv.html"
JELLY = "best-jellyfin-player-apple-tv.html"

AS = {
    "uhf": "https://apps.apple.com/us/app/uhf-love-your-iptv-player/id6443751726",
    "iptvx": "https://apps.apple.com/us/app/iptvx/id1451470024",
    "smarters": "https://apps.apple.com/us/app/smarters-player-lite/id1628995509",
    "iplaytv": "https://apps.apple.com/us/app/iplaytv/id1072226801",
    "gse": "https://apps.apple.com/us/app/gse-smart-iptv-pro/id6443923265",
    "infuse": "https://apps.apple.com/us/app/infuse/id1136220934",
    "swiftfin": "https://apps.apple.com/us/app/swiftfin/id1604098728",
    "chromareel": "https://apps.apple.com/us/app/chromareel/id6837356606",
    "swiptv": "https://apps.apple.com/gb/app/swiptv-iptv-player/id1658538188",
}


def a(url, text):
    return f'<a href="{url}" target="_blank" rel="noopener">{text}</a>'


def L(fname, text):
    """An internal link to another page on this site, by its clean address."""
    return f'<a href="/{fname[:-5]}">{text}</a>'


ALSO = f"""
<h2 id="also">More guides</h2>
<ul class="also-list">
  <li>{L(PILLAR, "Best IPTV player apps for iPhone, iPad and Apple TV")} — UHF, IPTVX, Smarters Player Lite, iPlayTV, GSE and Lumavu side by side</li>
  <li>{L(DUO, "Best IPTV player for iPhone Duo")} — book, tabletop and Multiview at the fold</li>
  <li>{L(DUO_APPS, "Video and IPTV player apps made for iPhone Duo")} — which ones are built for the fold</li>
  <li>{L(M3U, "M3U player for iPhone and iPad")} — how to open an M3U or M3U8 link</li>
  <li>{L(XTREAM, "Xtream Codes player for Apple TV")} — signing in with a server, username and password</li>
  <li>{L(JELLY, "Jellyfin players for Apple TV")} — Swiftfin, Infuse, Chromareel and Lumavu, after Prism</li>
  <li>{L("lumavu-vs-tivimate.html", "Lumavu vs TiviMate")} — for people moving from Android TV</li>
  <li>{L("iptv-smarters-alternative.html", "An IPTV Smarters alternative")} — without ads or an account</li>
</ul>
"""

PLAYER_ONLY = "Lumavu is a player only: it does not include, sell or recommend anything to watch."
TM_APPLE = "Apple, iPhone, iPhone Duo, iPad, Apple TV, AirPlay and App Store are trademarks of Apple Inc."

# The two older comparison pages get the full, clean-address guide list
TIVIMATE = TIVIMATE.replace(compare.ALSO, ALSO)
SMARTERS = SMARTERS.replace(compare.ALSO, ALSO)

# ---------------------------------------------------------------------------------------------------------------
# Pillar: best IPTV player apps for iPhone, iPad and Apple TV
# ---------------------------------------------------------------------------------------------------------------

PILLAR_HTML = f"""
<p class="updated">Checked {CHECKED}. Every fact about another app comes from its US App Store listing or release notes on that day, and each name links to the listing. Prices are the US or UK App Store prices shown, and vary by country.</p>
<div class="summary">
  <p><strong>Disclosure first.</strong> We make Lumavu, one of the players below. We've tried to describe every other app the way its own listing does, and to say plainly where Lumavu falls short.</p>
  <p><strong>The short version.</strong> On Apple devices, the established picks are <strong>UHF</strong> (the most actively updated, with Plex, Jellyfin and Emby too) and <strong>IPTVX</strong> (polished, with iCloud sync, but free with ads). <strong>Smarters Player Lite</strong> is the one most people already know. <strong>Lumavu</strong> is the newest: free with no account and no ads, it adds Jellyfin and Emby to M3U and Xtream, and it has the most complete layout for iPhone Duo we found. TiviMate isn't on Apple devices at all.</p>
</div>

<h2 id="pick">Quick picks</h2>
<ul>
  <li><strong>Best all-rounder on Apple TV:</strong> {a(AS["uhf"], "UHF")}. Updated on 24 November 2026, with M3U8, Xtream, Plex, Jellyfin and Emby, Chromecast and AirPlay, downloads and Multiview.</li>
  <li><strong>Best on iPhone Duo:</strong> Lumavu. Book and tabletop layouts, Multiview that splits at the fold, and playback that carries on as you open or close it. See {L(DUO, "Lumavu on iPhone Duo")}.</li>
  <li><strong>Best free player with no ads and no account:</strong> Lumavu. The free app has no ads, and the App Store privacy label says no data is collected.</li>
  <li><strong>Most polished media-library look:</strong> {a(AS["iptvx"], "IPTVX")}, if you don't mind ads on the free tier or a subscription.</li>
  <li><strong>The one most guides are written for:</strong> {a(AS["smarters"], "Smarters Player Lite")}, with about 458,000 ratings.</li>
  <li><strong>Pay once, no subscription:</strong> {a(AS["iplaytv"], "iPlayTV")} ($5.99), though it hasn't been updated since September 2025.</li>
</ul>

<h2 id="compare">The players compared</h2>
<div class="cmp-wrap">
<table class="cmp wide">
  <thead>
    <tr><th scope="col">App</th><th scope="col">Devices</th><th scope="col">What you can add</th><th scope="col">iPhone Duo</th><th scope="col">Price</th><th scope="col">Ads and tracking</th><th scope="col">Last update · needs</th></tr>
  </thead>
  <tbody>
    <tr><th scope="row">Lumavu</th><td>iPhone, iPhone Duo, iPad, Apple TV (Mac to follow)</td><td>M3U, Xtream Codes, Jellyfin, Emby</td><td>Made for it: book, tabletop, open and closed layouts; Multiview splits at the fold</td><td>Free; Pro £2.99/month, £19.99/year or £49.99 once (UK)</td><td>No ads, no account. Privacy label: data not collected</td><td>20 Nov 2026 · iOS and tvOS 18</td></tr>
    <tr><th scope="row">{a(AS["uhf"], "UHF")}</th><td>iPhone, iPad, Apple TV</td><td>M3U8, Xtream, Plex, Jellyfin, Emby</td><td>Release notes (2.5.0, 31 Oct): "various changes to better support" iPhone Duo</td><td>Free; Pro $1.99/month, $17.99/year or $49.99 lifetime (US)</td><td>Listing: Pro has "zero ads and watermarks"</td><td>24 Nov 2026 · iOS 16</td></tr>
    <tr><th scope="row">{a(AS["iptvx"], "IPTVX")}</th><td>iPhone, iPad, Apple TV</td><td>Xtream, M3U, M3U8, Plex, SMB</td><td>Not mentioned in the listing</td><td>Free with ads; Full from $3.99/month or $28.99/year (US)</td><td>Privacy label includes "Data Used to Track You"</td><td>22 Nov 2026 · iOS 16</td></tr>
    <tr><th scope="row">{a(AS["smarters"], "Smarters Player Lite")}</th><td>iPhone, iPad, Apple TV</td><td>M3U, JSON and "other standard formats"</td><td>Not mentioned in the listing</td><td>Free; Premium $1.99 once (US)</td><td>Privacy label includes "Data Used to Track You"</td><td>26 Nov 2026 · iOS 15.6</td></tr>
    <tr><th scope="row">{a(AS["iplaytv"], "iPlayTV")}</th><td>iPhone, iPad, Apple TV</td><td>Xtream, M3U</td><td>Not mentioned</td><td>$5.99 once (US)</td><td>Paid app</td><td>24 Sep 2025 · iOS 18.6</td></tr>
    <tr><th scope="row">{a(AS["gse"], "GSE Smart IPTV Pro")}</th><td>iPhone, iPad</td><td>M3U, JSON, Xtream</td><td>Not mentioned</td><td>$2.99 once (US)</td><td>Paid app</td><td>14 Nov 2022 · iOS 9</td></tr>
  </tbody>
</table>
</div>
<p>"Not mentioned" means the listing doesn't say. It doesn't prove the app looks wrong on iPhone Duo, so try it before you pay.</p>

<h2 id="lumavu">Lumavu</h2>
<p>Lumavu is a player for iPhone, iPhone Duo, iPad and Apple TV. You add an M3U link, an Xtream Codes login, or a Jellyfin or Emby server, and Lumavu lays it out with a TV guide, catch-up where your source offers it, resume, favourites and a PIN lock on categories.</p>
<ul>
  <li><strong>It works out what you've given it.</strong> If an M3U link is really an Xtream account underneath, Lumavu notices and signs in as Xtream, so you also get the films, series and catch-up the account has.</li>
  <li><strong>One entry, not three.</strong> When the same stream appears in 4K, HD and SD, Lumavu shows it once. If one copy fails, it tries the next copy by itself.</li>
  <li><strong>Live subtitles.</strong> Subtitles are written on the device from what's being said, and on iPhone and iPad (iOS 26 and later) they can be translated as they go.</li>
  <li><strong>Made for iPhone Duo.</strong> Hold it like a book and the sidebar fills the left half, clear of the crease. Stand it on a table and the picture sits on top with the controls on the base. {L(DUO, "More on iPhone Duo")}.</li>
  <li><strong>Jellyfin and Emby.</strong> Films and series from your own server, next to your playlists. Live TV from Jellyfin or Emby isn't there yet.</li>
</ul>
<p><strong>Free:</strong> one playlist on each device, one favourites list, and the guide from yesterday to tomorrow, with no ads and no account. <strong>Lumavu Pro</strong> adds iCloud sync, the whole week's guide with reminders and your own XMLTV guides, Multiview (up to four at once), recordings, offline downloads on iPhone and iPad (your place carries over to the streamed copy), and as many playlists as you like.</p>
<p><strong>Where it falls short:</strong> it's new, with only a handful of App Store ratings so far. It needs iOS and tvOS 18, so older Apple TVs that stop at tvOS 17 can't run it. There's no Chromecast and no Plex, recordings only run while the app is open, and Apple TV writes live subtitles but doesn't translate them.</p>
{CTA}

<h2 id="uhf">UHF</h2>
<p>{a(AS["uhf"], "UHF")}, from Short Wavelength Applications, is the most actively updated player here: version 2.10.0 arrived on 24 November 2026. Its listing names M3U8, Xtream, Plex, Jellyfin and Emby, a resizable Picture in Picture, downloads, AirPlay and Chromecast, CarPlay while parked, Multiview, and recording through a free UHF Server companion app on a Mac, Windows or Linux computer. Pro ($1.99 a month, $17.99 a year or $49.99 lifetime in the US) adds multi-device sync and removes ads. It runs back to iOS 16, and it's rated 4.7 from about 3,400 ratings.</p>
<p><strong>Choose UHF if</strong> you want the longest feature list and Chromecast, or your Apple TV is older than tvOS 18.</p>

<h2 id="iptvx">IPTVX</h2>
<p>{a(AS["iptvx"], "IPTVX")}, from Bending X, has a polished media-library look, iCloud sync, Plex and SMB shares, Dolby Vision and HDR10, multi-screen viewing and an offline mode on iOS. The free tier is "Free with Ads", where watching a video ad can unlock more viewing time; the Full subscription starts at $3.99 a month or $28.99 a year in the US. Its privacy label includes data used to track you. It's rated 4.4 from about 3,200 ratings.</p>
<p><strong>Choose IPTVX if</strong> the look matters most and you're happy to subscribe.</p>

<h2 id="smarters">Smarters Player Lite</h2>
<p>{a(AS["smarters"], "Smarters Player Lite")}, from WHMCS Smarters, is the official Apple version of the name most people are given when they first set up a player, with about 458,000 ratings at 4.8. It takes M3U and JSON playlists, gained EPG reminders in its 26 November update, and has a one-off $1.99 Premium upgrade. Its privacy label includes data used to track you. Several lookalike apps use similar names, so check the developer. We wrote a separate {L("iptv-smarters-alternative.html", "IPTV Smarters alternative")} page.</p>

<h2 id="iplaytv">iPlayTV</h2>
<p>{a(AS["iplaytv"], "iPlayTV")}, by Andre Silva, is a paid app ($5.99 in the US) with no subscription, and its listing names Xtream, a TV guide, catch-up and AirPlay. The last update was on 24 September 2025, and it now needs iOS 18.6. Pay once if you like that model, but check it works with your playlist first.</p>

<h2 id="gse">GSE Smart IPTV Pro</h2>
<p>{a(AS["gse"], "GSE Smart IPTV Pro")} ($2.99) is a long-standing player with M3U, JSON and Xtream, an XMLTV guide, AirPlay, Chromecast and recording. The App Store shows its last update on 14 November 2022, so expect rough edges on new devices. Several unrelated apps now use "GSE" in their names.</p>

<h2 id="android">TiviMate, Televizo and other Android players</h2>
<p>TiviMate and Televizo are Android players. Neither has an official App Store app, and apps with similar names on the App Store come from unrelated developers. If you're moving from TiviMate, see {L("lumavu-vs-tivimate.html", "Lumavu vs TiviMate")}.</p>

<h2 id="servers">If you mostly use Jellyfin, Emby or Plex</h2>
<p>A dedicated media-server client may suit you better than an IPTV player. Swiftfin is the official Jellyfin app, Infuse covers Jellyfin, Emby, Plex and network shares, and Chromareel is a new Jellyfin app made for iPhone Duo. Prism, a popular hub app, stopped working around 16 November 2026. We compare them in {L(JELLY, "Jellyfin players for Apple TV")}.</p>

<h2 id="choose">How to choose</h2>
<ol class="steps">
  <li><span><strong>Check what you've been given.</strong> An M3U or M3U8 link, an Xtream Codes login (server, username and password), or a media server. Most players take the first two. See {L(M3U, "M3U on iPhone")} and {L(XTREAM, "Xtream Codes on Apple TV")}.</span></li>
  <li><span><strong>Check your oldest device.</strong> UHF and IPTVX run back to iOS 16; Lumavu and iPlayTV need 18 or later.</span></li>
  <li><span><strong>Decide where you'll watch.</strong> On Apple TV, the remote and the guide matter most. On iPhone Duo, look for a layout that uses the fold.</span></li>
  <li><span><strong>Try two.</strong> They all read the same playlist, so installing a second one costs nothing.</span></li>
</ol>
"""

PILLAR_FAQ = [
    ("What is the best IPTV app for iPhone?", "For most people it's UHF, IPTVX or Lumavu. UHF has the longest feature list, IPTVX the most polished look, and Lumavu is free with no ads or account and has the best iPhone Duo layout we found. All three play M3U links and Xtream Codes logins."),
    ("What is the best IPTV app for Apple TV?", "UHF is the most actively updated tvOS player and runs back to tvOS 16. Lumavu needs tvOS 18 and adds Jellyfin and Emby films and series next to your playlist. Smarters Player Lite is the simplest."),
    ("Is there a free IPTV player with no ads on iPhone?", "Lumavu is free with no ads and no account, with one playlist on each device. UHF's free tier is also usable, with ads removed in Pro."),
    ("Is TiviMate available on iPhone or Apple TV?", "No. TiviMate is an Android TV app. Apps with similar names on the App Store are from unrelated developers."),
    ("Do IPTV player apps include anything to watch?", "No. Every app here, Lumavu included, is a player for a playlist or server you already have."),
    ("Which IPTV player works best on iPhone Duo?", "Lumavu has dedicated book, tabletop, open and closed layouts, and Multiview splits at the fold. Several other players, including UHF, Fast Player and SWIPTV, also mention iPhone Duo support."),
]

PILLAR_NOTE = f"UHF, IPTVX, Smarters Player Lite, iPlayTV, GSE Smart IPTV, TiviMate, Televizo, Infuse, Swiftfin, Chromareel, Prism, Jellyfin, Emby and Plex are trademarks of their owners. Lumavu is not affiliated with any of them. {PLAYER_ONLY} {TM_APPLE}"


def qa(faq):
    import html as _h
    items = "".join(f'  <details><summary>{_h.escape(q, quote=False)}</summary><div class="a"><p>{_h.escape(ans, quote=False)}</p></div></details>\n'
                    for q, ans in faq)
    return f'<h2 id="faq">Questions</h2>\n<div class="qa">\n{items}</div>\n'


def tail(faq, note):
    return qa(faq) + ALSO + f'<p class="note">{note}</p>\n'

# ---------------------------------------------------------------------------------------------------------------
# iPhone Duo: Lumavu's own page, rewritten with the 1.0.3 release-note detail
# ---------------------------------------------------------------------------------------------------------------

DUO_HTML = f"""
<p class="updated">Updated {CHECKED}. iPhone Duo display sizes are from Apple's {a("https://www.apple.com/iphone-duo/specs/", "technical specifications")}. What Lumavu does on iPhone Duo is from its {a(STORE, "App Store release notes")} (version 1.0.3, 20 November 2026) and our support page.</p>
<div class="summary">
  <p><strong>The short version.</strong> Lumavu is an IPTV player made for iPhone Duo, open, closed and every way in between. Hold it like a book and the sidebar takes the left half, clear of the crease. Stand it half open on a table and the picture sits on top with the controls on the base. Multiview splits at the fold, and whatever you're watching carries on as you open or close it. It's the same free download and the same Pro purchase as on iPhone, iPad and Apple TV.</p>
</div>

<h2 id="postures">Every way you hold it</h2>
<div class="cmp-wrap">
<table class="cmp">
  <thead><tr><th scope="col">How you hold it</th><th scope="col">What Lumavu does</th></tr></thead>
  <tbody>
    <tr><th scope="row">Closed (5.4-inch outer screen)</th><td>The iPhone layout, with tabs along the bottom. Everything stays clear of the clock and the controls down the side, and the artwork runs right up to the top.</td></tr>
    <tr><th scope="row">Open flat (7.6-inch inner screen)</th><td>The full iPad-style layout: the sidebar, the TV guide and every row are sized for the inner screen, with your playlists down the side.</td></tr>
    <tr><th scope="row">Like a book</th><td>The sidebar fills the left half and everything else sits on the right, clear of the crease. The player's buttons move across too, so nothing lands on the fold.</td></tr>
    <tr><th scope="row">Tabletop (half open on a table)</th><td>The picture sits in the top half and the controls sit on the base, like a small TV.</td></tr>
    <tr><th scope="row">Multiview (Lumavu Pro)</th><td>Up to four at once, and the grid splits at the fold rather than across it.</td></tr>
    <tr><th scope="row">Opening or closing it</th><td>You stay where you were: the same page, and the same film keeps playing.</td></tr>
  </tbody>
</table>
</div>
<p>Small things count on a foldable too: names in the TV guide show in full on the inner screen, and the player's programme times stay on one line.</p>

<h2 id="why">Why a foldable suits a TV app</h2>
<p>According to {a("https://www.apple.com/iphone-duo/specs/", "Apple's specifications")}, iPhone Duo has a 7.6-inch inner folding display (1878 by 2670 pixels) and a 5.4-inch outer display (1398 by 2034 pixels), both HDR with ProMotion up to 120Hz. Open, it's close to a small tablet, which is a better size for a film than any phone. Half open, it stands up by itself, so you don't need a stand on a plane tray or a kitchen worktop.</p>
<p>The catch is the crease. An app that simply stretches its iPhone layout puts buttons, subtitles or the middle of the picture on the fold. Lumavu's layouts are drawn around it.</p>

<h2 id="watch">What else works on iPhone Duo</h2>
<ul>
  <li><strong>Offline downloads (Pro).</strong> Save a film or a whole season before a flight. Your place carries over to the streamed copy when you're back online. Downloads wait for Wi-Fi unless you allow mobile data.</li>
  <li><strong>Live subtitles.</strong> Written on the device from what's being said, and translated as they go on iOS 26 or later.</li>
  <li><strong>Picture in Picture and AirPlay.</strong> For streams that play in Apple's player. Lumavu also has its own Apple TV app.</li>
  <li><strong>4K, HD and SD as one entry.</strong> The guide stays short, which matters on the outer screen.</li>
  <li><strong>No account and no ads.</strong> The App Store privacy label says no data is collected.</li>
</ul>

<h2 id="add">What you add</h2>
<p>An M3U or M3U8 link, an Xtream Codes login, or a Jellyfin or Emby server. If an M3U link is really an Xtream account, Lumavu signs in as Xtream by itself. From Jellyfin and Emby you get films and series today. {PLAYER_ONLY}</p>
{CTA}

<h2 id="others">Other players on iPhone Duo</h2>
<p>Lumavu isn't the only player that has thought about the fold. On their own sites or listings, Fast Player, Smart IPTV Pro, SWIPTV and RunTV describe iPhone Duo layouts, UHF's release notes mention iPhone Duo support, and Infuse and Chromareel do the same for media servers. We list them, with what each says it does, in {L(DUO_APPS, "video and IPTV player apps made for iPhone Duo")}.</p>

<h2 id="price">What it costs</h2>
<p>Lumavu is free with one playlist on each device, one favourites list, and the guide from yesterday to tomorrow. Lumavu Pro adds sync across your devices, the whole week's guide, Multiview, recordings, downloads, and as many playlists as you like. In the UK, Pro is £2.99 a month, £19.99 a year (with seven days free for new subscribers) or £49.99 once. One purchase covers iPhone, iPhone Duo, iPad and Apple TV on the same Apple Account.</p>
<p>{TRY}.</p>
"""

DUO_FAQ = [
    ("Does Lumavu work on iPhone Duo?", "Yes. Version 1.0.3 is made for iPhone Duo, with layouts for closed, open, book and tabletop. It's the same app and the same purchase as on iPhone."),
    ("What happens if I fold iPhone Duo while something is playing?", "It keeps playing. Lumavu keeps you on the same page and the same film as the layout changes."),
    ("Does Lumavu have a tabletop mode on iPhone Duo?", "Yes. Stand it half open and the picture sits in the top half, with the controls on the base."),
    ("Can I watch four streams at once on iPhone Duo?", "With Lumavu Pro, Multiview plays up to four at once and splits at the fold. Each tile is its own stream, so your account needs to allow that many connections."),
    ("Can I download films to watch offline on iPhone Duo?", "Yes, with Lumavu Pro, for films and episodes that come as files. Live streams and HLS-only links can't be downloaded."),
    ("Does Lumavu include anything to watch?", "No. It's a player for the playlist or server you already have."),
]
DUO_NOTE = f"Display sizes are from Apple's iPhone Duo specifications. Other apps named here are trademarks of their owners. {PLAYER_ONLY} {TM_APPLE}"

# ---------------------------------------------------------------------------------------------------------------
# iPhone Duo video / IPTV / media player apps (the "best iPhone Duo apps" cluster, for watching)
# ---------------------------------------------------------------------------------------------------------------

DUO_APPS_HTML = f"""
<p class="updated">Checked {CHECKED}. Each entry says only what that app's own listing, release notes or website says about iPhone Duo. Disclosure: we make Lumavu.</p>
<div class="summary">
  <p><strong>The short version.</strong> iPhone Duo's 7.6-inch inner screen is the biggest iPhone screen yet for watching, and the hinge lets it stand by itself. But an app has to be built for it, or the crease runs through the middle of your buttons. These are the video, IPTV and media-server players that say they're made for iPhone Duo, and what each one does with the fold.</p>
</div>

<h2 id="look">What to look for</h2>
<ul>
  <li><strong>Tabletop (half-open) layout.</strong> The picture on the top half, controls on the bottom. This is the posture that turns a foldable into a little TV.</li>
  <li><strong>A book layout that respects the crease.</strong> Lists on one side, player or details on the other, with nothing sitting on the fold.</li>
  <li><strong>Continuity.</strong> Opening or closing it shouldn't stop or reload what's playing.</li>
  <li><strong>A real outer-screen layout.</strong> Not a stretched or letterboxed iPhone app.</li>
</ul>

<h2 id="iptv">IPTV players made for iPhone Duo</h2>
<div class="cmp-wrap">
<table class="cmp wide">
  <thead><tr><th scope="col">App</th><th scope="col">Tabletop</th><th scope="col">Book / side by side</th><th scope="col">Keeps playing as you fold</th><th scope="col">Other Duo touches</th><th scope="col">Source</th></tr></thead>
  <tbody>
    <tr><th scope="row">Lumavu</th><td>Yes: picture on top, controls on the base</td><td>Yes: sidebar in the left half, clear of the crease; player buttons move across</td><td>Yes: same page, same film</td><td>Multiview splits at the fold; outer screen kept clear of the clock and side controls; also Jellyfin and Emby</td><td>{a(STORE, "Release notes, v1.0.3")}</td></tr>
    <tr><th scope="row">Smart IPTV Pro Player</th><td>Yes: video above the fold, controls below</td><td>Yes: list left, player right, split on the fold</td><td>Not stated</td><td>Layouts switch automatically</td><td>{a("https://iphoneiptv.app/", "Developer site")}</td></tr>
    <tr><th scope="row">RunTV</th><td>Yes: one big picture above the fold, up to three small ones below</td><td>Yes: dashboard split into two halves at the fold</td><td>Streams keep playing on the cover screen</td><td>Folded, it works as a remote for a TV; up to four streams open</td><td>{a("https://runtv.run/iptv-player-iphone-duo", "Developer site")}</td></tr>
    <tr><th scope="row">Fast Player</th><td>Not stated</td><td>Big-screen layout with the player beside the list and guide</td><td>Yes, without reloading the stream</td><td>From version 3.0</td><td>{a("https://fastplayer.co/iphone-duo/", "Developer site")}</td></tr>
    <tr><th scope="row">{a(AS["swiptv"], "SWIPTV")}</th><td>Not stated</td><td>Unfolded, the iPad layout with categories on the left</td><td>Not stated</td><td>Rotates in every direction</td><td>App Store listing</td></tr>
    <tr><th scope="row">{a(AS["uhf"], "UHF")}</th><td>Not stated</td><td>Not stated</td><td>Not stated</td><td>"Various changes to better support" iPhone Duo (2.5.0, 31 Oct 2026)</td><td>Release notes</td></tr>
  </tbody>
</table>
</div>
<p>"Not stated" means the app's own description doesn't say, not that it can't. If a posture matters to you, try it before paying.</p>

<h2 id="servers">Media-server and video players for iPhone Duo</h2>
<ul>
  <li><strong>{a(AS["chromareel"], "Chromareel")}</strong> (Jellyfin, free, launched 26 November 2026). Its listing says: open it flat and turn it sideways to browse on one side and watch on the other; stand it half open like a laptop for the picture on top and every control on the flat half; fold it into a tent and the cover screen keeps playing. It needs iOS 26.</li>
  <li><strong>{a(AS["infuse"], "Infuse")}</strong> (Jellyfin, Emby, Plex, network shares). Its 23 November release notes list "improved support for iPhone Duo".</li>
  <li><strong>Lumavu</strong> also plays films and series from Jellyfin and Emby, next to M3U and Xtream playlists, with the layouts above.</li>
</ul>
<p>For a wider look at Jellyfin on Apple devices, see {L(JELLY, "Jellyfin players for Apple TV")}.</p>

<h2 id="streaming">Streaming apps</h2>
<p>Among the big streaming apps, Apple's {a("https://www.apple.com/newsroom/2026/10/developers-bring-incredible-new-app-experiences-to-iphone-duo/", "iPhone Duo developer announcement")} highlighted Netflix, which lets you scroll Clips on the outer display and open the phone to keep watching on the inner one.</p>

<h2 id="directories">Finding more Duo apps</h2>
<p>Several independent sites track apps made for iPhone Duo, including duoworthy.com, getduoready.com, duotoday.com and duodiscover.com. Release notes are the most reliable signal: look for "iPhone Duo", "tabletop" or "fold" in What's New.</p>
"""

DUO_APPS_FAQ = [
    ("What's the best video player for iPhone Duo?", "It depends on what you watch. For an M3U playlist or Xtream login, Lumavu, Smart IPTV Pro and RunTV describe tabletop layouts. For a Jellyfin library, Chromareel and Infuse mention iPhone Duo support, and Lumavu plays Jellyfin and Emby films and series too."),
    ("Is there an IPTV app for iPhone Duo?", "Yes, several. Lumavu has closed, open, book and tabletop layouts and splits Multiview at the fold. Fast Player, Smart IPTV Pro, SWIPTV and RunTV also describe iPhone Duo layouts."),
    ("What is tabletop mode on iPhone Duo?", "Standing the phone half open on a surface. Apps made for it put the picture in the top half and the controls on the bottom half."),
    ("Do iPhone apps work on iPhone Duo without an update?", "They open, but an app that hasn't been updated may not use the inner screen well or may put controls on the crease. Look for iPhone Duo in the app's release notes."),
]
DUO_APPS_NOTE = f"Chromareel, Infuse, Fast Player, Smart IPTV Pro Player, RunTV, SWIPTV, UHF, Netflix, Jellyfin, Emby and Plex are trademarks of their owners. Lumavu is not affiliated with any of them. {PLAYER_ONLY} {TM_APPLE}"

# ---------------------------------------------------------------------------------------------------------------
# M3U player for iPhone and iPad
# ---------------------------------------------------------------------------------------------------------------

M3U_HTML = f"""
<p class="updated">Updated {CHECKED}. Steps are for Lumavu; the same ideas apply to any player.</p>
<div class="summary">
  <p><strong>The short version.</strong> An M3U (or M3U8) playlist is a text file, usually a link, that lists streams. iPhone and iPad can't open one by themselves: you need a player app. In Lumavu, choose Add playlist, then M3U, and paste the link or pick the file. If the link is really an Xtream Codes account, Lumavu notices and signs in as Xtream, so you also get the films, series and catch-up behind it.</p>
</div>

<h2 id="what">What an M3U playlist is</h2>
<p>M3U is a plain-text list of addresses, one per stream, usually with a name, a group and a logo for each. M3U8 is the same format saved as UTF-8 text, and the extension is also used for HLS streams, which Apple's own player handles well. A playlist link often ends in <code>.m3u</code> or <code>.m3u8</code>, or has <code>type=m3u</code> in it.</p>
<p>A TV guide usually comes separately, as an XMLTV link (often ending <code>.xml</code> or <code>.xml.gz</code>).</p>

<h2 id="steps">How to open an M3U link on iPhone or iPad</h2>
<ol class="steps">
  <li><span><strong>Get a player.</strong> {TRY}. It's free for iPhone, iPhone Duo, iPad and Apple TV, with no account.</span></li>
  <li><span><strong>Add playlist, then M3U.</strong> Paste the link, or choose a file from the Files app.</span></li>
  <li><span><strong>Name it.</strong> Give it a name, a colour and an icon, so it's easy to spot in the sidebar.</span></li>
  <li><span><strong>Add the guide.</strong> If you have an XMLTV link, add it in the playlist's settings. Xtream accounts usually bring their own guide.</span></li>
</ol>
<p>Use a link rather than a file if you can: a link refreshes itself and, with Lumavu Pro, syncs to your other devices through iCloud. A file stays on the device you imported it on.</p>

<h2 id="xtream">When an M3U link is really Xtream Codes</h2>
<p>Many M3U links are generated by an Xtream Codes server and carry a username and password in the address. An M3U link only gives a player the list of streams. Signing in as Xtream also brings the films and series sections, catch-up and the guide. Lumavu spots this and signs in as Xtream for you; in most other players you'd type the server, username and password separately. More in {L(XTREAM, "Xtream Codes on Apple TV")}.</p>

<h2 id="tidy">Keeping a big playlist tidy</h2>
<ul>
  <li><strong>Duplicates merged.</strong> When the same stream appears in 4K, HD and SD, Lumavu shows one entry. If one copy fails, it tries the next by itself.</li>
  <li><strong>Hide what you never watch.</strong> Hide a whole language or family of categories in one tap, or lock categories behind a PIN.</li>
  <li><strong>Formats.</strong> HLS plays in Apple's player, with Picture in Picture and AirPlay. MKV, AVI and MPEG-TS play too.</li>
</ul>

<h2 id="players">Other M3U players for iPhone</h2>
<p>UHF, IPTVX, Smarters Player Lite, iPlayTV and GSE Smart IPTV Pro all open M3U playlists. VLC opens an M3U file as a flat list, without a guide. We compare them in {L(PILLAR, "the best IPTV players for iPhone, iPad and Apple TV")}.</p>
{CTA}
"""

M3U_FAQ = [
    ("How do I open an M3U file on iPhone?", "Install a player such as Lumavu, choose Add playlist, then M3U, and paste the link or pick the file from the Files app. iPhone can't play an M3U playlist without a player app."),
    ("What's the difference between M3U and M3U8?", "Both are playlists. M3U8 is saved as UTF-8 text, and the same extension is used for HLS streams. Players treat them the same way."),
    ("Does Lumavu work with M3U on iPad and iPhone Duo?", "Yes. The same app runs on iPhone, iPhone Duo, iPad and Apple TV."),
    ("Why doesn't my M3U playlist show a TV guide?", "M3U playlists don't carry a guide. Add the XMLTV link in the playlist's settings. Xtream logins usually include the guide."),
    ("Does Lumavu include a playlist?", "No. Lumavu is a player for the playlist you already have."),
]
M3U_NOTE = f"{PLAYER_ONLY} {TM_APPLE}"

# ---------------------------------------------------------------------------------------------------------------
# Xtream Codes player for Apple TV
# ---------------------------------------------------------------------------------------------------------------

XTREAM_HTML = f"""
<p class="updated">Updated {CHECKED}. Steps are for Lumavu on Apple TV; the same login works on iPhone, iPhone Duo and iPad.</p>
<div class="summary">
  <p><strong>The short version.</strong> An Xtream Codes login is three things: a server address, a username and a password. On Apple TV, install a player that supports Xtream, such as Lumavu, choose Add playlist, then Xtream Codes, and type them in. With Lumavu Pro, add it once on your iPhone and it appears on your Apple TV through iCloud.</p>
</div>

<h2 id="what">What an Xtream Codes login is</h2>
<p>Xtream Codes is a common server system behind many playlists. Instead of a single link, you sign in, and the player gets live streams, films, series, the TV guide and catch-up as separate sections. The server address usually looks like <code>http://example.com:8080</code>.</p>
<p>If you only have an M3U link with <code>username=</code> and <code>password=</code> in it, that's an Xtream account too. Lumavu recognises it and signs in for you.</p>

<h2 id="steps">How to add Xtream Codes on Apple TV</h2>
<ol class="steps">
  <li><span><strong>Install Lumavu on Apple TV.</strong> It's free on the App Store and needs tvOS 18 or later. {TRY}.</span></li>
  <li><span><strong>Add playlist, then Xtream Codes.</strong> Enter the server address, username and password. When Apple TV shows its keyboard, a nearby iPhone can offer to type for you.</span></li>
  <li><span><strong>Give it a name and colour.</strong> It shows in the sidebar.</span></li>
  <li><span><strong>Or skip typing.</strong> With Lumavu Pro, add the login on your iPhone, iPhone Duo or iPad and iCloud sync brings it to Apple TV, with your favourites and where you left off. Passwords are kept in the Keychain.</span></li>
</ol>

<h2 id="tv">What you get on Apple TV</h2>
<ul>
  <li><strong>A TV guide</strong> from the account, and catch-up where the account offers it.</li>
  <li><strong>Films and series that remember</strong> where you stopped.</li>
  <li><strong>One entry for 4K, HD and SD copies,</strong> with automatic fallback if one fails.</li>
  <li><strong>Live subtitles</strong> written on the device (Apple TV writes them but doesn't translate them).</li>
  <li><strong>Multiview (Pro).</strong> Up to four at once, if your account allows that many connections.</li>
</ul>
<p>What Lumavu doesn't do on Apple TV yet: Jellyfin or Emby live TV, and recording, which runs on iPhone, iPad and Mac while the app is open.</p>
{CTA}

<h2 id="others">Other Xtream players for Apple TV</h2>
<p>UHF, IPTVX, Smarters Player Lite and iPlayTV also sign in with Xtream on Apple TV. UHF runs back to tvOS 16, so it's the one to try if your Apple TV can't update to tvOS 18. See {L(PILLAR, "our comparison")}.</p>
"""

XTREAM_FAQ = [
    ("Can Apple TV play Xtream Codes?", "Not by itself. Install a player that supports Xtream Codes, such as Lumavu, UHF or IPTVX, and sign in with the server address, username and password."),
    ("Which Apple TV models can run Lumavu?", "Any Apple TV that runs tvOS 18 or later."),
    ("Do I need to type the login with the Apple TV remote?", "No. You can use a nearby iPhone's keyboard, or, with Lumavu Pro, add the login on iPhone and let iCloud sync bring it to Apple TV."),
    ("Is Xtream Codes the same as M3U?", "They often come from the same account. M3U is a single list; signing in as Xtream also brings films, series, the guide and catch-up as separate sections."),
    ("Does Lumavu include an Xtream account?", "No. Lumavu is a player for a login you already have."),
]
XTREAM_NOTE = f"Xtream Codes is a name used by third-party server software; Lumavu is not affiliated with it. {PLAYER_ONLY} {TM_APPLE}"

# ---------------------------------------------------------------------------------------------------------------
# Jellyfin on Apple TV, rewritten with Prism and Chromareel, and more depth of its own
# ---------------------------------------------------------------------------------------------------------------

JELLY_HTML = f"""
<p class="updated">Checked {CHECKED}. Facts are from each app's App Store listing ({a(AS["swiftfin"], "Swiftfin")}, {a(AS["infuse"], "Infuse")}, {a(AS["chromareel"], "Chromareel")}, {a(STORE, "Lumavu")}), {a("https://firecore.com/infuse", "firecore.com")} and {a("https://prismhub.app", "prismhub.app")}. Disclosure: we make Lumavu.</p>
<div class="summary">
  <p><strong>The short version.</strong> If you only use Jellyfin and your Apple TV runs tvOS 26.1, start with <strong>Swiftfin</strong>, the free official client with live TV from your server. Choose <strong>Infuse</strong> for the widest file support or if you also use Plex or a NAS. <strong>Chromareel</strong> is a new free Jellyfin app with a streaming-service look, but it needs iOS 26. Choose <strong>Lumavu</strong> if you want your Jellyfin or Emby films and series and an IPTV playlist in one app, on tvOS 18 or later, or the most complete iPhone Duo layout. Prism, a popular hub app, stopped working around 16 November 2026.</p>
</div>

<h2 id="prism">If you used Prism</h2>
<p>Prism's own site says it has reached the end of its life: installed copies kept opening until about 16 November 2026, it can't be installed on new devices, and it won't be updated. Your films and series stay on your Jellyfin or Emby server, and watched status saved on the server comes with you to any app that signs in to the same account. Expect to rebuild app-specific things such as layouts and collections.</p>
<p>When you pick a replacement, check three things: which servers it supports (Jellyfin only, or Emby and Plex too), whether your oldest Apple TV can run it, and whether it plays your trickiest files.</p>

<h2 id="compare">At a glance</h2>
<div class="cmp-wrap">
<table class="cmp">
  <thead>
    <tr><th scope="col"></th><th scope="col">Swiftfin</th><th scope="col">Infuse</th><th scope="col">Chromareel</th><th scope="col">Lumavu</th></tr>
  </thead>
  <tbody>
    <tr><th scope="row">Role</th><td>Official Jellyfin client</td><td>General Apple media player</td><td>Jellyfin client</td><td>IPTV player that also connects to Jellyfin and Emby</td></tr>
    <tr><th scope="row">Servers</th><td>Jellyfin</td><td>Jellyfin, Emby, Plex, network folders, cloud drives</td><td>Jellyfin</td><td>Jellyfin and Emby, plus M3U and Xtream playlists</td></tr>
    <tr><th scope="row">Jellyfin live TV</th><td>Yes, if your server has it</td><td>Not stated on the homepage we used</td><td>Not stated</td><td>Not yet; films and series today</td></tr>
    <tr><th scope="row">Needs</th><td>tvOS 26.1 · iOS 18.6</td><td>tvOS 18.5 · iOS 18</td><td>iOS 26</td><td>tvOS 18 · iOS 18</td></tr>
    <tr><th scope="row">iPhone Duo</th><td>Not stated</td><td>"Improved support for iPhone Duo" (23 Nov release notes)</td><td>Side-by-side, laptop and tent layouts</td><td>Book, tabletop, open and closed layouts</td></tr>
    <tr><th scope="row">Offline downloads</th><td>Not stated</td><td>Not stated on the homepage we used</td><td>One-time unlock on iPhone</td><td>Lumavu Pro, on iPhone and iPad; your place carries over</td></tr>
    <tr><th scope="row">Price</th><td>Free</td><td>Free; Pro $1.99/month, $16.99/year or $99.99 once (firecore.com)</td><td>Free; downloads a one-time unlock</td><td>Free; Pro £2.99/month, £19.99/year or £49.99 once (UK)</td></tr>
    <tr><th scope="row">Ads and tracking</th><td>Privacy label: data not collected</td><td>Firecore says no ads and no tracking</td><td>Listing: no account, no tracking</td><td>No ads, no account. Privacy label: data not collected</td></tr>
  </tbody>
</table>
</div>
{CTA}

<h2 id="swiftfin">Swiftfin</h2>
<p>Swiftfin is the official Jellyfin app for iPhone, iPad and Apple TV, and it's free and open source. Its listing describes a native player for a Jellyfin server you run, with live TV and recordings from that server. The current Apple TV version needs tvOS 26.1 or later. If you only use Jellyfin and your Apple TV is up to date, it's the natural place to start.</p>

<h2 id="infuse">Infuse</h2>
<p>Infuse, by Firecore, connects to Jellyfin, Emby and Plex, as well as folders on a Mac, PC or NAS and several cloud drives. Playback is its strength, with a long list of file formats; Infuse Pro adds Dolby Vision, Dolby Atmos passthrough, AirPlay, iCloud library sync and cloud streaming. Its 23 November 2026 update added native live previews from Plex, Emby and Jellyfin, and improved iPhone Duo support.</p>

<h2 id="chromareel">Chromareel</h2>
<p>Chromareel launched on 26 November 2026 as a free Jellyfin app for iPhone and Apple TV. Its listing describes a home screen built around Continue Watching and Next Up, recommendations from what you watch, Skip Intro and Skip Credits from your server's markers, downloads as a one-time unlock on iPhone, and layouts made for iPhone Duo. It needs iOS 26, and it's brand new, so it has no ratings yet.</p>

<h2 id="lumavu">Lumavu</h2>
<p>Lumavu is an IPTV player for iPhone, iPhone Duo, iPad and Apple TV that also signs in to Jellyfin and Emby. You get your films and series, with posters, seasons and resume, next to any M3U or Xtream playlist, in one app. Movies and episodes from Jellyfin 10.11 and later play, and Jellyfin and Emby sign-ins are only ever sent to your own server. Live TV from Jellyfin or Emby isn't available yet.</p>
<p>It runs on tvOS 18, so it works on Apple TVs that can't install the current Swiftfin. With Lumavu Pro, downloads on iPhone and iPad carry your place back to the streamed copy, and iCloud sync keeps servers and progress the same on every device.</p>

<h2 id="setup">Adding a Jellyfin or Emby server to Lumavu</h2>
<ol class="steps">
  <li><span><strong>Install Lumavu</strong> on Apple TV, iPhone, iPhone Duo or iPad. {TRY}.</span></li>
  <li><span><strong>Add playlist, then Jellyfin or Emby.</strong> Enter your server's address, your username and password.</span></li>
  <li><span><strong>Name it</strong> and pick a colour and icon for the sidebar.</span></li>
</ol>

<h2 id="choose">Which should you pick?</h2>
<ul>
  <li><strong>Official app, Jellyfin live TV, up-to-date Apple TV:</strong> Swiftfin.</li>
  <li><strong>Demanding files, or Plex and a NAS too:</strong> Infuse.</li>
  <li><strong>A streaming-service feel on iOS 26, Jellyfin only:</strong> Chromareel.</li>
  <li><strong>Jellyfin or Emby and an IPTV playlist in one app, tvOS 18, or iPhone Duo:</strong> Lumavu.</li>
</ul>
<p>You can install more than one; they can all point at the same server.</p>
"""

JELLY_FAQ = [
    ("What is the best Jellyfin app for Apple TV?", "Swiftfin is the official, free client and includes Jellyfin live TV, but needs tvOS 26.1. Infuse has the widest file support. Lumavu runs on tvOS 18 and puts Jellyfin or Emby films and series next to IPTV playlists."),
    ("What can I use instead of Prism on Apple TV?", "Swiftfin for Jellyfin only, Infuse for Jellyfin, Emby and Plex, or Lumavu for Jellyfin or Emby alongside an IPTV playlist. Your libraries and server-side watched status stay on your server."),
    ("Does Lumavu play Jellyfin live TV?", "Not yet. Films and series from Jellyfin and Emby work today. For Jellyfin live TV, use Swiftfin."),
    ("Does Lumavu work with Emby?", "Yes, for films and series, on iPhone, iPhone Duo, iPad and Apple TV."),
    ("Does Lumavu include any films or series?", "No. Lumavu is a player for the server or playlist you already have."),
]
JELLY_NOTE = f"Jellyfin is a trademark of the Jellyfin project; Swiftfin is its official companion app. Infuse is a product of Firecore. Chromareel, Prism, Emby and Plex are trademarks of their owners. Lumavu is not affiliated with any of them. {PLAYER_ONLY} {TM_APPLE}"

# ---------------------------------------------------------------------------------------------------------------

TIVIMATE_FAQ = [
    ("Is there an official TiviMate app for Apple TV or iPhone?", "No. TiviMate's website says the app is intended for Android TV and is installed from Google Play or as an APK. There is no official TiviMate app on the App Store."),
    ("Will my existing playlist work in Lumavu?", "If you have an M3U playlist or an Xtream Codes login, add it in Lumavu the same way you would in any other player. Lumavu doesn't include anything to watch, and it doesn't receive your playlist: the details stay on your device."),
    ("Does Lumavu work on Android TV?", "No. Lumavu is an Apple app, for iPhone, iPhone Duo, iPad and Apple TV. If you already use TiviMate on Android TV, you can keep it there and use Lumavu on your Apple devices."),
    ("Does Lumavu include anything to watch?", "No. It is a player for the playlist or server you already have."),
]

SMARTERS_FAQ = [
    ("Is Lumavu the same as IPTV Smarters?", "No. Lumavu is a separate app from Thinkers & Builders. It is not affiliated with IPTV Smarters or WHMCS SMARTERS."),
    ("Will the playlist I used in Smarters work in Lumavu?", "If you have the M3U link or the Xtream Codes login, add it in Lumavu. Lumavu doesn't include anything to watch, and it doesn't need an export from another player."),
    ("Does Lumavu have ads?", "No. There are no ads, no account and no tracking."),
    ("Does Lumavu include anything to watch?", "No. It is a player for the playlist or server you already have."),
]

# (filename, short name for footers and the 404 page)
COMPARE_LINKS = [
    (PILLAR, "Best IPTV players"),
    (DUO, "iPhone Duo"),
    (DUO_APPS, "iPhone Duo video apps"),
    (M3U, "M3U on iPhone"),
    (XTREAM, "Xtream on Apple TV"),
    (JELLY, "Jellyfin on Apple TV"),
    ("lumavu-vs-tivimate.html", "vs TiviMate"),
    ("iptv-smarters-alternative.html", "Smarters alternative"),
]

GUIDE_DATES = {f: SITE_UPDATED for f, _ in COMPARE_LINKS}


def page(fname, title, crumb, h1, toc, html, faq, note, description, og_title, og_description, published=None):
    return (fname, title, "Guide", h1, toc + [("faq", "Questions")], html + tail(faq, note), {
        "show_eyebrow": False, "description": description, "og_title": og_title, "og_description": og_description,
        "faq": faq, "crumb": crumb, "app_ld": True, "modified": SITE_UPDATED, "published": published or SITE_UPDATED})


COMPARE_PAGES = [
    page(PILLAR,
         "Best IPTV Player Apps for iPhone, iPad & Apple TV (2026) | Lumavu",
         "Best IPTV players for iPhone, iPad and Apple TV",
         "Best IPTV player apps for iPhone, iPad and Apple TV (2026)",
         [("pick", "Quick picks"), ("compare", "Compared"), ("lumavu", "Lumavu"), ("uhf", "UHF"), ("iptvx", "IPTVX"),
          ("smarters", "Smarters"), ("iplaytv", "iPlayTV"), ("gse", "GSE"), ("android", "TiviMate"), ("choose", "How to choose")],
         PILLAR_HTML, PILLAR_FAQ, PILLAR_NOTE,
         "The best IPTV players for iPhone, iPhone Duo, iPad and Apple TV in 2026: UHF, IPTVX, Smarters Player Lite, iPlayTV, GSE and Lumavu compared on price, ads, sources and iPhone Duo support.",
         "Best IPTV player apps for iPhone, iPad and Apple TV (2026)",
         "UHF, IPTVX, Smarters Player Lite, iPlayTV, GSE and Lumavu compared on price, ads, sources and iPhone Duo support. Checked 27 Nov 2026."),
    page(DUO,
         "Best IPTV Player for iPhone Duo: Book & Tabletop Layouts | Lumavu",
         "IPTV player for iPhone Duo",
         "The IPTV player made for iPhone Duo",
         [("postures", "Every posture"), ("why", "Why a foldable"), ("watch", "What else works"), ("add", "What you add"),
          ("others", "Other players"), ("price", "Price")],
         DUO_HTML, DUO_FAQ, DUO_NOTE,
         "Lumavu is an IPTV player made for iPhone Duo: a book layout clear of the crease, tabletop with the picture on top, Multiview split at the fold, and playback that carries on as you fold. Free, no ads.",
         "The IPTV player made for iPhone Duo",
         "Book layout clear of the crease, tabletop mode, Multiview split at the fold, and playback that carries on as you open or close it.",
         published="2026-11-18"),
    page(DUO_APPS,
         "iPhone Duo Video Player & IPTV Apps Made for the Fold (2026) | Lumavu",
         "iPhone Duo video and IPTV apps",
         "Video and IPTV player apps made for iPhone Duo",
         [("look", "What to look for"), ("iptv", "IPTV players"), ("servers", "Media players"), ("streaming", "Streaming apps"),
          ("directories", "Finding more")],
         DUO_APPS_HTML, DUO_APPS_FAQ, DUO_APPS_NOTE,
         "Which video, IPTV and media players are made for iPhone Duo? Tabletop, book and fold support compared for Lumavu, Smart IPTV Pro, RunTV, Fast Player, SWIPTV, UHF, Chromareel and Infuse.",
         "Video and IPTV player apps made for iPhone Duo",
         "Tabletop, book and fold support compared, from each app's own listing. Checked 27 Nov 2026."),
    page(M3U,
         "M3U Player for iPhone & iPad: How to Open an M3U Link | Lumavu",
         "M3U player for iPhone and iPad",
         "M3U player for iPhone and iPad",
         [("what", "What M3U is"), ("steps", "How to open one"), ("xtream", "M3U or Xtream?"), ("tidy", "Big playlists"),
          ("players", "Other players")],
         M3U_HTML, M3U_FAQ, M3U_NOTE,
         "How to open an M3U or M3U8 playlist on iPhone, iPhone Duo and iPad: paste the link into a player such as Lumavu, add an XMLTV guide, and let it detect an Xtream account behind the link. Free, no ads.",
         "M3U player for iPhone and iPad",
         "How to open an M3U or M3U8 link on iPhone, iPhone Duo and iPad, add a TV guide, and spot an Xtream account behind the link."),
    page(XTREAM,
         "Xtream Codes Player for Apple TV: How to Sign In | Lumavu",
         "Xtream Codes player for Apple TV",
         "Xtream Codes player for Apple TV",
         [("what", "What Xtream is"), ("steps", "How to add it"), ("tv", "On Apple TV"), ("others", "Other players")],
         XTREAM_HTML, XTREAM_FAQ, XTREAM_NOTE,
         "How to use an Xtream Codes login on Apple TV: install a player such as Lumavu, enter the server, username and password, or add it on iPhone and sync. Works on iPhone, iPhone Duo and iPad too.",
         "Xtream Codes player for Apple TV",
         "Sign in with a server address, username and password on Apple TV, or add it on iPhone and let iCloud bring it across."),
    page(JELLY,
         "Best Jellyfin Player for Apple TV (2026): Swiftfin, Infuse & More | Lumavu",
         "Jellyfin players for Apple TV",
         "Jellyfin players for Apple TV, after Prism",
         [("prism", "After Prism"), ("compare", "At a glance"), ("swiftfin", "Swiftfin"), ("infuse", "Infuse"), ("chromareel", "Chromareel"),
          ("lumavu", "Lumavu"), ("setup", "Setting up"), ("choose", "Which to pick")],
         JELLY_HTML, JELLY_FAQ, JELLY_NOTE,
         "Swiftfin, Infuse, Chromareel and Lumavu compared for Jellyfin on Apple TV, iPhone and iPhone Duo, with what to use now that Prism has shut down. Checked 27 Nov 2026.",
         "Jellyfin players for Apple TV, after Prism",
         "Swiftfin, Infuse, Chromareel and Lumavu compared, and what to use now Prism has shut down.",
         published="2026-11-16"),
    ("lumavu-vs-tivimate.html", "Lumavu vs TiviMate: an IPTV Player for iPhone, iPhone Duo and Apple TV", "Compare", "Lumavu vs TiviMate",
     [("apple", "On Apple devices?"), ("purpose", "What they're for"), ("compare", "How they compare"), ("fit", "When Lumavu fits"),
      ("price", "Price"), ("faq", "Questions")],
     TIVIMATE,
     {"show_eyebrow": True, "crumb": "Lumavu vs TiviMate", "app_ld": True, "modified": SITE_UPDATED, "published": "2026-11-16",
      "description": "TiviMate is an IPTV player for Android TV, not iPhone, iPhone Duo or Apple TV. Lumavu is a player for the same M3U or Xtream playlist on those Apple devices. Free, no ads, no account.",
      "og_title": "Lumavu vs TiviMate",
      "og_description": "TiviMate is for Android TV. Lumavu is a player for iPhone, iPhone Duo, iPad and Apple TV. Bring your own playlist.",
      "faq": TIVIMATE_FAQ}),
    ("iptv-smarters-alternative.html", "IPTV Smarters Alternative for iPhone, iPhone Duo and Apple TV | Lumavu", "Compare", "An IPTV Smarters alternative for iPhone and Apple TV",
     [("smarters", "Smarters Player Lite"), ("why", "Why switch"), ("compare", "How they compare"), ("move", "Moving your playlist"),
      ("price", "Price"), ("faq", "Questions")],
     SMARTERS,
     {"show_eyebrow": True, "crumb": "IPTV Smarters alternative", "app_ld": True, "modified": SITE_UPDATED, "published": "2026-11-16",
      "description": "Looking for an IPTV Smarters alternative on iPhone, iPhone Duo or Apple TV? Lumavu is a player for the M3U playlist or Xtream login you already have. No ads, no account, no tracking.",
      "og_title": "An IPTV Smarters alternative for iPhone and Apple TV",
      "og_description": "Lumavu is a player for the playlist you already have: no ads, no account, no tracking.",
      "faq": SMARTERS_FAQ}),
]
