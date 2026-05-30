local M = {}

function M.clean_config()
  local base_path = vim.uv.cwd() .. "/.devcontainer"
  local repo_json = base_path .. "/devcontainer.json"
  local nvim_dir = base_path .. "/nvim"
  local nvim_json = nvim_dir .. "/devcontainer.json"

  vim.fn.mkdir(nvim_dir, "p")

  local clean_cmd = string.format(
    'grep -v \'^[[:space:]]*//\' %s | jq \'(.mounts[]? | select(contains("env:HOME"))) |= (split("env:HOME}${env:USERPROFILE}") | join("localEnv:HOME}${localEnv:USERPROFILE}"))\' > %s',
    repo_json,
    nvim_json
  )
  os.execute(clean_cmd)
  vim.g.devcontainer_selected_config = nvim_dir
end

function M.create_wrapper()
  local wrapper_path = vim.fn.expand("~/.cache/nvim/podman_wrapper")
  local f = io.open(wrapper_path, "w")
  if f then
    f:write("#!/bin/sh\n")
    f:write('if [ "$1" = "run" ]; then\n')
    f:write("  shift\n")
    f:write('  exec podman run -p 8000:8000 -p 8001:8001 -p 1337:1337 "$@"\n')
    f:write("else\n")
    f:write('  exec podman "$@"\n')
    f:write("fi\n")
    f:close()
    os.execute("chmod +x " .. wrapper_path)
  end
  return wrapper_path
end

function M.run_mkdocs()
  local log_file = vim.fn.expand("~/.cache/nvim/devcontainer-mkdocs.log")

  local handle = io.popen("podman ps -lq")
  if not handle then
    vim.notify("Failed to execute podman command.", vim.log.levels.ERROR)
    return
  end

  local container_id = handle:read("*a"):gsub("%s+", "")
  handle:close()

  if container_id == "" then
    vim.notify("No active container detected.", vim.log.levels.ERROR)
    return
  end

  local exec_cmd = string.format(
    'podman exec -w /workspace %s /workspace/run.sh --cmd="mkdocs" --cmd_flags="--dev-addr=0.0.0.0:8000" --insiders > %s 2>&1 &',
    container_id,
    log_file
  )
  os.execute(exec_cmd)

  vim.cmd("edit " .. log_file)
  vim.cmd("startinsert")

  local bufnr = vim.api.nvim_get_current_buf()
  vim.api.nvim_buf_attach(bufnr, false, {
    on_lines = function()
      local lines = vim.api.nvim_buf_get_lines(bufnr, 0, -1, false)
      for _, line in ipairs(lines) do
        if string.find(line, "Serving on") then
          vim.schedule(function()
            vim.notify(
              "Site Compiled Successfully! Browse at: http://localhost:8000/en/",
              vim.log.levels.INFO
            )
          end)
          return true
        end
      end
    end,
  })
end

return M
