--- @brief [[
--- Devcontainer helper utilities for Hugo, MkDocs, and multi-site projects.
---
--- inject_run_args(run_args)   - adds port mappings to devcontainer.json
--- clean_old_containers()      - stops/removes containers for current project
--- resolve_workspace(id)       - inspects container for mount path
--- run_on_container(id, opts)  - exec + log + watch for success
--- run_multi(container_id, services) - runs multiple commands, opens logs in tabs
--- watch_log(bufnr, opts)      - buffer-attached pattern watcher
--- install_devcontainer_cli()  - standalone CLI installer
--- @brief ]]

local M = {}

--- Injects runArgs into devcontainer.json, strips JSONC comments, switches to
--- devcontainer-cli runtime. Call before DevcontainerStart or start_auto.
--- @param run_args string[] e.g. {"-p", "1313:1313"}
function M.inject_run_args(run_args)
  local repo_json = vim.uv.cwd() .. "/.devcontainer/devcontainer.json"

  local handle = io.popen("grep -v '^[[:space:]]*//' " .. repo_json)
  local json_str = handle:read("*a")
  handle:close()

  local ok, config = pcall(vim.json.decode, json_str)
  if not ok or type(config) ~= "table" then
    vim.notify("Failed to parse devcontainer.json", vim.log.levels.ERROR)
    return
  end

  config.runArgs = run_args

  local out = io.open(repo_json, "w")
  if out then
    out:write(vim.json.encode(config))
    out:close()
  end

  require("devcontainer.config").container_runtime = "devcontainer-cli"
  require("devcontainer.config").backup_runtime = "podman"
end

--- Stops all running and removes all exited devcontainer-cli containers for
--- the current project, matched by the devcontainer.local_folder label.
--- @brief Run before starting a new container to avoid port conflicts.
function M.clean_old_containers()
  local cwd = vim.uv.cwd()
  vim.fn.system(string.format(
    "podman ps -q --filter status=running --filter label=devcontainer.local_folder=%s | xargs -r podman stop 2>/dev/null",
    cwd
  ))
  vim.fn.system(string.format(
    "podman ps -a -q --filter status=exited --filter label=devcontainer.local_folder=%s | xargs -r podman rm 2>/dev/null",
    cwd
  ))
end

--- Resolves the workspace mount point inside a container by matching the host
--- source to vim.uv.cwd(). Falls back to "/workspace".
--- @param container_id string
--- @return string
function M.resolve_workspace(container_id)
  local cwd = vim.uv.cwd()
  local inspect = io.popen(string.format(
    "podman inspect %s --format '{{range .Mounts}}{{.Source}}|{{.Destination}}\n{{end}}'",
    container_id
  ))
  local workspace = "/workspace"
  if inspect then
    local output = inspect:read("*a")
    inspect:close()
    for line in output:gmatch("[^\n]+") do
      local src, dst = line:match("^(.-)|(.+)$")
      if src and dst and src == cwd then
        workspace = dst
        break
      end
    end
  end
  return workspace
end

--- Runs a command inside the container, opens the log, and watches for success.
--- @param container_id string
--- @param opts {log_name: string, command: string, workspace?: string, success_pattern: string, success_msg: string, error_pattern?: string}
function M.run_on_container(container_id, opts)
  local log_file = vim.fn.expand("~/.cache/nvim/" .. opts.log_name)
  local workspace = opts.workspace or M.resolve_workspace(container_id)

  vim.fn.system(string.format(
    "podman exec -i -w %s %s %s > %s 2>&1 &",
    vim.fn.shellescape(workspace),
    container_id,
    opts.command,
    log_file
  ))

  vim.cmd("edit " .. log_file)
  M.watch_log(vim.api.nvim_get_current_buf(), {
    success_pattern = opts.success_pattern,
    success_msg = opts.success_msg,
    error_pattern = opts.error_pattern,
  })
end

--- Runs multiple commands in the same container. Opens logs as buffers in the
--- current window (no splits) and attaches watchers to each.
--- @param container_id string
--- @param services table[]  list of opts tables as accepted by run_on_container
--- @return nil
function M.run_multi(container_id, services)
  for i, svc in ipairs(services) do
    local log_file = vim.fn.expand("~/.cache/nvim/" .. svc.log_name)
    local workspace = svc.workspace or M.resolve_workspace(container_id)

    vim.fn.system(string.format(
      "podman exec -i -w %s %s %s > %s 2>&1 &",
      vim.fn.shellescape(workspace),
      container_id,
      svc.command,
      log_file
    ))

    vim.cmd("edit " .. log_file)
    M.watch_log(vim.api.nvim_get_current_buf(), {
      success_pattern = svc.success_pattern,
      success_msg = svc.success_msg,
      error_pattern = svc.error_pattern,
    })
  end
end

--- Watch a log buffer for success/error patterns with notifications.
--- @param bufnr number buffer to watch
--- @param opts {success_pattern: string, success_msg: string, error_pattern?: string}
function M.watch_log(bufnr, opts)
  vim.api.nvim_buf_attach(bufnr, false, {
    on_lines = function()
      local lines = vim.api.nvim_buf_get_lines(bufnr, 0, -1, false)
      local last = lines[#lines]
      if not last then return end
      if opts.success_pattern and string.find(last, opts.success_pattern) then
        vim.schedule(function()
          vim.notify(opts.success_msg, vim.log.levels.INFO)
        end)
        return true
      end
      if opts.error_pattern and string.find(last, opts.error_pattern) then
        vim.schedule(function()
          vim.notify(last, vim.log.levels.WARN)
        end)
      end
    end,
  })
end

--- Installs the devcontainer CLI standalone binary via the official install
--- script (bundles its own Node.js, no npm required). Prompts for confirmation,
--- runs in a terminal split, and notifies on completion.
--- @brief Idempotent — skips if already installed.
--- @usage <leader>di
function M.install_devcontainer_cli()
  local handle = io.popen("which devcontainer 2>/dev/null")
  if not handle then
    vim.notify("Failed to check for devcontainer CLI.", vim.log.levels.ERROR)
    return
  end
  local result = handle:read("*a"):gsub("%s+", "")
  handle:close()

  if result ~= "" then
    local version_handle = io.popen("devcontainer --version 2>/dev/null")
    local version = ""
    if version_handle then
      version = version_handle:read("*a"):gsub("%s+", "")
      version_handle:close()
    end
    vim.notify(
      "devcontainer CLI already installed at " .. result .. " (version " .. version .. ")",
      vim.log.levels.INFO
    )
    return
  end

  vim.ui.select({ "Yes", "No" }, {
    prompt = "Install devcontainer CLI via standalone script? (no npm/Node.js needed)",
  }, function(choice)
    if choice ~= "Yes" then
      return
    end

    local data_home = vim.fn.expand(vim.env.XDG_DATA_HOME or "$HOME/.local/share")
    local prefix = data_home .. "/devcontainers"
    local bin_dir = prefix .. "/bin"
    local install_url = "https://raw.githubusercontent.com/devcontainers/cli/main/scripts/install.sh"
    local install_cmd = string.format(
      "curl -fsSL %s | sh -s -- --prefix %s && echo; echo '=== INSTALL COMPLETE ==='",
      install_url, prefix
    )

    vim.cmd("botright 10new")
    local bufnr = vim.api.nvim_get_current_buf()
    vim.api.nvim_open_term(bufnr, {})
    vim.fn.jobstart({ "bash", "-c", install_cmd }, {
      pty = true,
      on_exit = function(_, code)
        vim.cmd("bdelete!")
        if code == 0 then
          vim.fn.setenv("PATH", bin_dir .. ":" .. vim.env.PATH)
          local verify = io.popen("devcontainer --version 2>/dev/null")
          local version = ""
          if verify then
            version = verify:read("*a"):gsub("%s+", "")
            verify:close()
          end
          if version ~= "" then
            vim.notify(
              "devcontainer CLI v" .. version
                .. " installed! Add to your shell config:\n  export PATH=\"" .. bin_dir .. ":$PATH\"",
              vim.log.levels.INFO
            )
          end
        else
          vim.notify(
            "Installation failed (exit code " .. code .. "). Try manually:\n"
              .. "  curl -fsSL " .. install_url .. " | sh -s -- --prefix " .. prefix,
            vim.log.levels.ERROR
          )
        end
      end,
    })
  end)
end

return M
