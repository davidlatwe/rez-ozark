# Usage: . serve.ps1
rez env git `
    python `
    mkdocs_material-4.4.0 `
    mkdocs_git_revision_date_plugin==0.1.5 -- `
    mkdocs gh-deploy
