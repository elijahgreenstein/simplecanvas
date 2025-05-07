# Prepare module content

In this tutorial, we will add content to the files created by `addmod`.

## Introduction page

Open `intro.md`. It should contain the following text:

```
---
title: "1.1. Introduction"
---
```

As you can see, Simple Canvas provided a default title with a prefix, `1.1.`. This communicates that the introduction is the first item in the first content module. Let's edit our title and add some content as follows:

```
---
title: "1.1. Welcome to \"SC\"!"
---

# Welcome to SC 101!

This week we will learn about Simple Canvas.
```

Recall that we used [Pandoc's Markdown syntax](https://pandoc.org/MANUAL.html#pandocs-markdown) when we drafted the default quiz description in [Part 2 of the tutorial](tutorial-course.html). We must also follow this Markdown syntax to format course pages and [discussion board prompts](#discussion-board).

:::{.note}
**Note:** Notice that we have placed the title text inside quotation marks and that we have escaped quotation marks that are part of the text (`\"SC\"`). Enclose all titles in quotation marks to ensure that Simple Canvas parses the text correctly.
:::

Save and close the file.

## Quizzes

Open `quiz.yaml`. It should contain this [YAML](https://yaml.org)-formatted text:

```
title: "1.2. Quiz"
description: null
times:
  unlock_at: "2025-05-01T17:00:00Z"
  due_at: "2025-05-01T18:00:00Z"
  lock_at: "2025-05-01T18:30:00Z"
questions:
  - question: "What is ..."
    correct:
      - "Answer 1"
      - "Answer 2"
    incorrect:
      - "Answer 3"
      - "Answer 4"
  - question: "Write about ..."
```

Notice that the title, `1.2. Quiz`, indicates that this is the second item in the first content module.

### Quiz settings

Recall that we set default unlock times, deadlines, and lock times for quizzes when we created our course with `newcourse` in the [second tutorial](tutorial-course.html). Notice that Simple Canvas combined those times with our quiz date, `2025-05-01`, to create date-time strings that Canvas can parse.

Additionally notice that the quiz `description` is set to `null`. Simple Canvas will, therefore, use the default quiz description in `SC101/_conf/quiz-desc.md` when we upload the quiz to Canvas in the [next tutorial](tutorial-upload.html). Refer to the [guide to quizzes](howto-quiz.html) to learn how to customize the quiz description for an individual quiz.

### Quiz questions

The default quiz template contains two questions. Note the structure of each question:

- Each question follows the `questions:` line.
- Each question begins with `- question:`, which is offset by two spaces.
- Question text is enclosed in quotation marks and follows `- question:`.

Simple Canvas can handle three kinds of questions:

- Simple Canvas treats questions without answers as an *essay question*. The second question in the template is an essay question.
- Simple Canvas treats questions with only one correct answer as a *multiple choice question*. The template above does not contain a multiple choice question.
- Simple Canvas treats questions with more than one correct answer as a *multiple answers question*. The first question in the template is a multiple answers question.

Notice that answers are divided into two groups: `correct` and `incorrect`. Both of these words are preceded by four spaces to align with the word `question` and both are followed by a colon `:`.

Answers follow either `correct` or `incorrect`. Each answer text is preceded by six spaces, a hyphen `-`, and another space. Each answer is enclosed in quotation marks.

### Multiple choice question

Let's add some questions to our quiz. We will first add a multiple choice question. Remove the text beneath `questions:` and add the following:

```
questions:
  - question: "Which command creates a module?"
    correct:
      - "addmod"
    incorrect:
      - "newcourse"
      - "upmod"
```

This question has only one correct answer. Simple Canvas will treat this question as a multiple choice question.

### Multiple answers question

Let's add a multiple answers question. Add this at the bottom of `quiz.yaml`:

```
  - question: "What are the default module items?"
    correct:
      - "pages"
      - "quizzes"
      - "discussions"
    incorrect:
      - "assignments"
```

This question has three correct answers. Simple Canvas will treat this question as a multiple answers question.

### Essay question

Let's add a final essay question. Add this at the bottom of `quiz.yaml`:

```
  - question: "What do you like about Simple Canvas?"
```

This question does not have answers listed. Simple Canvas will treat this question as an essay question.

Save and close the file.

## Discussion boards

Finally, let's update our discussion board. Open `disc.md`. It should contain this text:

```
---
title: "1.3. Discussion"
---
```

Notice that the title indicates that this is the third item in the first content module.

As with the [introduction page](#introduction-page), we can add Markdown-formatted text to this file. Add this text below the three hyphens `---`:

```
# Overview

Discuss:

1. how to create a new course with Simple Canvas; and
1. how to add a module to your course.
```

Save and close the file.

## Next steps

When you feel comfortable with how to edit pages, quizzes, and discussion boards, go to the [next tutorial](tutorial-upload.html).

Refer to the [guide to quizzes](howto-quiz.html) for more details about quiz customization.

:::{.nav}
[Previous](tutorial-module.html)

[Home](index.html)

[Next](tutorial-upload.html)
:::
