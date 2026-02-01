# TG BOT THAT DOWNLOADS MANGA FROM SHADY MANGA SITES

@https://t.me/manga_bato_downloader_bot

# ABOUT
Telegram bot that scrapes images from manga sites and packs them into PDFs so my gf can read them offline in a nice format, probably the most popular side project I've ever worked on lol.

# TECH CHALLENGES
As the git history shows, the sites she reads manga on keep changing, so I had to keep up with the demand and put in a lot more effort than initially envisioned. I tried to keep it working with HTTP only so it would stay simpler and smaller, but each site uses a different weird frontend situation that takes ages to figure out, so I had to switch to Selenium, which worked out pretty well to be fair. I had to invest in proper architecture since I, no doubt, will need to add another scraper next week.
