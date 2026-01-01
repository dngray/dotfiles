vim.pack.add({
  { src = "https://github.com/catppuccin/nvim", name = "catppuccin" },
})

vim.opt.termguicolors = true -- Required for 16-million true colors
vim.opt.wrap = true -- Soft wrap lines so emails don't cut off
vim.opt.linebreak = true -- Don't break lines in the middle of words
vim.opt.textwidth = 72 -- Hard wrap standard for plain-text email formatting
vim.opt.spell = true -- Enable spell check for writing drafts

require("catppuccin").setup({ flavour = "mocha" })
vim.cmd.colorscheme("catppuccin")
