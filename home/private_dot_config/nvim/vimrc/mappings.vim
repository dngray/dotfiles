let mapleader = ','     " set leader shortcut to a comma

" VimTex mapping for inkscape-figures {{{
" https://github.com/gillescastel/inkscape-figures#vim-mappings
inoremap <C-f> <Esc>: silent exec '.!inkscape-figures create "'.getline('.').'" "'.b:vimtex.root.'/figures/"'<CR><CR>:w<CR>
nnoremap <C-f> : silent exec '!inkscape-figures edit "'.b:vimtex.root.'/figures/" > /dev/null 2>&1 &'<CR><CR>:redraw!<CR> " }}}

" UltiSnips {{{
" Trigger configuration. Do not use <tab> if you use https://github.com/Valloric/YouCompleteMe.
let g:UltiSnipsExpandTrigger="<C-e>"
let g:UltiSnipsListSnippets="<c-l>"
let g:UltiSnipsJumpForwardTrigger="<c-b>"
let g:UltiSnipsJumpBackwardTrigger="<c-z>"

inoremap <c-x><c-k> <c-x><c-k>

" }}}

" markdown-preview.nvim {{{

" normal/insert
nmap <C-s> <Plug>MarkdownPreview
nmap <M-s> <Plug>MarkdownPreviewStop
nmap <C-p> <Plug>MarkdownPreviewToggle

" }}}

" Coc.vim {{{
map <leader>cld :CocList diagnostics<CR>
map <leader>a :CocAction<CR>
map <leader>fa :CocCommand markdownlint.fixAll<CR>
" }}}

" Show file manager
map <C-p> :FZF<CR>

" vim:foldmethod=marker:foldlevel=0
