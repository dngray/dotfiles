return {
  {
    "https://codeberg.org/esensar/nvim-dev-container",
    keys = {
      {
        "<leader>dc",
        function()
          local util = require("devcontainer_util")
          util.clean_config()
          util.create_wrapper()
          vim.cmd("DevcontainerStart")
        end,
        desc = "Container: Start",
      },
      { "<leader>ds", "<cmd>DevcontainerStop<cr>", desc = "Container: Stop" },
      { "<leader>dl", "<cmd>DevcontainerLogs<cr>", desc = "Container: Logs" },
      {
        "<leader>dm",
        function()
          require("devcontainer_util").run_mkdocs()
        end,
        desc = "Container: Run Main MkDocs (Follow Logs)",
      },
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
        container_runtime = vim.fn.expand("~/.cache/nvim/podman_wrapper"),
        config_search_start = function()
          return vim.g.devcontainer_selected_config
        end,
      })
    end,
  },
}
