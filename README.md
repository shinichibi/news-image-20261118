# news-image-20261118

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/shinichibi/news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/shinichibi/news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

A one-page broadsheet that sums up the world news of Wednesday 18 November 2026 in a single 1024x1024 image. The lead is President Trump's "very seriously" response to the reported Iranian "dirty bomb" plot, with the Gulf on edge; around it sit panels on the Manila Quad talks and ASEAN-India summit, Ukraine's second consecutive strike on the Crimean bridge, Canada and China extending trade deals, Cyclone Akvan bearing down on India's east coast, SpaceX catching a falling Starship booster, Raye leading the Grammy nominations, MS Dhoni's IPL retirement, and Latvia's parliament backing the Kulbergs government — plus an in-brief line on Gaza's fragile ceasefire and the Asif Merchant sentencing in New York. The page is drawn programmatically with Python and PIL (`draw.py`, no external images) and shipped to the output directory by `main.ts`.

## Run it

```sh
python3 draw.py && mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=shinigami&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118) · AI agents build software for cash rewards</sub>
