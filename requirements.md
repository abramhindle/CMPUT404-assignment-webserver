# Build a webserver! </br>
## Description

   Your task is to build a partially HTTP 1.1 compliant
   webserver. Your webserver will serve static content from the www
   directory in the same directory that you start the webserver in.

   You are meant to understand the very basics of HTTP by having a
   hands-on ground up understanding of what it takes to have an HTTP
   connection.

## Collaboration
   * You may consult with others but the submission should be your
     own source code.
   * Collaboration must be documented in the README.md file
   * Any external source code must be referenced and documented in
     the README.md file

## User Stories
   * As a user I want to view files in ./www via a webbrowser
   * As a user I want to view files in ./www via curl
   * As a webserver admin I want to serve HTML and CSS files from ./www
   * As a webserver admin I want ONLY files in ./www and deeper to be
     served.

## Requirements
   * [&nbsp;&nbsp;] The webserver can serve files from ./www
   * [&nbsp;&nbsp;] The webserver can be run using the runner.sh file
   * [&nbsp;&nbsp;] The webserver can pass all the tests in freetests.py
   * [&nbsp;&nbsp;] The webserver can pass all the tests in not-free-tests.py
     (you only have part of this one, I reserve the right to add tests)
   * [&nbsp;&nbsp;] The webserver supports mime-types for HTML
   * [&nbsp;&nbsp;] The webserver supports mime-types for CSS
   * [&nbsp;&nbsp;] The webserver can return index.html from directories (paths
     that end in /)
   * [&nbsp;&nbsp;] The webserver can server 404 errors for paths not found
   * [&nbsp;&nbsp;] The webserver works with Firefox and Chromium
     http://127.0.0.1:8080/
   * [&nbsp;&nbsp;] The webserver can serve CSS properly so that the front page
     has an orange h1 header.
   * [&nbsp;&nbsp;] I can check out the source code via an HTTP git URL
   * [&nbsp;&nbsp;] Provide a screenshot (commit and push it!) of Firefox at
     http://127.0.0.1:8080/ and http://127.0.0.1:8080/deep/
   * [&nbsp;&nbsp;] Return a status code of "405 Method Not Allowed" for any method you cannot handle (POST/PUT/DELETE)

## Restrictions
   * [&nbsp;&nbsp;] Use Python3
   * [&nbsp;&nbsp;] Must run in the undergrad lab (Ubuntu 12.04)
   * [&nbsp;&nbsp;] License your webserver properly (use an OSI approved license)
     * Put your name on it!
   * [&nbsp;&nbsp;] You cannot use a Web Server library

## Recommendations
   * Use the server.py skeleton. Handling sockets yourself is not
     that fun
   * Keep it short, keep it modular

## Submission Instructions
   * Fork my repository from github
     https://github.com/abramhindle/CMPUT404-assignment-webserver
   * Push your commits to your fork
   * In EClass for this assignment submit a URL to the git
     repository. I would prefer github for the host.
     * Line 1: the git URL
     * Line 2: Your CCID
     * Line 3: Your collaborator's CCID

   * To mark your assignment I should be able to type: <br/>
     `git clone http://github.com/youruserid/thisassignment.git yourccid`<br/>
     `cd yourccid`<br/>
     `bash runner.sh`
   * Marks will be deducted if I cannot successfully do this.


## Marking
   * 4 Marks for passing all of freetests.py
   * 2 Marks for passing all of not-free-tests.py
   * 1 Mark Firefox screenshots
