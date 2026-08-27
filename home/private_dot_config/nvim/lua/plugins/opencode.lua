return {
  "nickjvandyke/opencode.nvim",
  init = function()
    -- Ensure ~/.local/bin is in Neovim's path for the shim binary execution
    local local_bin = vim.fn.expand("$HOME/.local/bin")
    if not string.find(vim.env.PATH, local_bin) then
      vim.env.PATH = local_bin .. ":" .. vim.env.PATH
    end
  end,
  -- All container settings are properly returned here to hook into the plugin setup block
  opts = function()
    local fortress_path = os.getenv("FORTRESS_PATH") or ""
    local rel_path = fortress_path:gsub("^.-/src/", "")
    local password = os.getenv("OPENCODE_SERVER_PASSWORD") or ""

    return {
      lsp = {
        enabled = true,
      },
      server = {
        hostname = "127.0.0.1",
        port = 4096,
        password = password,
      },
      path_config = {
        root_map = {
          [fortress_path] = "/home/opencode/workspace/" .. rel_path,
        },
      },
      -- 🛠️ CUSTOM PICKER ACTIONS: Injects explicit macros into require("opencode").select()
      select = {
        prompts = {
          ["Refactor (Clean Code)"] = "Analyze this code structure. Optimize for performance, remove redundant code loops, and verify variable scopes match strict functional paradigms.",
          ["Generate Unit Tests"] = "Write thorough, comprehensive unit test blocks covering all happy paths, boundary edge cases, and error handling states for this module.",
          ["Security Audit"] = "Review this block for security regressions. Look out for buffer drops, system execution leaks, unvalidated user strings, or loose process permissions.",
          ["Explain Architecture"] = "Break down the architectural patterns utilized here. Map out the flow of data inputs, function dependencies, and state boundaries step-by-step.",
        },
      },
    }
  end,
  keys = {
    -- 🤖 Ask (Fixed: Converted back to a strict string format to satisfy string? signature matching)
    {
      "<leader>aa",
      function()
        require("opencode").ask("@this ")
      end,
      desc = "OpenCode: Ask",
      mode = { "n", "x" },
    },

    -- 🛠️ Action Picker (Quick access to fix/explain/refactor)
    {
      "<leader>af",
      function()
        require("opencode").select()
      end,
      desc = "OpenCode: Actions",
      mode = { "n", "x" },
    },

    -- 📋 Toggle View (Quickly check the active session in the jail)
    {
      "<leader>as",
      function()
        require("opencode").toggle()
      end,
      desc = "OpenCode: Toggle View",
      mode = { "n", "t" },
    },

    -- 🎯 Operators (The brilliant 'go' style text-objects for ranges)
    {
      "go",
      function()
        return require("opencode").operator("@this ")
      end,
      desc = "Add range to opencode",
      expr = true,
      mode = { "n", "x" },
    },
    {
      "goo",
      function()
        return require("opencode").operator("@this ") .. "_"
      end,
      desc = "Add line to opencode",
      expr = true,
      mode = "n",
    },

    -- 📜 Scroll the active OpenCode TUI pane directly from your Neovim buffer
    {
      "<S-C-u>",
      function()
        require("opencode").command("session.half.page.up")
      end,
      desc = "Scroll AI Up",
    },
    {
      "<S-C-d>",
      function()
        require("opencode").command("session.half.page.down")
      end,
      desc = "Scroll AI Down",
    },
  },
}
