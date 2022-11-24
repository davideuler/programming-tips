
# Open Source Projects


open source tools:
* https://github.com/PostHog/posthog
* https://github.com/sixpack/sixpack
* https://github.com/growthbook/growthbook/ (TS)
* https://github.com/Unleash/unleash (TS)
* https://github.com/fluxcd/flagger (Go)
* https://github.com/splitrb/split (Ruby)


https://github.com/Flagsmith/flagsmith

https://github.com/rudderlabs/rudder-server

https://github.com/FetLife/rollout

https://github.com/intuit/wasabi/ (java)

https://github.com/privacy-com/wasabi

https://github.com/assaf/vanity (ruby)

https://github.com/wix-incubator/petri (java)

https://github.com/mixcloud/django-experiments

https://pypi.org/project/django-lean/

https://github.com/pushtell/react-ab-test

https://github.com/danmaz74/ABalytics

https://vwo.com/blog/ab-testing-tools/

https://posthog.com/blog/best-open-source-ab-testing-tools

data visualization & reporting
https://github.com/metabase/metabase


# Open Source A/B Testing

https://medium.com/growth-book/open-source-a-b-testing-dbc68aedab70

A/B testing is such a core part of product development, it’s hard to justify relying on 3rd party services. Tools like Google Optimize are great for dipping your toes in the water and doing a few one-off experiments, but if you want to scale, you should really bring experimentation in-house. Building an A/B testing platform completely from scratch is extremely hard and time consuming (expect at least 2,000 hours of work to get something decent). Given this, many people turn to Open Source tools as a starting point.

I like to think of a basic A/B testing platform as several distinct services:

**Targeting and Variation Assignment** is the code that runs within your application that decides which users are put into an A/B test and what variation they see.

**Exposure and Metric Tracking** also runs within your application and records which users saw which variations and what the users ended up doing afterwards.

**Analysis and Reporting** reads the raw data and performs statistical analyses to determine if your variant is better than the control and by how much.

In the following sections, I’ll go through each of these and the available open source options.

# Targeting and Variation Assignment

The most important thing for targeting and variation assignment is performance. Any delay here will be immediately felt by your users and may actually end up invalidating A/B test results.

The biggest offender here, and also surprisingly one of the more popular open source libraries, is [**SixPack**](https://github.com/sixpack/sixpack). SixPack makes an HTTP request to an API (that performs DB read/write operations) before it can assign each variation. These calls can’t be cached and, in my opinion, this completely invalidates SixPack as a serious contender.

Some feature flag libraries like [**Unleash**](https://github.com/Unleash/unleash) do a single HTTP call to an API at the start of the app that fetches all of the data needed to evaluate variations. This is better than SixPack’s approach since the data can be cached more easily, but may still be too expensive for some use cases.

Other feature flagging libraries like [**rollout**](https://github.com/FetLife/rollout) avoid API calls entirely, but still require a round trip to a Redis database. It’s likely your application already relies on Redis in some way for other parts of rendering, so this may not be a huge concern for you.

The fastest options are libraries that evaluate everything locally without any external calls at all. The most popular of these is Facebook’s [**PlanOut**](https://github.com/facebook/planout). The downside of this approach is that any changes to experiments require a code deploy (as opposed to flipping a toggle in an admin UI). Shameless plug time — if you are running A/B tests on the front-end and using React, checkout my [**growthbook-react**](https://github.com/growthbook/growthbook-react) library. It’s extremely fast and easy to use.

The other factor to consider besides performance is the support for complex experiments. Typically, in feature flag tools, A/B testing is kind of an afterthought and thus only the simplest experiments are supported. True A/B testing libraries like PlanOut or growthbook-react can support way more complex use cases — different randomization ids (e.g. userId vs anonymousId), nested experiments, advanced user targeting, etc..

# Exposure and Metric Tracking

This is the process of logging which variation a user is exposed to and what they do afterwards. The end goal is to get this data into a data warehouse or analytics tool that you can query for analysis later. Like variation assignment, this code runs in your app and performance is important, but tracking calls can typically be made asynchronously, so it’s less of a factor.

Real-time user event tracking is actually really hard to do yourself at scale. For most companies, I would recommend using a paid hosted service for this — Segment, Mixpanel, Amplitude, FreshPaint, Fivetran, etc.. You can use Google Analytics for this as well, but be aware it comes with some serious limitations when it comes time to actually query the data and analyze it later.

If you do want to go the open source route, [**RudderStack**](https://github.com/rudderlabs/rudder-server) is a good option. They have a paid hosted version as well if you want to upgrade later. The other open source alternative is to write directly into your database (Postgres, MySQL, MongoDB, Redis, etc.) although beware of scaling issues. Most application databases expect read-heavy traffic and too many analytics writes can cause performance issues.

# Analysis and Reporting

Once you have the exposure and metrics stored together in a database, you need to query the raw data and run statistical analyses on it to determine the effect.

The query to get the data can actually become quite complex. For example, if your goal is to get people to click a button, you need to make sure to only count button clicks AFTER the person is put into a variation. And depending on the context, you may only want to count button clicks within X minutes of seeing the variation. On the other hand, for metrics like “Pages per Session”, you probably want to start counting BEFORE the person is put into the experiment to reduce the variability of the data. For metrics like Revenue, you may want to set a value cap so one random bulk order for $10,000 doesn’t completely screw everything up. Some metrics like Average Order Value need a different denominator (number of orders vs number of users). I routinely see **500+ line SQL queries** for a single experiment!

The statistics involved in A/B test analysis can also be fairly complicated. You can use a simple Student T, Fisher Exact, or Chi-Square test, but make sure you don’t fall prey to the [peeking problem](https://www.evanmiller.org/how-not-to-run-an-ab-test.html). There is [sequential analysis](https://www.evanmiller.org/sequential-ab-testing.html) which doesn’t have a peeking problem, but only applies to very specific metrics. There are [Bayesian](https://www.evanmiller.org/bayesian-ab-testing.html) approaches which are robust, but can be complicated to implement properly.

In addition to the main analysis, you also want to be doing things like Sample Ratio Mismatch (SRM) checks, Bonferroni corrections, and bot detection / outlier removal.

For a quick and dirty analysis, there are some free online calculators out there — [Evan Miller](https://www.evanmiller.org/ab-testing/) is always solid, [A/B Test Guide](https://abtestguide.com/calc/) has another one. We even built our own at [Growth Book](https://www.growthbook.io/ab-calculator).

If you are storing data in MixPanel or Amplitude, they have some built-in reports for analyzing A/B test results, although they are extremely simplistic and make a lot of assumptions about your data that might not be true.

On the open source side, there is [**ExpAn**](https://github.com/zalando/expan) for python, and for R there is Google’s [**AB Package**](https://github.com/google/abpackage) and [**bayesAB**](https://github.com/FrankPortman/bayesAB). Be aware, these libraries are meant to be used by experienced data scientists and it’s really easy to make incorrect assumptions.

Time for another shameless plug — I’m a co-founder of the [**Growth Book App**](https://www.growthbook.io/) , which is a hosted A/B test analysis platform. It connects to your data source, queries the raw data, runs the analysis and creates visualizations of the results. Growth Book uses a Bayesian statistics engine, performs SRM checks, and lets you segment results by various user properties. It’s also a great place to document your experiments by adding screenshots, markdown descriptions, discussion threads, and more!

# Summary

A/B testing needs such a deep product integration that most companies end up bringing it in-house. This can take many months or years of work to build from scratch. Open source tools can help you hit the ground running and evolve over time.

Every situation is unique, so feel free to reach out to us at [**Growth Book**](https://www.growthbook.io/) and we can help you navigate the space and find what’s right for you.
