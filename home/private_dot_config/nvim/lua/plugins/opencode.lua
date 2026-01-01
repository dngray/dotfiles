return {
  "nickjvandyke/opencode.nvim",
  lazy = false,
  keys = {

    -- 🤖 Ask (The 'submit = true' makes it actually SEND the code + question)
    {
      "<leader>aa",
      function()
        require("opencode").ask("@this: ", { submit = true })
      end,
      desc = "OpenCode: Ask",
      mode = { "n", "x" },
    },

    -- 🛠️ Action Picker (Replaces the 'fix' and 'explain' guesswork)
    {
      "<leader>af",
      function()
        require("opencode").select()
      end,
      desc = "OpenCode: Actions",
      mode = { "n", "x" },
    },

    -- 📋 Toggle/Sessions (Clean way to peek at the jail)
    {
      "<leader>as",
      function()
        require("opencode").toggle()
      end,
      desc = "OpenCode: Toggle View",
      mode = { "n", "t" },
    },

    -- 🎯 Operators (The 'go' style bindings for quick range selection)
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

    -- 📜 Scrolling the Jailed TUI from Neovim
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
  init = function()
    -- Ensure ~/.local/bin is in Neovim's path for the shim
    local local_bin = vim.fn.expand("$HOME/.local/bin")
    if not string.find(vim.env.PATH, local_bin) then
      vim.env.PATH = local_bin .. ":" .. vim.env.PATH
    end

    local fortress_path = os.getenv("FORTRESS_PATH") or ""
    local rel_path = fortress_path:gsub("^.-/src/", "")
    local password = os.getenv("OPENCODE_SERVER_PASSWORD") or ""

    vim.g.opencode_opts = {
      -- Experimental LSP must be explicitly enabled in some versions
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
    }
  end,
}
