return {
  {
    "https://codeberg.org/esensar/nvim-dev-container",
    keys = {
      {
        "<leader>dc",
        function()
          local base_path = vim.uv.cwd() .. "/.devcontainer"
          local repo_json = base_path .. "/devcontainer.json"
          local nvim_dir = base_path .. "/nvim"
          local nvim_json = nvim_dir .. "/devcontainer.json"

          -- 1. Build the target directory structure natively
          vim.fn.mkdir(nvim_dir, "p")

          -- 2. Pure OSTree native extraction pipeline to fix localEnv mounts cleanly
          local clean_cmd = string.format(
            'grep -v \'^[[:space:]]*//\' %s | jq \'(.mounts[]? | select(contains("env:HOME"))) |= (split("env:HOME}${env:USERPROFILE}") | join("localEnv:HOME}${localEnv:USERPROFILE}"))\' > %s',
            repo_json,
            nvim_json
          )
          os.execute(clean_cmd)

          -- 3. DYNAMIC WRAPPER INJECTION: Intercept podman run and guarantee static 1:1 port allocations
          local wrapper_path = vim.fn.expand("~/.cache/nvim/podman_wrapper")
          local wrapper_file = io.open(wrapper_path, "w")
          if wrapper_file then
            wrapper_file:write("#!/bin/sh\n")
            wrapper_file:write('if [ "$1" = "run" ]; then\n')
            wrapper_file:write("  shift\n")
            wrapper_file:write('  exec podman run -p 8000:8000 -p 8001:8001 -p 1337:1337 "$@"\n')
            wrapper_file:write("else\n")
            wrapper_file:write('  exec podman "$@"\n')
            wrapper_file:write("fi\n")
            wrapper_file:close()
            os.execute("chmod +x " .. wrapper_path)
          end

          -- 4. Lock the targeted directory path state before letting the plugin launch
          vim.g.devcontainer_selected_config = nvim_dir
          vim.cmd("DevcontainerStart")
        end,
        desc = "Container: Start",
      },
      { "<leader>ds", "<cmd>DevcontainerStop<cr>", desc = "Container: Stop" },
      { "<leader>dl", "<cmd>DevcontainerLogs<cr>", desc = "Container: Logs" },
      {
        "<leader>dm",
        function()
          local log_file = vim.fn.expand("~/.cache/nvim/devcontainer-mkdocs.log")

          local handle = io.popen("podman ps -lq")
          if not handle then
            vim.notify("Error: Failed to execute podman command.", vim.log.levels.ERROR)
            return
          end

          local read_output = handle:read("*a")
          handle:close()

          if not read_output then
            vim.notify("Error: Could not read podman process output.", vim.log.levels.ERROR)
            return
          end

          local container_id = read_output:gsub("%s+", "")
          if container_id == "" then
            vim.notify("Error: No active container detected to execute against.", vim.log.levels.ERROR)
            return
          end

          -- Overrides localhost by injecting 0.0.0.0 directly into the run flags
          local exec_cmd = string.format(
            'podman exec -w /workspace %s /workspace/run.sh --cmd="mkdocs" --cmd_flags="--dev-addr=0.0.0.0:8000" --insiders > %s 2>&1 &',
            container_id,
            log_file
          )
          os.execute(exec_cmd)

          vim.cmd("edit " .. log_file)
          vim.cmd("startinsert")

          -- Monitor the buffer log for immediate feedback
          local bufnr = vim.api.nvim_get_current_buf()
          vim.api.nvim_buf_attach(bufnr, false, {
            on_lines = function(_, _, _, _, _, _)
              local lines = vim.api.nvim_buf_get_lines(bufnr, 0, -1, false)
              for _, line in ipairs(lines) do
                if string.find(line, "Serving on") then
                  vim.schedule(function()
                    vim.notify(
                      "✅ Site Compiled Successfully! Browse at: http://localhost:8000/en/",
                      vim.log.levels.INFO
                    )
                  end)
                  return true
                end
              end
            end,
          })
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
        -- https://codeberg.org/esensar/nvim-dev-container/wiki/Recipes#support-for-multiple-devcontainer-configs
        -- Route the container operations strictly through our custom execution injector script
        container_runtime = vim.fn.expand("~/.cache/nvim/podman_wrapper"),
        config_search_start = function()
          return vim.g.devcontainer_selected_config
        end,
      })
    end,
  },
}
