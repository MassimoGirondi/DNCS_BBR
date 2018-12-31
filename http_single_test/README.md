This test simulates the download of a single large file from an HTTP server over a link with some losses.

The files are generated through the `generate_files.sh` script and they are served through nginx.
The content of each file is random data, so any way of compressing them should be almost useless.

Run `http_singleTest.py` to run the network and the tests, then `http_singleGraph.py` to generate new plots.
