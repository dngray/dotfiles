--- @brief [[
--- Devcontainer keymaps for Hugo / MkDocs sites.
--- Services are defined as data tables — the same functions handle all of them.
---
--- Keymaps:
---   <leader>dhp    Hugo: Pull
---   <leader>dhr    Hugo: Run
---   <leader>dmp    MkDocs: Pull
---   <leader>dmr    Main + Articles + Caddy (unified preview at localhost:1337)
---   <leader>dar    Articles only
---   <leader>dcr    Caddy only
---   <leader>ds     Container: Stop & Clean
---   <leader>dl     Container: Logs (plugin)
---   <leader>dlc    Container: Clear Logs
---   <leader>dlo    Container: Open Log (picker)
---   <leader>di     Container: Install CLI
--- @brief ]]

local util = require("devcontainer_util")

local mkdocs_ports = { "-p", "8000:8000", "-p", "8001:8001", "-p", "1337:1337" }

--- @class Service
--- @field run_args? string[]    Port mappings to inject (nil = reuse previous)
--- @field log_name string       Log file name (~/.cache/nvim/<log_name>)
--- @field workspace? string     Container working dir (nil = auto-detect)
--- @field command string        Command to exec inside container
--- @field success_pattern? string  Regex to watch for (nil = no notification)
--- @field success_msg? string   Notification on success
--- @field error_pattern? string Regex for error detection

--- @type table<string, Service>
local services = {
  hugo = {
    run_args = { "-p", "1313:1313" },
    log_name = "devcontainer-hugo.log",
    workspace = "/workspaces/privacyguides.org",
    command = "/usr/local/hugo/bin/hugo server --bind 0.0.0.0",
    success_pattern = "Web Server is available",
    success_msg = "Hugo server ready! Browse at: http://localhost:1313/",
    error_pattern = "^ERROR",
  },
  main = {
    run_args = mkdocs_ports,
    log_name = "devcontainer-main.log",
    command = ('bash -s -- --cmd="mkdocs" --cmd_flags="--dev-addr=0.0.0.0:8000" --insiders < %s/run.sh'):format(vim.uv.cwd()),
    success_pattern = "Serving on",
    success_msg = "Main site ready! Browse at: http://localhost:8000/en/",
  },
  articles = {
    log_name = "devcontainer-articles.log",
    command = "mkdocs serve --config-file=mkdocs.blog.yml --dev-addr=0.0.0.0:8001",
    success_pattern = "Serving on",
    success_msg = "Articles ready! Browse at: http://localhost:8001/",
  },
  caddy = {
    log_name = "devcontainer-caddy.log",
    command = "caddy run --config .devcontainer/Caddyfile",
    success_msg = "Caddy reverse proxy ready! Browse at: http://localhost:1337/",
  },
}

--- Starts the container and runs one or more services inside it.
--- Cleans old containers and injects port mappings before starting.
--- @param svc_names string[]       Service names to run (e.g. {"main", "articles"})
--- @param inject_args? string[]    Port mappings to inject (nil = pull from services)
local function start(svc_names, inject_args)
  inject_args = inject_args or (function()
    for _, name in ipairs(svc_names) do
      local s = services[name]
      if s and s.run_args then return s.run_args end
    end
  end)()

  util.clean_old_containers()
  if inject_args then util.inject_run_args(inject_args) end

  require("devcontainer.commands").start_auto(function(_, _, id)
    local selected = vim.tbl_map(function(n) return services[n] end, svc_names)
    if #selected == 1 then
      util.run_on_container(id, selected[1])
    elseif #selected > 1 then
      util.run_multi(id, selected)
    end
  end)
end

--- Pull-only: clean + inject + start without running commands.
--- @param inject_args? string[]
local function pull(inject_args)
  util.clean_old_containers()
  if inject_args then util.inject_run_args(inject_args) end
  vim.cmd("DevcontainerStart")
end

--- Opens a vim.ui.select to pick which log to view.
local function open_log()
  local cache = vim.fn.expand("~/.cache/nvim")
  local logs = {}
  for name, _ in pairs(services) do
    table.insert(logs, { name = name, file = cache .. "/" .. services[name].log_name })
  end
  table.sort(logs, function(a, b) return a.name < b.name end)

  vim.ui.select(logs, {
    prompt = "Select devcontainer log:",
    format_item = function(item) return item.name end,
  }, function(choice)
    if choice then vim.cmd("edit " .. choice.file) end
  end)
end

local log_glob = "~/.cache/nvim/devcontainer-{main,articles,caddy,hugo}.log ~/.cache/nvim/devcontainer.log"

return {
  {
    "https://codeberg.org/esensar/nvim-dev-container",
    keys = {
      { "<leader>dhp", function() pull(services.hugo.run_args) end, desc = "Hugo: Pull" },
      { "<leader>dhr", function() start({ "hugo" }, services.hugo.run_args) end, desc = "Hugo: Run" },
      { "<leader>dmp", function() pull(mkdocs_ports) end, desc = "MkDocs: Pull" },
      { "<leader>dmr", function() start({ "main", "articles", "caddy" }) end, desc = "MkDocs: Run (Main + Articles + Caddy)" },
      { "<leader>dar", function() start({ "articles" }, mkdocs_ports) end, desc = "Articles: Run" },
      { "<leader>dcr", function() start({ "caddy" }, mkdocs_ports) end, desc = "Caddy: Run" },
      { "<leader>ds", util.clean_old_containers, desc = "Container: Stop & Clean" },
      { "<leader>dl", "<cmd>DevcontainerLogs<cr>", desc = "Container: Logs" },
      { "<leader>dlc", function()
          vim.fn.system("truncate -s 0 " .. log_glob .. " 2>/dev/null")
          vim.notify("Devcontainer logs cleared", vim.log.levels.INFO)
      end, desc = "Container: Clear Logs" },
      { "<leader>dlo", open_log, desc = "Container: Open Log" },
      { "<leader>di", util.install_devcontainer_cli, desc = "Container: Install CLI" },
    },
    config = function()
      require("devcontainer").setup({
        container_runtime = "devcontainer-cli",
        backup_runtime = "podman",
      })
    end,
  },
}
