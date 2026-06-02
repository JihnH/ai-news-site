#!/bin/bash
# 部署脚本 - 推送AI新闻网站到GitHub Pages

REPO_NAME="ai-news-site"
GITHUB_USER=""  # 需要填写
TOKEN="$GITHUB_TOKEN"

if [ -z "$GITHUB_USER" ]; then
    echo "错误: 请设置GitHub用户名"
    exit 1
fi

REMOTE_URL="https://${TOKEN}@github.com/${GITHUB_USER}/${REPO_NAME}.git"

cd /root/.openclaw/workspace/ai-news-site

# 检查远程仓库是否存在
git remote | grep origin > /dev/null
if [ $? -ne 0 ]; then
    git remote add origin "$REMOTE_URL"
fi

# 推送
git push -u origin master

echo "✅ 已推送到 GitHub"
echo "🌐 访问地址: https://${GITHUB_USER}.github.io/${REPO_NAME}"
