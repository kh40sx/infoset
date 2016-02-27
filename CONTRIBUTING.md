# How To Contribute

Below is the workflow for having your contribution accepted into the `infoset` repository.

1. Create an Issue or comment on an existing issue to discuss the feature
2. If the feature is approved, assign the issue to yourself
3. Fork the project 
4. Clone the fork to your local machine
5. Run `make setup` to install dependencies to virtualenv (information about virtualenv found further below in this doc)
6. Add the original project as a remote (git remote add upstream https://github.com/UWICompSociety/infoset, check with: git remote -v)
7. Create a topic branch for your change (git checkout -b <<branchName>>)
8. you may create additional brances if modifying multiple parts of the code
9. Write code and Commit your changes locally. Exampe proper git commit message below:
   "
   Make the example in CONTRIBUTING imperative and concrete ...

     Without this patch applied the example commit message in the CONTRIBUTING
     document is not a concrete example.  This is a problem because the
     contributor is left to imagine what the commit message should look like
     based on a description rather than an example.  This patch fixes the
     problem by making the example concrete and imperative.

     The first line is a real life imperative statement with a ticket number
     from our issue tracker.  The body describes the behavior without the patch,
     why this is a problem, and how the patch fixes the problem when applied.

     Resolves Issue: #123
     See also: #456, #789
   "

10. When you need to synch with upstream (pull the latest changes from main repo into your current branch), do: git fetch upstream -> -> git merge upstream/master. (or run `make synch` to let the projects makefile handle synching)
11. Check for uneccesary whitespace with git diff --check. 10. Write the necessary unit tests for your changes.
12. Run all the tests to assure nothing else was accidentally broken (run: `make test`)
13. Push your changes to your forked repository (git push origin <<BRANCH>>)
14. Perform a pull request on github
15. Your code will be reviewed
16. If your code passes review, your pull request will be accpeted

The `make contribute` command encapsulates steps 8 to 12 when you are ready to make a pull request.
The `make synch` command will synch your repository

# Code Style Guide

For ease of readability and maintainability `infoset` code must follow thse guidelines.
Code that does not comply will not be added to the `master` branch.

1. `infoset` uses the Google Python Style Guide for general style requirements
2. `infoset` uses the The Chromium Projects Python Style Guidelines for docstrings.
3. Indentations must be multiples of 4 blank spaces. No tabs.
4. All strings must be enclosed in single quotes
5. In addition too being pylint compliant, the code must be PEP8 and PEP257 compliant too.
6. There should be no trailing spaces in files

## Guidelines to remember
* Always opt for the most pythonic solution to a problem
* Avoid applying idoms from other programming languages
* Import each module with its full path name. ie: from pack.subpack import module
* Use exceptions where appropriate ( https://google.github.io/styleguide/pyguide.html#Exceptions )
* Use doc strings ( http://sphinxcontrib-napoleon.readthedocs.org/en/latest/example_google.html )
* Try not to have returns at multiple points in a function unless they are failure state returns
* If you are in the middle of a development session and have to interrupt your work, it is a good idea to write a broken unit test about what you want to develop next. When coming back to work, you will have a pointer to where you were and get back on track faster.

## Commits

`infoset` strives to maintain a proper log of development through well structured git commits.
The link below offer insight and advice on the topic of commit messages:
https://robots.thoughtbot.com/5-useful-tips-for-a-better-commit-message
http://chris.beams.io/posts/git-commit/

## PEP8 and PEP257 Compliance

You can verify your code for compliance using running the `make lint` command from the project root.

## VirtualEnv

`virtualenv` is a tool to create isolated Python environments.
It creates an environment that has its own installation directories,
that doesn’t share libraries with other virtualenv environments nor does it access the globally installed libraries either.

The `infoset` project's makefile wil automatically set up a makefile for you once you have virutalenv installed globally.
All dependencies that `infoset` requires, aside from pip and virtualenv itself, will be installed to this virtual env.
The makefile will run commands such as `nosetests` from the virtual env. If you wish to run these commands manually,
run them as `venv/bin/nosetests` as they would not have been installed to your machine globally.

## Sample .vimrc File for Compliance

You can use this sample .vimrc file to help meet our style requirements

```
" Activate syntax
syntax on
" set number

" Disable automatic comment insertion
autocmd FileType * setlocal formatoptions-=c formatoptions-=r formatoptions-=o

" Delete trailing whitespace
autocmd BufWritePre * :%s/\s\+$//e

" Convert tabs to spaces
set expandtab

" Set tabs to 4 spaces
set tabstop=4

" Set the number of spaces for indentation
set shiftwidth=4

" Switch on highlighting the last used search pattern when the terminal has colors
if &t_Co > 2 || has("gui_running")
  set hlsearch
endif

" Tell vim to remember certain things when we exit
"  '10  :  marks will be remembered for up to 10 previously edited files
"  "100 :  will save up to 100 lines for each register
"  :20  :  up to 20 lines of command-line history will be remembered
"  %    :  saves and restores the buffer list
"  n... :  where to save the viminfo files
set viminfo='10,\"100,:20,%,n~/.viminfo

" Function for viminfo to work
function! ResCur()
  if line("'\"") <= line("$")
    normal! g`"
    return 1
  endif
endfunction

" Function for viminfo to work
augroup resCur
  autocmd!
  autocmd BufWinEnter * call ResCur()
augroup END

```
