return {
  "nvim-orgmode/orgmode",
  event = "VeryLazy",
  config = function()
    -- Setup orgmode
    require("orgmode").setup({
      org_agenda_files = "~/Notes/org**/**",
      org_default_notes_file = "~/Notes/org/refile.org",
    })
  end,
}
