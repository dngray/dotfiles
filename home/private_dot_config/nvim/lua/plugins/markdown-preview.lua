return {

  {
    "selimacerbas/markdown-preview.nvim",
    dependencies = { "selimacerbas/live-server.nvim" }, -- Built-in pure Lua HTTP server
    ft = { "markdown", "mdx" }, -- Only loads when editing markdown files
    keys = {
      -- Binds your preferred layout shortcut keys natively
      { "<leader>mp", "<cmd>MarkdownPreview<cr>", desc = "Open Live Markdown Preview" },
      { "<leader>ms", "<cmd>MarkdownPreviewStop<cr>", desc = "Stop Preview Server" },
    },
    config = function()
      -- Optional configuration hooks go here
      -- The plugin handles server-sent rendering automatically without external tools
    end,
  },
}
