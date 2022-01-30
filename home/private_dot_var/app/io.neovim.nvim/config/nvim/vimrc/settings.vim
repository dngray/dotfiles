"function! FileSize()
"    let bytes = getfsize(expand("%:p"))
"    if bytes <= 0
"        return ""
"    endif
"    if bytes < 1024
"        return bytes . "B"
"    else
"        return (bytes / 1024) . "kB"
"    endif
"endfunction

set showmatch           " show matching bracket (briefly jump)
set showmode            " show mode in status bar (insert/replace/...)
set showcmd             " show typed command in status bar
set ruler               " show cursor position in status bar
set title               " show file in titlebar
set wildmenu            " completion with menu
"set confirm            " add confirmation menu
set nolazyredraw        " Don't redraw while executing macros
autocmd FocusGained * :redraw! " Redrawing when regaining focus

" editor settings
set ignorecase          " case insensitive searching
set smartcase           " but become case sensitive if you type uppercase characters
set autoindent          " smart auto indenting
set smartindent         " smart auto indenting
set smarttab            " smart tab handling for indenting
set nopaste             " correctly pasting in vim
set nocp
set errorbells          " Turn on error bell
set shell=bash
set backspace=eol,start,indent
set tabstop=4           " number of spaces a tab counts for
set shiftwidth=4        " spaces for autoindents
set softtabstop=4
set expandtab           " turn a tabs into spaces

" Language indentation
augroup langindentation
	autocmd Filetype c setlocal expandtab tabstop=2 shiftwidth=2 softtabstop=2
	autocmd Filetype cpp setlocal expandtab tabstop=2 shiftwidth=2 softtabstop=2
	autocmd Filetype css setlocal expandtab tabstop=2 shiftwidth=2 softtabstop=2
	autocmd Filetype javascript setlocal expandtab tabstop=2 shiftwidth=2 softtabstop=2
	autocmd Filetype html setlocal expandtab tabstop=2 shiftwidth=2 softtabstop=2
	autocmd Filetype json setlocal expandtab tabstop=2 shiftwidth=2 softtabstop=2
	autocmd Filetype scss setlocal expandtab tabstop=2 shiftwidth=2 softtabstop=2
	autocmd Filetype php setlocal expandtab tabstop=2 shiftwidth=2 softtabstop=2
	autocmd Filetype yaml setlocal expandtab tabstop=2 shiftwidth=2 softtabstop=2
augroup END

" misc settings
set fileformats=unix,dos          " only detect unix file format, displays that ^M with dos files
set viminfo='20,\"500             " remember copy registers after quitting in the .viminfo file -- 20 jump links, regs up to 500 lines'
set hidden                        " remember undo after quitting
set history=200                   " keep 200 lines of command history
set mouse=a                       " use mouse in visual mode (not normal,insert,command,help mode
set mousehide                     " hide the mouse while typing
set clipboard=unnamed,unnamedplus " yank and paste with the system clipboard
set printoptions=header:0,duplex:long,paper:a4 " Printing options

" netrw - https://shapeshed.com/vim-netrw/
" Netrw options
map <F2> :Lexplore<cr>

" hide banner
let g:netrw_banner = 0
" hide swp, DS_Store files
let g:netrw_list_hide='.*\.swp$,\.DS_Store'
" set tree style listing
let g:netrw_liststyle=3
" display directories first
let g:netrw_sort_sequence='[\/]$'
" ignore case on sorting
let g:netrw_sort_options='i'
" vspilt netrw to the left window
let g:netrw_altv = 1
" 30% of the screen for the netrw window, 70% for the file window
let g:netrw_winsize = 15
" open file in a previous buffer (right window)
let g:netrw_browse_split = 4
" buffer setting
let g:netrw_bufsettings = 'nomodifiable nomodified readonly nobuflisted nowrap number'
