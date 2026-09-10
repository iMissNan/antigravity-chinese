#!/usr/bin/env bash
# check-secrets.sh：推送前敏感信息扫描（pre-push 钩子 / 手动调用）
# 用法: check-secrets.sh [仓库目录]   默认当前目录
# 例外清单: 仓库根 .gitallowed（每行一个 glob 路径，# 开头为注释）
set -u
ROOT="${1:-$(pwd)}"
cd "$ROOT" || exit 1
ALLOWLIST=".gitallowed"
FILES=$(git ls-files -co --exclude-standard 2>/dev/null)
[ -z "$FILES" ] && exit 0
DANGER_NAME='(^|/)(\.env(\..*)?|.*\.(pem|key|p12|pfx|jks)|id_rsa|id_ed25519|credentials\.json|secrets\..*|\.npmrc|\.pypirc)$'
PATTERNS=(
  'sk-[A-Za-z0-9_-]{16,}'
  'ghp_[A-Za-z0-9]{20,}'
  'gho_[A-Za-z0-9]{20,}'
  'glpat-[A-Za-z0-9_-]{20,}'
  'github_pat_[A-Za-z0-9_]{20,}'
  'xox[baprs]-[A-Za-z0-9-]{10,}'
  'AKIA[0-9A-Z]{16}'
  '-----BEGIN [A-Z ]*PRIVATE KEY-----'
  'access_token[[:space:]]*[:=][[:space:]]*[^[:space:]]+'
  'api[_-]?key[[:space:]]*[:=][[:space:]]*[^[:space:]]+'
  'password[[:space:]]*[:=][[:space:]]*[^[:space:]]+'
  'passwd[[:space:]]*[:=][[:space:]]*[^[:space:]]+'
  'secret[[:space:]]*[:=][[:space:]]*[^[:space:]]+'
)
is_allowed() {
  local f="$1" pat
  [ -f "$ALLOWLIST" ] || return 1
  while IFS= read -r pat; do
    [ -z "$pat" ] && continue
    case "$pat" in \#*) continue ;; esac
    case "$f" in $pat) return 0 ;; esac
  done < "$ALLOWLIST"
  return 1
}
HIT=0
while IFS= read -r f; do
  [ -z "$f" ] && continue
  is_allowed "$f" && continue
  if echo "$f" | grep -Eq "$DANGER_NAME"; then
    echo "🔴 危险文件名: $f" >&2; HIT=1; continue
  fi
  if [ -f "$f" ]; then
    for p in "${PATTERNS[@]}"; do
      if grep -aEq -- "$p" "$f" 2>/dev/null; then
        echo "🔴 疑似敏感内容 ($p): $f" >&2; HIT=1; break
      fi
    done
  fi
done <<< "$FILES"
if [ "$HIT" -eq 1 ]; then
  echo "❌ 检测到敏感信息，已中止推送。确认无风险请将文件加入 .gitallowed 后重试。" >&2
  exit 1
fi
echo "✅ 敏感信息扫描通过"
exit 0
