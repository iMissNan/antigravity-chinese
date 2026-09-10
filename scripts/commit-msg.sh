#!/usr/bin/env bash
# commit-msg 钩子：GitHub/Gitee 提交规范校验（纯 shell 零依赖）
# 格式: <type>(<scope>): <中文描述>  |  type 白名单: feat fix docs style refactor perf test chore ci revert
# 规则: 描述 ≤50 字符、必须含中文、结尾不加句号；git revert 自动消息放行
set -u
MSG_FILE="$1"
[ -f "$MSG_FILE" ] || exit 0
FIRST_LINE=$(head -n 1 "$MSG_FILE" | sed 's/\r$//')
case "$FIRST_LINE" in
  Revert*|Merge*|Initial*) exit 0 ;;
esac
TYPES='feat|fix|docs|style|refactor|perf|test|chore|ci|revert'
if ! echo "$FIRST_LINE" | grep -Eq "^($TYPES)(\([^)]+\))?!?: .+$"; then
  echo "❌ 提交被拦截：首行格式不符合规范" >&2
  echo "   正确格式: <type>(<scope>): <中文描述>" >&2
  echo "   类型: $TYPES" >&2
  echo "   示例: feat(汉化): 添加全量设置与权限汉化" >&2
  exit 1
fi
SUBJECT=$(echo "$FIRST_LINE" | sed -E 's/^[^:]+:[[:space:]]*//')
LEN=${#SUBJECT}
if [ "$LEN" -gt 50 ]; then
  echo "❌ 提交被拦截：描述过长（${LEN} 字符 > 50）" >&2
  exit 1
fi
if ! echo "$SUBJECT" | grep -qP '[\x{4e00}-\x{9fff}]'; then
  echo "❌ 提交被拦截：描述必须包含中文（type 用英文，描述用中文）" >&2
  exit 1
fi
case "$SUBJECT" in
  *。|*．|*.) echo "❌ 提交被拦截：描述结尾不要加句号" >&2; exit 1 ;;
esac
exit 0
