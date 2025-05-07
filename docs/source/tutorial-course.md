# Set up a new course

In this tutorial, we will use the Simple Canvas command line interface to set up a new course: "SC101 -- Simple Canvas 101."

## Preparation

We will need an access token to make API calls to Canvas. Follow the [Canvas instructions](https://community.canvaslms.com/t5/Canvas-Basics-Guide/How-do-I-manage-API-access-tokens-in-my-user-account/ta-p/615312) to generate an access token. We will use the token shortly.

Next, determine the API URL for your institution. The URL will look similar to `https://canvas.YOURINSTITUTION.edu/api/v1`. Be prepared to copy this URL shortly.

Finally, let's prepare a directory for our courses. Type the command below and press [enter]{.scode} to create a directory named `courses` and make it the working directory:

```
mkdir courses && cd courses
```

## New course command

We are now ready to set up a new course with Simple Canvas. Type the following command and press [enter]{.scode}:

```
python -m simplecanvas newcourse SC101
```

Simple Canvas will now ask you a series of questions:

`> Enter API token`
~ Copy the access token that you generated on Canvas, paste it here, and press [enter]{.scode}.

`> Enter API URL:`
~ Copy the API URL for your institution, paste it here, and press [enter]{.scode}.

`> Enter course unique identifier:`
~ Open your course on Canvas. The URL will end with the path `courses/<UID>`. Type the identifier in place of `<UID>` and press [enter]{.scode}.

`> Enter quiz unlock time:`
~ Simple Canvas will set up a default time to unlock each module quiz. Enter the default unlock time in Coordinated Universal Time (UTC), in the format `HH:MM:SS`. For example, let's say that we want our quizzes to unlock at 10:00 AM Pacific Daylight Time (PDT). PDT is seven hours behind UTC, so type `17:00:00` and press [enter]{.scode}.

`> Enter quiz deadline:`
~ Simple Canvas will set up a default deadline for each module quiz. Let's say that we want students to complete the quizzes by 11:00:00 AM PDT, one hour after quizzes unlock. Type `18:00:00` and press [enter]{.scode}.

`> Enter quiz lock time:`
~ Students will not be able to access quizzes after the lock time. Let's give students an extra 30 minutes to submit a late quiz. Type `18:30:00` and press [enter]{.scode}.

Simple Canvas will now create a new directory, `SC101`, several sub-directories, and configuration files.

## File structure

Let's explore the files and directories set up by Simple Canvas:

```
SC101/
    _conf/
        quiz-desc.md
        settings.yaml
        token
    modules/
```

The `_conf` directory contains our course configuration files. We will edit a few of them to finalize our course set up.

The `modules` directory is for our course modules. We will set up a new module in the [next tutorial](tutorial-module.html).

## Default quiz description

We can edit `SC101/_conf/quiz-desc.md` to prepare a default quiz description. We will format the quiz description with [Pandoc's Markdown syntax](https://pandoc.org/MANUAL.html#pandocs-markdown). Open `quiz-desc.md`, delete any text, and write the following:

```
# Overview

This is an open-book quiz:

- You **may** refer to course materials and notes.
- You **may not** ask classmates, friends, or others for help.

# Deadline

Submit your quiz by 11:00 AM.
```

:::{.note}
**Note:** Notice that we have used a level-one heading: `# Overview`. Canvas reserves level-one `<h1>` tags for webpage titles. Simple Canvas therefore shifts all headings down one level. Use level-one headings for top-level headings in all content files; Simple Canvas will convert these to level-two, `<h2>` tags.
:::

Save and close `quiz-desc.md`. Simple Canvas will use the above description for each quiz, unless we provide an alternative description. Refer to the [guide to quizzes](howto-quiz.html) for details about quiz customization.

## Token

Simple Canvas wrote our Canvas access token to `SC101/_conf/token`. If your access token changes, you can replace the token in this file.

:::{.warning}
**Warning:** Do not make the access token public. If you use Git for version control for your course, add `token` to your `.gitignore` file.
:::

## Next steps

When you feel comfortable with the Simple Canvas `newcourse` command, go to the [next tutorial](tutorial-module.html).

Refer to the [guide to course settings](howto-course.html) for additional details about how to customize your course.

:::{.nav}
[Previous](tutorial-install.html)

[Home](index.html)

[Next](tutorial-module.html)
:::

