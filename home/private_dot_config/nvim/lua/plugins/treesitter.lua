return {
  "nvim-treesitter/nvim-treesitter",
  opts = function(_, opts)
    local parser_dir = vim.fn.expand("$HOME/.local/share/nvim/site")
    vim.fn.mkdir(parser_dir .. "/parser", "p")

    opts.parser_install_dir = parser_dir .. "/parser"
    vim.opt.runtimepath:append(parser_dir)

    opts.auto_install = false
    opts.indent = { enable = true }
    opts.highlight = { enable = true }

    -- 1. By default, ensure_installed is empty so standard host boots download NOTHING.
    -- 2. It will only populate when we explicitly run the container script with this variable.
    if os.getenv("COMPILE_PARSERS") == "1" then
      opts.ensure_installed = {
        "bash",
        "c",
        "diff",
        "gotmpl",
        "html",
        "javascript",
        "jsdoc",
        "json",
        "jsonc",
        "lua",
        "luadoc",
        "luap",
        "markdown",
        "markdown_inline",
        "printf",
        "python",
        "query",
        "regex",
        "toml",
        "tsx",
        "typescript",
        "vim",
        "vimdoc",
        "xml",
        "yaml",
      }
    else
      opts.ensure_installed = {}
    end
  end,
}
