--- @param run_args string[]  Port mappings e.g. {"-p", "1313:1313"}
local function inject(run_args)
  require("devcontainer_util").inject_run_args(run_args)
end

--- @param clean_fn fun()  Prepares the container config before start
--- @param run_opts table|nil  Options passed to run_on_container, or nil for pull-only
local function run(clean_fn, run_opts)
  clean_fn()
  require("devcontainer.commands").start_auto(function(_, _, id)
    if run_opts then require("devcontainer_util").run_on_container(id, run_opts) end
  end)
end

--- @param clean_fn fun()  Prepares the container config before start
local function pull(clean_fn)
  clean_fn()
  vim.cmd("DevcontainerStart")
end

local util = require("devcontainer_util")
local hugo_args = { "-p", "1313:1313" }
local mkdocs_args = { "-p", "8000:8000", "-p", "8001:8001", "-p", "1337:1337" }

return {
  {
    "https://codeberg.org/esensar/nvim-dev-container",
    keys = {
      { "<leader>dhp", function() pull(function() inject(hugo_args) end) end, desc = "Hugo: Pull" },
      { "<leader>dhr", function() run(function() util.clean_old_containers(); inject(hugo_args) end, {
          log_name = "devcontainer-hugo.log",
          workspace = "/workspaces/privacyguides.org",
          command = "/usr/local/hugo/bin/hugo server --bind 0.0.0.0",
          success_pattern = "Web Server is available",
          success_msg = "Hugo server ready! Browse at: http://localhost:1313/",
          error_pattern = "^ERROR",
      }) end, desc = "Hugo: Run" },
      { "<leader>ds", function() util.clean_old_containers() end, desc = "Container: Stop & Clean" },
      { "<leader>dl", "<cmd>DevcontainerLogs<cr>", desc = "Container: Logs" },
      { "<leader>dlc", function()
          local cache = vim.fn.expand("~/.cache/nvim")
          vim.fn.system("truncate -s 0 " .. cache .. "/devcontainer-{mkdocs,hugo}.log " .. cache .. "/devcontainer.log 2>/dev/null")
          vim.notify("Devcontainer logs cleared", vim.log.levels.INFO)
      end, desc = "Container: Clear Logs" },
      { "<leader>dlo", function()
          local cache = vim.fn.expand("~/.cache/nvim")
          local cwd = vim.uv.cwd()
          local log = "devcontainer-hugo.log"
          if vim.fn.glob(cwd .. "/mkdocs.yml") ~= "" then log = "devcontainer-mkdocs.log" end
          vim.cmd("edit " .. cache .. "/" .. log)
      end, desc = "Container: Open Log" },
      { "<leader>di", function() require("devcontainer_util").install_devcontainer_cli() end, desc = "Container: Install CLI" },
      { "<leader>dmp", function() pull(function() inject(mkdocs_args) end) end, desc = "MkDocs: Pull" },
      { "<leader>dmr", function() run(function() inject(mkdocs_args) end, {
          log_name = "devcontainer-mkdocs.log",
          command = 'bash -s -- --cmd="mkdocs" --cmd_flags="--dev-addr=0.0.0.0:8000" --insiders < ' .. vim.uv.cwd() .. '/run.sh',
          success_pattern = "Serving on",
          success_msg = "Site Compiled Successfully! Browse at: http://localhost:8000/en/",
      }) end, desc = "MkDocs: Run" },
    },
    config = function()
      require("devcontainer").setup({
        container_runtime = "devcontainer-cli",
        backup_runtime = "podman",
      })
    end,
  },
}
