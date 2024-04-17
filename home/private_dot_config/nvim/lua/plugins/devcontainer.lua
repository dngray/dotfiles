return {
  {
    "https://codeberg.org/esensar/nvim-dev-container",
    config = function()
      require("devcontainer").setup({
        -- https://codeberg.org/esensar/nvim-dev-container/wiki/Recipes#support-for-multiple-devcontainer-configs
        config_search_start = function()
          if vim.g.devcontainer_selected_config == nil or vim.g.devcontainer_selected_config == "" then
            local candidates = vim.split(
              vim.fn.glob(vim.loop.cwd() .. "/.devcontainer/**/devcontainer.json"),
              "\n",
              { trimempty = true }
            )
            if #candidates < 2 then
              vim.g.devcontainer_selected_config = vim.loop.cwd()
            else
              local choices = { "Select devcontainer config file to use:" }
              for idx, candidate in ipairs(candidates) do
                table.insert(choices, idx .. ". - " .. candidate)
              end
              local choice_idx = vim.fn.inputlist(choices)
              if choice_idx > #candidates then
                choice_idx = 1
              end
              vim.g.devcontainer_selected_config = string.gsub(candidates[choice_idx], "/devcontainer.json", "")
            end
          end
          return vim.g.devcontainer_selected_config
        end,
      })
    end,
  },
}
