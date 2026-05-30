return {
  -- 1. Configure rumdl inside nvim-lint
  {
    "mfussenegger/nvim-lint",
    opts = {
      linters_by_ft = {
        markdown = { "rumdl" },
        ["markdown.mdx"] = { "rumdl" },
      },
    },
    init = function()
      local lint = require("lint")
      if lint.linters.rumdl then
        lint.linters.rumdl.args = {
          "check",
          "--config",
          vim.fn.expand("~/.config/rumdl/rumdl.toml"),
          "--stdin-filename",
          function()
            return vim.api.nvim_buf_get_name(0)
          end,
          "--output",
          "json",
          "-",
        }
      end
    end,
  },

  -- 2. Let conform.nvim handle formatting on save safely
  {
    "stevearc/conform.nvim",
    opts = {
      formatters = {
        ["markdown-toc"] = {
          condition = function(_, ctx)
            for _, line in ipairs(vim.api.nvim_buf_get_lines(ctx.buf, 0, -1, false)) do
              if line:find("<!%-%- toc %-%->") then
                return true
              end
            end
          end,
        },
        ["rumdl-cli"] = {
          command = "rumdl",
          args = function(_, ctx)
            local args = { "fmt", "--silent", "--stdin-filename", "$FILENAME", "-" }

            if ctx.filename:find("src/dngray/pg", 1, true) or ctx.filename:find("/pg/") then
              table.insert(args, 1, vim.fn.expand("~/.config/rumdl/rumdl.toml"))
              table.insert(args, 1, "--config")
            end
            return args
          end,
          stdin = true,
        },
      },
      formatters_by_ft = {
        ["markdown"] = { "markdown-toc", "rumdl-cli" },
        ["markdown.mdx"] = { "markdown-toc", "rumdl-cli" },
      },
    },
  },
}
