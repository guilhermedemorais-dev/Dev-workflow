#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 3 ]]; then
  echo "Usage: $0 <project-root> <prompt-file> <status-file>" >&2
  exit 64
fi

project_root=$1
prompt_file=$2
status_file=$3

if [[ ! -d "$project_root" ]]; then
  echo "Project root does not exist: $project_root" >&2
  exit 66
fi

if [[ ! -f "$prompt_file" ]]; then
  echo "Prompt file does not exist: $prompt_file" >&2
  exit 66
fi

if ! command -v gnome-terminal >/dev/null 2>&1; then
  echo "gnome-terminal is not available" >&2
  exit 69
fi

if ! command -v claude >/dev/null 2>&1; then
  echo "claude is not available" >&2
  exit 69
fi

rm -f "$status_file"

runner=$(mktemp /tmp/claude-visible-runner.XXXXXX)
cat >"$runner" <<'RUNNER'
#!/usr/bin/env bash
set -uo pipefail

project_root=$1
prompt_file=$2
status_file=$3
runner_file=$4
prompt=$(cat "$prompt_file")

cd "$project_root" || exit 66

printf '\nO LLM executor recebeu o checkpoint do agente orquestrador.\n'
printf 'Acompanhe o trabalho nesta janela. Ao terminar, use /exit.\n\n'

claude "$prompt" \
  --permission-mode acceptEdits \
  --tools "Read,Edit,Write,Glob,Grep"
exit_code=$?

printf '%s\n' "$exit_code" >"$status_file"
rm -f "$runner_file"

printf '\nO LLM executor encerrou com codigo %s. O agente orquestrador pode revisar o diff.\n' "$exit_code"
printf 'Pressione Enter para fechar esta janela.\n'
read -r
RUNNER
chmod 700 "$runner"

gnome-terminal \
  --working-directory="$project_root" \
  --title="LLM executor - checkpoint delegado" \
  -- "$runner" "$project_root" "$prompt_file" "$status_file" "$runner"

echo "Executor LLM opened in a visible terminal."
echo "Status file: $status_file"
