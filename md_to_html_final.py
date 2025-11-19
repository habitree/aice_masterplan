#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
마크다운 파일을 HTML로 완전히 변환하는 최종 스크립트
"""
import os
import re
import sys
import io

# Windows에서 UTF-8 출력 설정
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def escape_html(text):
    """HTML 특수문자 이스케이프"""
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    return text

def parse_inline_markdown(text):
    """인라인 마크다운 처리"""
    # 강조 (순서 중요: ** 먼저, * 나중에)
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'(?<!\*)\*(?!\*)([^*]+?)(?<!\*)\*(?!\*)', r'<em>\1</em>', text)
    
    # 인라인 코드
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    
    # 링크
    text = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2">\1</a>', text)
    
    return text

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
    in_table = False
    table_rows = []
    in_summary = False
    in_checklist = False
    
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        
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
        
        # 리스트 종료 처리
        if in_list and not (stripped.startswith('- ') or re.match(r'^\d+\.\s+', stripped) or not stripped):
            html_parts.append(f'</{list_type}>')
            in_list = False
            list_type = 'ul'
        
        # 제목 처리 (목차 섹션 제외)
        if stripped.startswith('# '):
            if i > 0:  # 첫 번째 제목이 아니면
                html_parts.append(f'<h1>{parse_inline_markdown(stripped[2:])}</h1>')
            i += 1
            continue
        elif stripped.startswith('## '):
            # 요약 섹션 체크
            if '요약' in stripped or '정리' in stripped:
                if in_summary:
                    html_parts.append('</div>')
                html_parts.append('<div class="summary">')
                in_summary = True
            # 체크리스트 섹션 체크
            elif '체크리스트' in stripped or '✅' in stripped:
                if in_checklist:
                    html_parts.append('</div>')
                html_parts.append('<div class="checklist">')
                in_checklist = True
            
            html_parts.append(f'<h2>{parse_inline_markdown(stripped[3:])}</h2>')
            i += 1
            continue
        elif stripped.startswith('### '):
            html_parts.append(f'<h3>{parse_inline_markdown(stripped[4:])}</h3>')
            i += 1
            continue
        
        # 구분선 (체크리스트나 요약 섹션 안에서는 닫기)
        if stripped == '---':
            if in_checklist:
                html_parts.append('</div>')
                in_checklist = False
            if in_summary:
                html_parts.append('</div>')
                in_summary = False
            html_parts.append('<hr>')
            i += 1
            continue
        
        # 체크리스트 항목
        if stripped.startswith('- [ ]') or stripped.startswith('- [x]') or stripped.startswith('- [X]'):
            if not in_checklist:
                html_parts.append('<div class="checklist">')
                in_checklist = True
            checked = 'checked' if stripped[3:5] in ['[x', '[X'] else ''
            content = stripped[5:].strip()
            html_parts.append(f'<div class="checklist-item"><input type="checkbox" {checked}><label>{parse_inline_markdown(content)}</label></div>')
            i += 1
            continue
        
        # 리스트 처리
        if stripped.startswith('- '):
            if not in_list:
                html_parts.append('<ul>')
                in_list = True
                list_type = 'ul'
            content = stripped[2:]
            html_parts.append(f'<li>{parse_inline_markdown(content)}</li>')
            i += 1
            continue
        elif re.match(r'^\d+\.\s+', stripped):
            if not in_list or list_type != 'ol':
                if in_list:
                    html_parts.append(f'</{list_type}>')
                html_parts.append('<ol>')
                in_list = True
                list_type = 'ol'
            content = re.sub(r'^\d+\.\s+', '', stripped)
            html_parts.append(f'<li>{parse_inline_markdown(content)}</li>')
            i += 1
            continue
        
        # 코드 블록이 리스트 안에 있는지 확인 (다음 줄이 코드 블록이면 리스트 종료)
        if in_list and i < len(lines) - 1:
            next_line = lines[i + 1].strip()
            if next_line.startswith('```'):
                html_parts.append(f'</{list_type}>')
                in_list = False
                list_type = 'ul'
        
        # 인용구 처리
        if stripped.startswith('> '):
            content = stripped[2:]
            # Tip, Warning 등 특수 처리
            if '💡' in content or 'Tip' in content:
                # 중첩 strong 태그 방지
                clean_content = re.sub(r'\*\*(.+?)\*\*', r'\1', content)
                html_parts.append(f'<div class="tip"><strong>{parse_inline_markdown(clean_content)}</strong></div>')
            elif '⚠️' in content or 'Warning' in content:
                clean_content = re.sub(r'\*\*(.+?)\*\*', r'\1', content)
                html_parts.append(f'<div class="warning"><strong>{parse_inline_markdown(clean_content)}</strong></div>')
            else:
                html_parts.append(f'<blockquote>{parse_inline_markdown(content)}</blockquote>')
            i += 1
            continue
        
        # 빈 줄
        if not stripped:
            i += 1
            continue
        
        # 일반 문단
        if stripped:
            parsed = parse_inline_markdown(line)
            html_parts.append(f'<p>{parsed}</p>')
        
        i += 1
    
    # 리스트가 끝나지 않은 경우
    if in_list:
        html_parts.append(f'</{list_type}>')
    
    # 섹션이 끝나지 않은 경우
    if in_summary:
        html_parts.append('</div>')
    if in_checklist:
        html_parts.append('</div>')
    
    return '\n    '.join(html_parts)

def markdown_to_html(md_file, html_file):
    """마크다운 파일을 HTML로 변환"""
    
    # HTML 템플릿 읽기
    template_path = os.path.join(os.path.dirname(__file__), "templates", "html_style_template.html")
    with open(template_path, "r", encoding="utf-8") as f:
        html_template = f.read()
    
    # 마크다운 파일 읽기
    with open(md_file, "r", encoding="utf-8") as f:
        md_content = f.read()
    
    # 제목 추출 (첫 번째 # 제목)
    title_match = re.search(r'^#\s+(.+)$', md_content, re.MULTILINE)
    title = title_match.group(1) if title_match else "제목 없음"
    
    # 마크다운을 HTML로 변환
    body_content = parse_markdown_to_html(md_content)
    
    # 템플릿에 내용 삽입
    html_output = html_template.replace("제목을 여기에 입력", title)
    
    # 기존 컨테이너 내용 교체
    pattern = r'<div class="container">\s*<h1>[^<]+</h1>.*?<div class="footer">'
    replacement = f'<div class="container">\n    <h1>{title}</h1>\n    \n    <div class="section-box">\n    {body_content}\n    </div>\n    \n    <div class="footer">'
    
    html_output = re.sub(pattern, replacement, html_output, flags=re.DOTALL)
    
    # HTML 파일 저장
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html_output)
    
    print(f"[OK] 변환 완료: {os.path.basename(md_file)} -> {os.path.basename(html_file)}")

if __name__ == "__main__":
    # 02_파이썬기초 폴더의 모든 MD 파일 변환
    base_dir = os.path.dirname(__file__)
    python_dir = os.path.join(base_dir, "02_파이썬기초")
    
    if os.path.exists(python_dir):
        md_files = [f for f in os.listdir(python_dir) if f.endswith(".md")]
        print(f"\n총 {len(md_files)}개 파일 변환 시작...\n")
        for filename in sorted(md_files):
            md_path = os.path.join(python_dir, filename)
            html_path = os.path.join(python_dir, filename.replace(".md", ".html"))
            try:
                markdown_to_html(md_path, html_path)
            except Exception as e:
                print(f"[ERROR] 오류 발생 ({filename}): {e}")
                import traceback
                traceback.print_exc()
        print(f"\n모든 변환 완료!\n")

