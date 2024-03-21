return {
  {
    "https://codeberg.org/esensar/nvim-dev-container",
    config = function()
      require("devcontainer").setup({})
    end,
  },
}
