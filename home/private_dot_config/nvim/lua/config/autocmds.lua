-- Autocmds are automatically loaded on the VeryLazy event
-- Default autocmds that are always set: https://github.com/LazyVim/LazyVim/blob/main/lua/lazyvim/config/autocmds.lua
-- Add any additional autocmds here

local function augroup(name)
  return vim.api.nvim_create_augroup("lazyvim_" .. name, { clear = true })
end

vim.api.nvim_create_autocmd({ "BufNewFile", "BufRead" }, {
  group = augroup("gotmpl_highlight"),
  pattern = "*.tmpl",
  command = "setlocal ft=gotmpl",
})

-- -- Disable autoformat for lua files
-- vim.api.nvim_create_autocmd({ "FileType" }, {
--   pattern = { "lua" },
--   callback = function()
--     vim.b.autoformat = false
--   end,
-- })
