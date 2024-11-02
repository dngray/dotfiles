local function shouldLoadPlugin()
  if vim.g.email then
    return false
  end
  return true
end

return {
  {
    "saghen/blink.cmp",
    cond = shouldLoadPlugin,
  },
  {
    "lervag/vimtex",
    cond = shouldLoadPlugin,
  },
}
