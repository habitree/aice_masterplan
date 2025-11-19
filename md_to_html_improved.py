#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
마크다운 파일을 HTML로 변환하는 개선된 스크립트
"""
import os
import re
import sys

def parse_markdown_to_html(md_content):
    """마크다운 내용을 HTML로 변환"""
    html_parts = []
    lines = md_content.split('\n')
    i = 0
    in_code_block = False
    code_block_lang = ''
    code_block_content = []
    in_list = False
    list_type = 'ul'
    
    while i < len(lines):
        line = lines[i]
        
        # 코드 블록 처리
        if line.startswith('```'):
            if in_code_block:
                # 코드 블록 종료
                code_content = '\n'.join(code_block_content)
                html_parts.append(f'<pre><code class="language-{code_block_lang}">{escape_html(code_content)}</code></pre>')
                code_block_content = []
                in_code_block = False
                code_block_lang = ''
            else:
                # 코드 블록 시작
                in_code_block = True
                code_block_lang = line[3:].strip() or 'text'
            i += 1
            continue
        
        if in_code_block:
            code_block_content.append(line)
            i += 1
            continue
        
        # 제목 처리
        if line.startswith('# '):
            html_parts.append(f'<h1>{line[2:].strip()}</h1>')
            i += 1
            continue
        elif line.startswith('## '):
            html_parts.append(f'<h2>{line[3:].strip()}</h2>')
            i += 1
            continue
        elif line.startswith('### '):
            html_parts.append(f'<h3>{line[4:].strip()}</h3>')
            i += 1
            continue
        
        # 구분선
        if line.strip() == '---':
            html_parts.append('<hr>')
            i += 1
            continue
        
        # 리스트 처리
        if line.strip().startswith('- '):
            if not in_list:
                html_parts.append('<ul>')
                in_list = True
            content = line.strip()[2:]
            html_parts.append(f'<li>{parse_inline_markdown(content)}</li>')
            i += 1
            continue
        elif line.strip().startswith(('1. ', '2. ', '3. ', '4. ', '5. ', '6. ', '7. ', '8. ', '9. ')):
            if not in_list or list_type != 'ol':
                if in_list:
                    html_parts.append(f'</{list_type}>')
                html_parts.append('<ol>')
                in_list = True
                list_type = 'ol'
            content = re.sub(r'^\d+\.\s+', '', line.strip())
            html_parts.append(f'<li>{parse_inline_markdown(content)}</li>')
            i += 1
            continue
        else:
            if in_list:
                html_parts.append(f'</{list_type}>')
                in_list = False
                list_type = 'ul'
        
        # 인용구 처리
        if line.strip().startswith('> '):
            content = line.strip()[2:]
            # Tip, Warning 등 특수 처리
            if '💡' in content or 'Tip' in content:
                html_parts.append(f'<div class="tip"><strong>{parse_inline_markdown(content)}</strong></div>')
            elif '⚠️' in content or 'Warning' in content:
                html_parts.append(f'<div class="warning"><strong>{parse_inline_markdown(content)}</strong></div>')
            else:
                html_parts.append(f'<blockquote>{parse_inline_markdown(content)}</blockquote>')
            i += 1
            continue
        
        # 빈 줄
        if not line.strip():
            html_parts.append('<p></p>')
            i += 1
            continue
        
        # 일반 문단
        if line.strip():
            html_parts.append(f'<p>{parse_inline_markdown(line)}</p>')
        
        i += 1
    
    # 리스트가 끝나지 않은 경우
    if in_list:
        html_parts.append(f'</{list_type}>')
    
    return '\n'.join(html_parts)

def parse_inline_markdown(text):
    """인라인 마크다운 처리"""
    # 강조
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    
    # 인라인 코드
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    
    # 링크
    text = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2">\1</a>', text)
    
    return text

def escape_html(text):
    """HTML 특수문자 이스케이프"""
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    text = text.replace('"', '&quot;')
    text = text.replace("'", '&#39;')
    return text

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
    
    # 마크다운을 HTML로 변환
    body_content = parse_markdown_to_html(md_content)
    
    # 섹션 박스로 감싸기
    body_html = f'<div class="section-box">\n{body_content}\n</div>'
    
    # 템플릿에 내용 삽입
    html_output = html_template.replace("제목을 여기에 입력", title)
    
    # 기존 컨테이너 내용 찾아서 교체
    pattern = r'<div class="container">\s*<h1>[^<]+</h1>\s*<div class="section-box">.*?</div>\s*<div class="summary">.*?</div>\s*<div class="checklist">.*?</div>'
    replacement = f'<div class="container">\n    <h1>{title}</h1>\n    {body_html}\n    <div class="footer">\n      <p>AICE Associate 시험 대비 | 학습 자료</p>\n    </div>'
    
    html_output = re.sub(pattern, replacement, html_output, flags=re.DOTALL)
    
    # HTML 파일 저장
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html_output)
    
    print(f"변환 완료: {os.path.basename(md_file)} -> {os.path.basename(html_file)}")

if __name__ == "__main__":
    # 02_파이썬기초 폴더의 모든 MD 파일 변환
    base_dir = os.path.dirname(__file__)
    python_dir = os.path.join(base_dir, "02_파이썬기초")
    
    if os.path.exists(python_dir):
        md_files = [f for f in os.listdir(python_dir) if f.endswith(".md")]
        for filename in sorted(md_files):
            md_path = os.path.join(python_dir, filename)
            html_path = os.path.join(python_dir, filename.replace(".md", ".html"))
            try:
                markdown_to_html(md_path, html_path)
            except Exception as e:
                print(f"오류 발생 ({filename}): {e}")
                import traceback
                traceback.print_exc()

