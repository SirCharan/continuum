# Continuum config — copy to ~/.config/continuum/config.sh (or export in your shell).
# All optional; sensible defaults shown.
export CLAUDE_MEMORY_DIR="$HOME/.claude/memory"      # where your notes live (symlinked into Obsidian)
export CLAUDE_VAULT_LINK=""                           # e.g. "$HOME/Documents/Obsidian Vault/Memory" — enables doctor's symlink check
export CLAUDE_PROJECT_MAP='{}'                        # JSON {cwd-basename: project}; empty ⇒ project = cwd basename
export CLAUDE_SECTION_TITLES='{}'                     # JSON {folder: "Nice Title"}; empty ⇒ auto title-case
export CLAUDE_KNOWN_DANGLERS=""                       # comma-sep note names that are intentionally unresolved links
export UPKEEP_LABEL="com.continuum.upkeep"            # launchd/cron label for the weekly job
