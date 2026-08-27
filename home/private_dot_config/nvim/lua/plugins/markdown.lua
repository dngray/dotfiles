return {
  -- 1. Strip out markdownlint-cli2 from nvim-lint
  {
    "mfussenegger/nvim-lint",
    optional = true,
    opts = {
      linters_by_ft = {
        markdown = {},
        ["markdown.mdx"] = {},
      },
    },
  },

  -- 2. Let conform.nvim run both markdown-toc and the rumdl formatter via CLI
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
        -- Define rumdl explicitly as a CLI formatter with an inline disable override
        ["rumdl-cli"] = {
          command = "rumdl",
          -- 'fmt' runs the formatter, '--disable MD013' forces line length checking to turn off
          args = { "fmt", "--disable", "MD013", "$FILENAME" },
          stdin = false,
        },
      },
      formatters_by_ft = {
        -- Sequence: First regenerates your TOC, then applies rumdl fixes safely on save
        ["markdown"] = { "markdown-toc", "rumdl-cli" },
        ["markdown.mdx"] = { "markdown-toc", "rumdl-cli" },
      },
    },
  },
}
