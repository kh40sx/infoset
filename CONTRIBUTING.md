# How To Contribute
Below is the workflow for having your contribution accepted into the `infoset` repository

1. Create an Issue or comment on an existing issue to discuss the feature
2. If the feature is approved, assign the issue to yourself
3. Fork the project 
4. Clone the fork to your local machine
5. Add the original project as a remote (git remote add upstream https://github.com/UWICompSociety/infoset, check with: git remote -v)
6. Create a topic branch for your change (git checkout -b <<branchName>>)
7. you may create additional brances if modifying multiple parts of the code
8. When you need to synch with upstream (pull down the latest changes), do git fetch upstream -> git checkout master -> git merge upstream/master
9. Check for uneccesary whitespace with git diff --check
   - Exampe proper git commit message 
   "
   Make the example in CONTRIBUTING imperative and concrete ...

     "Without this patch applied the example commit message in the CONTRIBUTING
     document is not a concrete example.  This is a problem because the
     contributor is left to imagine what the commit message should look like
     based on a description rather than an example.  This patch fixes the
     problem by making the example concrete and imperative.

     The first line is a real life imperative statement with a ticket number
     from our issue tracker.  The body describes the behavior without the patch,
     why this is a problem, and how the patch fixes the problem when applied.

     Resolves: #123
     See also: #456, #789
   "
10. Write the necessary unit tests for your changes.
11. Run all the tests to assure nothing else was accidentally broken (run: make test)
12. Perform a pull request
13. Your code will be reviewed
14. If your code passes review, your pull request will be accpeted

# Code Style Guide
For ease of readability and maintainability `infoset` code must follow thse guidelines.
Code that does not comply will not be added to the `master` branch.

1. `infoset` uses the Google Python Style Guide for general style requirements
2. `infoset` uses the The Chromium Projects Python Style Guidelines for docstrings.
3. Indentations must be multiples of 4 blank spaces. No tabs.
4. All strings must be enclosed in single quotes
5. In addition too being pylint compliant, the code must be PEP8 and PEP257 compliant too.
6. There should be no trailing spaces in files

## Sample Bash Script for Pylint, PEP8 and PEP257 Compliance

You can verify your code for compliance using this sample script, where $1 is the file you are verifying.
Ensure that pylint, PEP8 and PEP257 are installed beforehand.
```
#!/bin/bash

# List of error messages to suppress
DISABLE_LIST='W0702,W0703'

# Maximum number of local variables
MAX_LOCALS=20

pylint --reports=no --max-locals=$MAX_LOCALS --disable=$DISABLE_LIST $1
pep8 --show-source $1
pep257 $1
```
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
