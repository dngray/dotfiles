-- ~/.config/nvim/lazy-email.lua

-- Ensure lazy.nvim is installed
local lazypath = vim.fn.stdpath("data") .. "/site/pack/packer/start/lazy.nvim"
if vim.fn.isdirectory(lazypath) == 0 then
  -- If lazy.nvim is not installed, clone it
  vim.fn.system({
    "git",
    "clone",
    "https://github.com/folke/lazy.nvim.git",
    lazypath,
  })
end

-- Add lazy.nvim to runtime path
vim.opt.rtp:prepend(lazypath)

-- Setup lazy.nvim with plugins
require("lazy").setup({
  -- Load catppuccin plugin
  { "catppuccin/nvim" },
})

-- Set colorscheme to catppuccin-mocha
vim.cmd("colorscheme catppuccin-mocha")
