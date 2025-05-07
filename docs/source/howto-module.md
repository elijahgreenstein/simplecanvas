# How to customize module settings

## Setup

Set up a new module with `addmod` (replace `<MODULE>` with the module name):

```
python -m simplecanvas addmod <MODULE>
```

Answer the questions from Simple Canvas. Simple Canvas will create the files listed below under `<MODULE>`:

```
<COURSE>/
    modules/
        <MODULE>/
            _conf.py
            disc.md
            intro.md
            quiz.yaml
```

## Default settings

Simple Canvas sets up the default module settings in `<MODULE>/_conf.py`. Default settings appear as below, where `<USER>` represents user replies to Simple Canvas prompts:

```
module_name: "<MODULE>"
title: "<USER>"
position: <USER>
item_order:
  - [intro.md, page]
  - [quiz.yaml, quiz]
  - [disc.md, disc]
```

## Default module files

By default, Simple Canvas creates three files with `addmod`:

1. `intro.md`: an introduction page
1. `quiz.yaml`: a quiz
1. `disc.md`: a discussion board


## Remove an item

Simple Canvas will only upload files named in the list under `item_order`. To remove an item from the module, delete the corresponding line.

### Example

```
item_order:
  - [intro.md, page]
  - [disc.md, disc]
```

With the above settings, Simple Canvas will only upload the introduction page and discussion board prompt. Simple Canvas will ignore all other files in `modules/<MODULE>`.

## Reorder the items

Simple Canvas will order the content on Canvas in the order the files appear under `item_order`. Reorder the list before any upload to Canvas to determine the order of items uploaded with `upmod`.

```
item_order:
  - [disc.md, disc]
  - [quiz.yaml, quiz]
  - [intro.md, page]
```

With the above settings, Simple Canvas will order the items in the module as follows: first a discussion board, then a quiz, last a page.

:::{.note}
**Note:** Simple Canvas prefixes the title of each default item with a numeric code that follows the default order. Edit the title in each file to correspond to the new order. For example, change `1.3. Discussion` to `1.1. Discussion`. Alternatively, remove the numeric code: `Discussion`.
:::

## Add items

Simple Canvas will upload all files in `modules/<MODULE>` listed under `item_order`. To add a new file, add an entry to the list. Write the entry with the form:

```
  - [<FILE_NAME>, <ITEM_TYPE>]
```

:::{.note}
**Note:** Two spaces precede the hyphen `-`.
:::

Write the file name in `modules/<MODULE>` in place of `<FILE_NAME>`. Write the type of the item in place of `<ITEM_TYPE>`. Simple Canvas supports three item types: `page`, `quiz`, or `disc` (discussion).

### Example

```
item_order:
  - [welcome.md, page]
  - [notes.md, page]
  - [discussion.md, disc]
  - [check.yaml, quiz]
  - [thoughts.md, disc]
  - [review.yaml, quiz]
  - [handout.md, page]
```

With the above settings, Simple Canvas will upload three pages, two discussions, and two quizzes to Canvas with the `upmod` command. Note that the names of the files do not correspond to the default names (`intro.md`, `quiz.yaml`, and `disc.md`). Simple Canvas can upload files with any name, as long as (1) the file appears under `item_order`, (2) the type of the file follows the file name, and (3) the file exists in `modules/<MODULE>`.

