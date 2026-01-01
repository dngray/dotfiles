return {
  {
    "https://codeberg.org/esensar/nvim-dev-container",
    keys = {
      { "<leader>dc", "<cmd>DevcontainerStart<cr>", desc = "Container: Start" },
      { "<leader>ds", "<cmd>DevcontainerStop<cr>", desc = "Container: Stop" },
      { "<leader>dl", "<cmd>DevcontainerLogs<cr>", desc = "Container: Logs" },
      {
        "<leader>dr",
        function()
          vim.g.devcontainer_selected_config = nil
          vim.notify("Devcontainer selection reset")
        end,
        desc = "Container: Reset Selection",
      },
    },
    config = function()
      require("devcontainer").setup({
        -- https://codeberg.org/esensar/nvim-dev-container/wiki/Recipes#support-for-multiple-devcontainer-configs
        config_search_start = function()
          if vim.g.devcontainer_selected_config == nil or vim.g.devcontainer_selected_config == "" then
            local candidates =
              vim.split(vim.fn.glob(vim.uv.cwd() .. "/.devcontainer/**/devcontainer.json"), "\n", { trimempty = true })
            if #candidates < 2 then
              vim.g.devcontainer_selected_config = vim.uv.cwd()
            else
              local choices = { "Select devcontainer config file to use:" }
              for idx, candidate in ipairs(candidates) do
                table.insert(choices, idx .. ". - " .. candidate)
              end
              local choice_idx = vim.fn.inputlist(choices)
              if choice_idx <= 0 or choice_idx > #candidates then
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
