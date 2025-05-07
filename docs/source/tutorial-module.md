# Set up a new module

In this tutorial, we will use Simple Canvas to add a new module to our course.

## Add a module

Change the working directory to `SC101`. Then, type this command and press [enter]{.scode}:

```
python -m simplecanvas addmod Week_01
```

Simple Canvas will ask you a series of questions:

`> Enter module title:`
~ The name of the module as it will appear in Canvas. Type `Example module` and press [enter]{.scode}.

`> Enter module position:`
~ This is the position among the modules on campus. Let's assume that we want to keep an information module at the top of our list of modules. `Week_01` will, therefore, be our second module. Type `2` and press [enter]{.scode}.

`> Enter module prefix:`
~ Simple Canvas automatically prefixes the title of each item in the module (page, quiz, discussion) with a number. This is our first content module, so type `1` and press [enter]{.scode}.

`> Enter quiz date:`
~ The Simple Canvas `addmod` command automatically creates a quiz. Enter the quiz date in the format [YYYY-MM-DD]{.scode}. For example, type `2025-05-01` and press [enter]{.scode}.

Simple Canvas will now create a new directory, `Week_01`, and several files in it.

## File structure

Let's explore the files set up by Simple Canvas in `SC101/modules/Week_01`:

```
SC101/
    _conf/
    modules/
        Week_01/
            _conf.yaml
            disc.md
            intro.md
            quiz.yaml
```

Simple Canvas wrote module settings to `_conf.yaml`. Refer to the [guide to module settings](howto-module.html) to learn how to customize these settings.

Simple Canvas also prepared three files for our module content. By default, Simple Canvas organized these in the following order:

1. `intro.md`: an introduction page
1. `quiz.yaml`: a quiz
1. `disc.md`: a discussion board

We will edit these files in the [next tutorial](tutorial-content.html).

## Next steps

When you feel comfortable with `addmod`, go to the [next tutorial](tutorial-content.html).

Refer to the [guide to module settings](howto-module.html) for additional details about how to customize your module.

:::{.nav}
[Previous](tutorial-course.html)

[Home](index.html)

[Next](tutorial-content.html)
:::
