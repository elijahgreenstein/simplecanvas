# How to customize course settings

## Setup

Create a new course:

```
python -m simplecanvas newcourse <NAME>
```

Answer the question prompts from Simple Canvas. After Simple Canvas creates course files, open `<NAME>/_conf/settings.yaml`.

## Default settings

The default settings are shown below, where `<USER>` represents answers to the Simple Canvas prompts.

```
course:
  course_name: "<NAME>"
  course_id: "<USER>"
  course_url: <USER>
discussion:
  discussion_type: threaded
  published: false
quiz:
  hide_results: always
  quiz_type: assignment
  shuffle_answers: true
times:
  unlock_at: "<USER>"
  due_at: "<USER>"
  lock_at: "<USER>"
```

## Change discussion settings

Default discussion settings follow `discussion`. The [Canvas API documentation](https://canvas.instructure.com/doc/api/index.html) provides details about other options for "[Discussion Topics](https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics.create)". Follow [YAML](https://yaml.org) syntax to add other parameters.

### Example

```
discussion:
  discussion_type: threaded
  published: false
  require_initial_post: true
  sort_order: asc
```

With these settings, Simple Canvas will upload discussions that:

1. are "threaded,"
1. are not published at upload (instructors will need to publish them manually on Canvas),
1. require students to make a post before viewing other posts, and
1. are sorted in "ascending" order.

:::{.note}
**Note:** Boolean options take the values `true` or `false`. One-word strings do not need to be placed in quotation marks (`string`). Strings with punctuation should be placed in quotation marks (`"string: punctuation"`) to ensure that Simple Canvas parses the text correctly.
:::

## Change quiz settings

Default quiz settings follow `quiz`. The [Canvas API documentation](https://canvas.instructure.com/doc/api/index.html) provides details about other options for "[Discussion Topics](https://canvas.instructure.com/doc/api/quizzes.html#method.quizzes/quizzes_api.create)". Follow [YAML](https://yaml.org) syntax to add other parameters.

### Example

```
quiz:
  hide_results: always
  quiz_type: practice_quiz
  shuffle_answers: true
  time_limit: 5
  one_question_at_a_time
```

With these settings, Simple Canvas will upload quizzes that:

1. hide results,
1. are practice quizzes rather than assignments,
1. shuffle answers,
1. impose a five-minute time limit,
1. and require students to answer questions one at a time.

## Change quiz times

Edit the times following `unlock_at`, `due_at`, and `lock_at` to change the default quiz times.

:::{.note}
**Note:** This may be necessary during a term due to changes to/from daylight savings time.
:::

