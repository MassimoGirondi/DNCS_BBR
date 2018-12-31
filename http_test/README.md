This test simulates the action of browsing a complex webpage over a link with some losses.

From a `page.har` file, which can be obtained through any browser's developer console, random files are generated
under the folder `page` running the script `har_analyze.py`. The files have the same size of the requests contained in the
`page.har` file. With `page_stats.py` you can obtain a plot showing the page structure.

Run `http_Test.py` to run the network and the tests, then `http_Graph.py` to generate new plots.
