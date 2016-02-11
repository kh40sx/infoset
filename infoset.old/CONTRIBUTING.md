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
