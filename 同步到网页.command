#!/bin/bash
# 双击此文件即可将案例库同步到网页

cd "$(dirname "$0")"

# Git 用户信息（commit 必须，否则会静默失败）
git config user.name  "hwangsiran-lab"
git config user.email "hwangsiran@gmail.com"

echo "📦 正在检查改动..."
git add .

CHANGED=$(git diff --cached --name-only)
if [ -z "$CHANGED" ]; then
  echo "✅ 没有新改动，无需同步。"
  echo ""
  read -p "按回车键关闭..."
  exit 0
fi

echo "📝 以下文件将被更新："
echo "$CHANGED"
echo ""

git commit -m "update $(date '+%Y-%m-%d %H:%M')"
if [ $? -ne 0 ]; then
  echo "❌ 提交失败，请截图此窗口联系开发者。"
  echo ""
  read -p "按回车键关闭..."
  exit 1
fi

echo ""
echo "⬆️  正在推送到 GitHub..."
git push
if [ $? -ne 0 ]; then
  echo "❌ 推送失败，请检查网络或 Token 是否过期。"
  echo ""
  read -p "按回车键关闭..."
  exit 1
fi

echo ""
echo "✅ 同步完成！约1分钟后刷新页面即可看到最新内容。"
echo "🌐 网址：https://hwangsiran-lab.github.io/case-library/cases-library.html"
echo ""
read -p "按回车键关闭..."
