#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
마크다운 파일을 HTML로 변환하는 스크립트
"""
import os
import re
import sys

def markdown_to_html(md_file, html_file):
    """마크다운 파일을 HTML로 변환"""
    
    # HTML 템플릿 읽기
    template_path = os.path.join(os.path.dirname(__file__), "templates", "html_style_template.html")
    with open(template_path, "r", encoding="utf-8") as f:
        html_template = f.read()
    
    # 마크다운 파일 읽기
    with open(md_file, "r", encoding="utf-8") as f:
        md_content = f.read()
    
    # 제목 추출
    title_match = re.search(r'^#\s+(.+)$', md_content, re.MULTILINE)
    title = title_match.group(1) if title_match else "제목 없음"
    
    # HTML 변환 (간단한 변환)
    html_content = md_content
    
    # 제목 변환
    html_content = re.sub(r'^#\s+(.+)$', r'<h1>\1</h1>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^##\s+(.+)$', r'<h2>\1</h2>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^###\s+(.+)$', r'<h3>\1</h3>', html_content, flags=re.MULTILINE)
    
    # 코드 블록 변환
    html_content = re.sub(
        r'```(\w+)?\n(.*?)```',
        r'<pre><code>\2</code></pre>',
        html_content,
        flags=re.DOTALL
    )
    
    # 인라인 코드
    html_content = re.sub(r'`([^`]+)`', r'<code>\1</code>', html_content)
    
    # 강조
    html_content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html_content)
    html_content = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html_content)
    
    # 리스트
    html_content = re.sub(r'^-\s+(.+)$', r'<li>\1</li>', html_content, flags=re.MULTILINE)
    
    # 링크
    html_content = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2">\1</a>', html_content)
    
    # 구분선
    html_content = re.sub(r'^---$', r'<hr>', html_content, flags=re.MULTILINE)
    
    # 템플릿에 내용 삽입
    html_output = html_template.replace("제목을 여기에 입력", title)
    html_output = html_output.replace(
        '<div class="container">\n    <h1>제목을 여기에 입력</h1>',
        f'<div class="container">\n    <h1>{title}</h1>\n    <div class="section-box">\n{html_content}\n    </div>'
    )
    
    # HTML 파일 저장
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html_output)
    
    print(f"변환 완료: {md_file} -> {html_file}")

if __name__ == "__main__":
    # 02_파이썬기초 폴더의 모든 MD 파일 변환
    base_dir = os.path.dirname(__file__)
    python_dir = os.path.join(base_dir, "02_파이썬기초")
    
    if os.path.exists(python_dir):
        for filename in os.listdir(python_dir):
            if filename.endswith(".md"):
                md_path = os.path.join(python_dir, filename)
                html_path = os.path.join(python_dir, filename.replace(".md", ".html"))
                markdown_to_html(md_path, html_path)

