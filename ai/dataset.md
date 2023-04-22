https://github.com/togethercomputer/RedPajama-Data

Dataset:
https://gist.github.com/rnirmal/e01acfdaf54a6f9b24e91ba4cae63518

Github Dataset

https://console.cloud.google.com/marketplace/details/github/github-repos?project=warm-lane-316404

https://hoffa.medium.com/github-on-bigquery-analyze-all-the-code-b3576fd2b150

https://console.cloud.google.com/bigquery?p=bigquery-public-data&d=github_repos&page=dataset&project=warm-lane-316404&ws=!1m4!1m3!3m2!1sbigquery-public-data!2sgithub_repos

https://huggingface.co/datasets/codeparrot/github-code

Github on BigQuery:
https://hoffa.medium.com/github-on-bigquery-analyze-all-the-code-b3576fd2b150


All the open source code in GitHub is now available in BigQuery. Go ahead, analyze it all. In this post you’ll find the related resources I know of so far:

**Update:** I know I said all — but it’s not all. I’m updating the answers to these and other questions at [github.com/fhoffa/analyzing_github](https://github.com/fhoffa/analyzing_github).

The pipeline mirrors code from:

-   Projects that have a [clear open source license](https://github.com/blog/2252-license-now-displayed-on-repository-overview).
-   Forks and/or un-notable projects not included.
-   Nevertheless, it represents terabytes of code.

## Official sources:

-   [GitHub announcement](https://github.com/blog/2201-making-open-source-data-more-available).
-   [Google Cloud Blog announcement](https://cloudplatform.googleblog.com/2016/06/GitHub-on-BigQuery-analyze-all-the-open-source-code.html).
-   [Google BigQuery Public Datasets docs](https://cloud.google.com/bigquery/public-data/github).

## In depth analysis

-   Read [Francesc](http://twitter.com/francesc)’s [step-by-step guide](https://medium.com/@francesc/analyzing-go-code-with-bigquery-485c70c3b451#.glhi7lrl4) to analyze Go code. Use these patterns for any other language too :).
-   Run a full JavaScript static code analyzer within a SQL query: [Running JSHint inside BigQuery](https://medium.com/@hoffa/ed0e3011732c).
-   Java imports: [Most used Java imports, from 2013 to 2016](https://medium.com/@hoffa/2a9640056022).
-   Top [Angular directives](https://kozikow.wordpress.com/2016/07/01/top-angular-directives-on-github/).
-   [Tabs or spaces](https://medium.com/@hoffa/400-000-github-repositories-1-billion-files-14-terabytes-of-code-spaces-or-tabs-7cfe0b5dd7fd#.a3y5j7hi5) (the holy wars).
-   SQL commas — [leading or trailing](https://hackernoon.com/winning-arguments-with-data-leading-with-commas-in-sql-672b3b81eac9)?

I’m waiting for your contributions — I will add them here:

-   1 hour after the dataset announcement @thomasdarimont was able to find all the [java projects that declare certain dependency](https://twitter.com/thomasdarimont/status/748259108072079361).
-   [Lakshmanan V](https://medium.com/u/247b0630b5d6?source=post_page-----b3576fd2b150--------------------------------)
    
     “[Popular Java projects on GitHub that could use some help](https://medium.com/google-cloud/popular-java-projects-on-github-that-could-use-some-help-analyzed-using-bigquery-and-dataflow-dbd5753827f4)” (analyzed using BigQuery and Dataflow).
-   [Guillaume Laforge](https://medium.com/u/431147437aeb?source=post_page-----b3576fd2b150--------------------------------)
    
     “What can we learn from [million lines of Groovy code on Github](http://glaforge.appspot.com/article/what-can-we-learn-from-million-lines-of-groovy-code-on-github)?”.
-   Filippo Valsorda “[Analyzing Go Vendoring with BigQuery](https://blog.filippo.io/analyzing-go-vendoring-with-bigquery/)”.
-   Go project uses BigQuery stats [to guide design decisions](https://github.com/golang/go/issues/16447#issuecomment-234386786), [more than once](https://github.com/golang/go/issues/14595#issuecomment-235501992).
-   David Gageot [analyzes 281,212 Docker projects](http://blog.javabien.net/2016/08/01/analysing-docker-projects-on-github-with-bigquery/).
-   [Kan Nishida](https://medium.com/u/1bfa80768afa?source=post_page-----b3576fd2b150--------------------------------)
    
     uses R to [cluster R packages](https://blog.exploratory.io/clustering-r-packages-based-on-github-data-in-google-bigquery-1cadba62eb8d).
-   [Aja Hammerly](https://medium.com/u/ef484db59f33?source=post_page-----b3576fd2b150--------------------------------)
    
     compares most popular gems according to Rubygems.org [download data vs GitHub gem calls](http://www.thagomizer.com/blog/2016/07/15/ruby-meets-bigquery-part-two.html).
-   [Sergey Abakumoff](https://medium.com/u/13832a65f7f1?source=post_page-----b3576fd2b150--------------------------------)
    
     looks at the [most popular npm packages](https://medium.com/@sAbakumoff/using-bigquery-github-data-to-rank-npm-repositories-ecf8947a1182) and [trending keywords](https://medium.com/@sAbakumoff/using-bigquery-github-data-to-find-out-open-source-software-development-trends-e288a2ca3e6b). 
    
    [Justin Beckwith](https://medium.com/u/32b3d805c3ba?source=post_page-----b3576fd2b150--------------------------------)
    
     performs a [similar analysis](http://jbeckwith.com/2016/08/13/bigquery-github/). Sergey follows up with a deeper assessment on why almost empty [packages duplicate all over GitHub](https://medium.com/@sAbakumoff/github-cancer-180db780d99d#.dbbznep13). 
    
    [Sergey Abakumoff](https://medium.com/u/13832a65f7f1?source=post_page-----b3576fd2b150--------------------------------)
    
     also analyzes [Angular vs React](https://medium.com/@sAbakumoff/angular-vs-react-text-analysis-of-commit-messages-1cda199f3bdb) messages.
-   Brent Shaffer [analyzes PHP](https://cloud.google.com/blog/big-data/2016/09/using-bigquery-to-analyze-php-on-github) code and libraries — also test coverage for different languages.
-   A full run down by 
    
    [Egor Zhuk,](https://medium.com/u/a317c5e334e2?source=post_page-----b3576fd2b150--------------------------------)
    
     “[Yet another analysis of Github data with Google BigQuery](https://medium.com/@EgorZhuk/yet-another-analysis-of-github-data-with-google-bigquery-c9e4e6fe39e3)”.
-   [John-David Dalton](https://medium.com/u/c9acea0bae6e?source=post_page-----b3576fd2b150--------------------------------)
    
     informs the travis-ci team on the [counts for Node versions tested](https://github.com/travis-ci/travis-ci/issues/6659#issuecomment-250874104).
-   [Alex Zhitnitsky](https://medium.com/u/c83e31411376?source=post_page-----b3576fd2b150--------------------------------)
    
     reviews 779,236 Java Logging Statements, 1,313 GitHub Repositories to determine “[ERROR, WARN or FATAL](http://blog.takipi.com/779236-java-logging-statements-1313-github-repositories-error-warn-or-fatal/)”?
-   [Florin Badita](https://medium.com/u/3b723c70c152?source=post_page-----b3576fd2b150--------------------------------)
    
     “[Naming conventions in Python import statements](https://medium.com/@baditaflorin/naming-conventions-in-python-import-statements-a-bigquery-adventure-using-the-github-db-dump-d900159ab680)”. Then “[Naming conventions in Python def function()](https://medium.com/@baditaflorin/naming-conventions-in-python-def-function-a-bigquery-adventure-using-the-github-db-dump-8b7a34fc5f72#.4q3xizhtp)”.
-   [Guillaume Laforge](https://medium.com/u/431147437aeb?source=post_page-----b3576fd2b150--------------------------------)
    
     “[Analyzing half a million Gradle build files — Guillaume Laforge’s Blog](http://glaforge.appspot.com/article/analyzing-half-a-million-gradle-build-files)”, 2017 “[Gradle vs Maven and Gradle in Kotlin or Groovy](http://glaforge.appspot.com/article/gradle-vs-maven-and-gradle-in-kotlin-or-groovy)”
-   @anvaka “[analyzed ~2TB of code to build an index of the most common words in programming languages](https://anvaka.github.io/common-words/#?lang=js)”. Cool visualizations, full code on GitHub, and a lot of [comments on reddit](https://www.reddit.com/r/programming/comments/5opk2f/i_analyzed_2tb_of_code_to_build_an_index_of_the/).
-   [Sergey Abakumoff](https://medium.com/u/13832a65f7f1?source=post_page-----b3576fd2b150--------------------------------)
    
     comes back, linking [code to StackOverflow](https://github.com/sAbakumoff/SoCiting2).
-   [Gareth Rushgrove](https://medium.com/u/271f3deb4b07?source=post_page-----b3576fd2b150--------------------------------)
    
     finds all kind of [metrics for Puppet](https://speakerdeck.com/garethr/the-future-of-testing-puppet-code?slide=36).
-   [Justine Tunney](https://medium.com/u/aabd669fa16b?source=post_page-----b3576fd2b150--------------------------------)
    
     tells us how [Googlers used BigQuery and GitHub to patch thousands of vulnerable projects](https://opensource.googleblog.com/2017/03/operation-rosehub.html) ([HN](https://news.ycombinator.com/item?id=13769727)).
-   [Walker Harrison](https://medium.com/u/4fc23f8322e1?source=post_page-----b3576fd2b150--------------------------------)
    
     found the [top imports in Jupyter (.ipynb) notebooks](https://dev.to/walker/using-googles-bigquery-to-better-understand-the-python-ecosystem).
-   [Jake McCrary](https://medium.com/u/8ee04aad1197?source=post_page-----b3576fd2b150--------------------------------)
    
     went for the [top Clojure librarie](http://jakemccrary.com/blog/2017/04/17/what-are-the-most-used-clojure-libraries/)s.
-   [Sebastian Baltes](https://medium.com/u/b021e75201d8?source=post_page-----b3576fd2b150--------------------------------)
    
     went [searching for Stack Overflow code that shows up in GitHub](https://sbaltes.github.io/blog/so-snippets-in-gh-projects) project.
-   [Steren Giannini](https://medium.com/u/ef2e4caf305a?source=post_page-----b3576fd2b150--------------------------------)
    
     found all the [constant regular expressions in Go](https://github.com/golang/go/issues/21463#issuecomment-322679645) — to improve Go’s regex capabilities ([article](https://labs.steren.fr/2017/08/17/extracting-all-go-regular-expressions-found-on-github/)).
-   Matt Warren [analysing C# code on GitHub with BigQuery](http://mattwarren.org/2017/10/12/Analysing-C-code-on-GitHub-with-BigQuery/).
-   [Michał Janaszek](https://medium.com/u/b1e8ffcda395?source=post_page-----b3576fd2b150--------------------------------)
    
     “[State of npm scripts](https://michaljanaszek.com/blog/state-of-npm-scripts)” ([queries](https://gist.github.com/Everettss/12c4f88ad75eaa86bb90430e2bddd6a4)).

A series of posts by Robert Kozikowski:

-   [Advanced GitHub search](https://kozikow.com/2016/06/05/more-advanced-github-code-search/) with BigQuery.
-   [Top emacs packages](https://kozikow.wordpress.com/2016/06/29/top-emacs-packages-used-in-github-repos/) used in GitHub repos.
-   [Visualizing relationships between python packages](https://kozikow.com/2016/07/10/visualizing-relationships-between-python-packages-2/).

## Tips

-   Don’t analyze the main [bigquery-public-data:github_repos.contents] table — at 1.5 TB, it will _instantly_ consume your monthly free terabyte. Use instead the official [bigquery-public-data:github_repos.sample_contents] extract (~23 GB), or one of the full language tables I left at [[fh-bigquery:github_extracts.contents_*](https://bigquery.cloud.google.com/dataset/fh-bigquery:github_extracts)].
-   How about doing a JOIN between this new dataset and the GitHub Archive to find the most starred files and their patterns? Sample code soon, but see how I played with [GitHub stars and Hacker News](https://www.reddit.com/r/bigquery/comments/3shl0o/qotd_what_else_did_they_star_get_to_know_your/) previously.
-   I’m pretty excited about getting author and committer timezones. We’ll be able to perform some regional analysis here.

## Visualizations

-   Google [Data Studio 360 dashboard](https://datastudio.google.com/open/0ByGAKP3QmCjLdXBlWVdrZU5yZW8) (previous post [about Data Studio](https://medium.com/google-cloud/showing-off-the-new-free-google-analytics-data-studio-with-reddit-aprils-gilded-comments-for-ebe965dbbb15)).

![](https://miro.medium.com/v2/resize:fit:1508/1*_uxwTTOd1oRXjmloZ5Qi0g.png)

![](https://miro.medium.com/v2/resize:fit:1638/1*Ud8ZAz1xoVWK9DfiX6_hBg.png)

![](https://miro.medium.com/v2/resize:fit:720/1*AM3e4amUqLdx4sFbpATMdA.png)

![](https://miro.medium.com/v2/resize:fit:674/1*D0IEdLQp0FKD-Iz9lG_Idw.png)

## More resources

-   Podcast: Myself, Will Curran, and Arfon Smith talk about the details of this announcement and more on [The Changelog #209](https://changelog.com/209/).
-   [GitHub Archive](https://www.githubarchive.org/), monitoring GitHub since 2011.

## Press

-   [Venture Beat](http://venturebeat.com/2016/06/29/github-releases-data-on-2-8-million-open-source-repositories-through-google-bigquery/).

## Social media

-   [/r/bigquery](https://www.reddit.com/r/bigquery/comments/4qhlog/all_the_open_source_code_in_github_now_shared/)
-   [Hacker News](https://news.ycombinator.com/item?id=12004442)

Stay curious! And find me on Twitter at [@felipehoffa](https://twitter.com/felipehoffa).
