return {
  {
    "selimacerbas/mdkite.nvim",
    dependencies = { "selimacerbas/kitehost.nvim" },
    ft = { "markdown", "mdx" },
    keys = {
      { "<leader>mp", "<cmd>MdKite start<cr>", desc = "Open Live Markdown Preview" },
      { "<leader>ms", "<cmd>MdKite stop<cr>", desc = "Stop Preview Server" },
    },
    -- Automatically runs setup() with your clean, default settings
    opts = {},
  },
}
