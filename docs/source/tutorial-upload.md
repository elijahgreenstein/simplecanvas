# Upload materials to Canvas

In this tutorial, we will use Simple Canvas to upload our course materials to Canvas LMS.

## The upload command

Simple Canvas makes the upload of modules simple. Make sure that `SC101` is the current working directory; then type this command and press [enter]{.scode}:

```
python -m simplecanvas -v upmod Week_01
```

We used the "verbose" option `-v` to make Simple Canvas print messages about the upload process. If our settings are configured correctly, Simple Canvas should print the following:

```
Uploading module: 'Week_01'
- Posting module ...
    - Status: 200
- Posting item '1.1. Welcome to "SC"!' ...
    - Status: 200
- Posting item '1.2. Quiz' ...
    - Status: 200
- Posting item '1.3. Discussion' ...
    - Status: 200
- Moving item '1.1. Welcome to "SC"!' ...
    - Status: 200
- Moving item '1.2. Quiz' ...
    - Status: 200
- Moving item '1.3. Discussion' ...
    - Status: 200
- Adding questions to '1.2. Quiz' ...
    - Status: 200
    - Status: 200
    - Status: 200
- Updating points for '1.2. Quiz' ...
    - Status: 200
```

Note the steps in the process:

- Simple Canvas first *creates* ("posts") the module.
- Simple Canvas then creates each module item (introduction page, quiz, and discussion).
- Simple Canvas then *moves* each item to the module.
- Simple Canvas then adds each question to the quiz.
- Finally, Simple Canvas updates the possible points for the quiz.

:::{.note}
**Note:** A status code of `200` indicates success. Any other status codes indicate a problem and a failure to post, move, or update the listed item.

To identify possible issues, first try a test run. Replicate the command above but type `-t` before `upmod`. Simple Canvas will print content from the expected API call.

If the problem is still unclear, replicate the above command but replace `-v` with `-vv` for additional verbosity. Simple Canvas will print the responses received with each API call.
:::

## Next steps

Content uploads are as simple as that! For additional customization, refer to the how-to guides:

- [How to customize course settings](howto-course.html)
- [How to customize module settings](howto-module.html)
- [How to customize quizzes](howto-quiz.html)

:::{.nav}
[Previous](tutorial-content.html)

[Home](index.html)

\
:::
