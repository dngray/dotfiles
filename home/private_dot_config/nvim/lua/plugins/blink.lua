return {
  -- Plugin: saghen/blink.cmp
  -- A plugin for handling completion behavior (built on top of nvim-cmp).
  "saghen/blink.cmp",

  -- Configuration options for the plugin
  opts = function(_, opts)
    -- Set a buffer-local variable to track if completion is enabled
    vim.b.completion = true

    -- Create a toggle using the 'Snacks' plugin (assumed helper library)
    -- Allows you to toggle completion on/off with <leader>uk
    Snacks.toggle({
      name = "Completion", -- Name shown in toggle UI
      get = function()
        return vim.b.completion -- Gets the current state
      end,
      set = function(state)
        vim.b.completion = state -- Sets the new state
      end,
    }):map("<leader>uk") -- Keybinding for toggle

    -- Enable the plugin only if completion is not explicitly disabled
    opts.enabled = function()
      return vim.b.completion ~= false
    end

    -- Ensure opts.completion and opts.completion.list exist
    opts.completion = opts.completion or {}
    opts.completion.list = opts.completion.list or {}

    -- Configure selection behavior for the completion list
    opts.completion.list.selection = {
      preselect = false, -- Do not preselect the first completion item
      auto_insert = false, -- Do not auto-insert the completion item
    }

    return opts
  end,
}
