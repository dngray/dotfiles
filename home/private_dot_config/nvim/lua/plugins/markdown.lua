return {
  -- Enable markdown diagnostics
  {
    "none-ls.nvim",
    opts = function(_, opts)
      local nls = require("null-ls")
      vim.list_extend(opts.sources, {
        nls.builtins.diagnostics.markdownlint_cli2.with({
          --args = { "**/*.md" },
          args = { "$FILENAME" },
        }),
      })
    end,
  },
}
