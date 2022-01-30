" Display settings
set termguicolors
set background=dark     " enable for dark terminals
set wrap                " wrap lines
set linebreak           " wrap words to new line
set scrolloff=3         " 2 lines above/below cursor when scrolling
set sidescrolloff=5     " 5 spaces scroll off to sides
set number              " show line numbers
set showbreak=↪         " show arrow at wrap
"set relativenumber     "

" Colorscheme and highlighting
syntax enable
set background=dark
set hlsearch          " highlight search
set incsearch         " search incremently (search while typing)

colorscheme selenized

" Correct comment highlighting for json
autocmd FileType json syntax match Comment +\/\/.\+$+

" cursor line
set cursorline          " show cursor line
highlight CursorLine cterm=NONE
set laststatus=2 " Show Infoline at bottom always

" http://vim.wikia.com/wiki/Highlight_unwanted_spaces
highlight ExtraWhitespace ctermbg=red guibg=red
augroup WhitespaceMatch
  " Remove ALL autocommands for the WhitespaceMatch group.
  autocmd!
  autocmd BufWinEnter * let w:whitespace_match_number =
        \ matchadd('ExtraWhitespace', '\s\+$')
  autocmd InsertEnter * call s:ToggleWhitespaceMatch('i')
  autocmd InsertLeave * call s:ToggleWhitespaceMatch('n')
augroup END
function! s:ToggleWhitespaceMatch(mode)
  let pattern = (a:mode == 'i') ? '\s\+\%#\@<!$' : '\s\+$'
  if exists('w:whitespace_match_number')
    call matchdelete(w:whitespace_match_number)
    call matchadd('ExtraWhitespace', pattern, 10, w:whitespace_match_number)
  else
    " Something went wrong, try to be graceful.
    let w:whitespace_match_number =  matchadd('ExtraWhitespace', pattern)
  endif
endfunction

