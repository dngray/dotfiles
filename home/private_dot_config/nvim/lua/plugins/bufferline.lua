return {
  -- TODO: remove this when this pr gets merged: https://github.com/LazyVim/LazyVim/pull/6354
  "akinsho/bufferline.nvim",
  init = function()
    local bufline = require("catppuccin.groups.integrations.bufferline")
    function bufline.get()
      return bufline.get_theme()
    end
  end,
}
