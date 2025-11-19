"""
HTML 파일을 이미지로 변환하는 스크립트
"""
import os
import sys
from pathlib import Path

# Windows에서 UTF-8 인코딩 설정
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("playwright가 설치되어 있지 않습니다. 설치 중...")
    os.system("pip install playwright")
    os.system("playwright install chromium")
    from playwright.sync_api import sync_playwright

def html_to_image(html_file, output_file=None, width=1200, height=None):
    """
    HTML 파일을 이미지로 변환
    
    Args:
        html_file: 입력 HTML 파일 경로
        output_file: 출력 이미지 파일 경로 (기본값: html_file과 같은 이름의 png)
        width: 이미지 너비 (기본값: 1200px)
        height: 이미지 높이 (기본값: None, 자동 조정)
    """
    html_path = Path(html_file).resolve()
    
    if not html_path.exists():
        print(f"오류: 파일을 찾을 수 없습니다: {html_file}")
        sys.exit(1)
    
    if output_file is None:
        output_file = html_path.with_suffix('.png')
    else:
        output_file = Path(output_file)
    
    print(f"HTML 파일 로딩: {html_path}")
    print(f"이미지 저장 경로: {output_file}")
    
    with sync_playwright() as p:
        # Chromium 브라우저 실행
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # HTML 파일 로드
        page.goto(f"file://{html_path}")
        
        # 페이지가 완전히 로드될 때까지 대기
        page.wait_for_load_state("networkidle")
        
        # 추가 대기 (CSS 및 폰트 로딩)
        page.wait_for_timeout(1000)
        
        # 뷰포트 설정 (고해상도를 위해 2배 크기로 설정)
        if width:
            # 고해상도를 위해 viewport를 2배로 설정
            page.set_viewport_size({"width": width * 2, "height": (height or 800) * 2})
        
        # 컨테이너 요소 찾기
        container = page.locator('.container')
        
        if container.count() > 0:
            # 컨테이너 요소만 스크린샷 (여백 제거, 고해상도)
            container.screenshot(
                path=str(output_file),
                type="png"
            )
        else:
            # 컨테이너가 없으면 전체 페이지 스크린샷
            page.screenshot(
                path=str(output_file),
                full_page=True,
                type="png"
            )
        
        browser.close()
    
    print(f"이미지 생성 완료: {output_file}")
    return True

if __name__ == "__main__":
    # Jupiter 브라우저 변경.html 파일만 변환 (고해상도)
    html_file = "Jupiter 브라우저 변경.html"
    
    if len(sys.argv) > 1:
        html_file = sys.argv[1]
    
    try:
        html_to_image(html_file, None, width=1200)
    except Exception as e:
        print(f"오류 발생: {e}")
        import traceback
        traceback.print_exc()

