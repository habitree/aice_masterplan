# 03-02. Pandas 기초

## 📋 목차

- [1. Pandas란?](#1-pandas란)
- [2. Series 생성 및 조작](#2-series-생성-및-조작)
- [3. DataFrame 생성](#3-dataframe-생성)
- [4. 데이터 읽기 및 쓰기](#4-데이터-읽기-및-쓰기)
- [5. 데이터 선택 및 필터링](#5-데이터-선택-및-필터링)
- [6. 데이터 탐색](#6-데이터-탐색)
- [7. 데이터 정렬 및 그룹화](#7-데이터-정렬-및-그룹화)
- [8. 실습](#8-실습)
- [9. 요약](#9-요약)

---

## 1. Pandas란?

**Pandas**는 Python에서 데이터 분석을 위한 가장 인기 있는 라이브러리입니다. 표 형태의 데이터를 효율적으로 다룰 수 있는 `DataFrame`과 `Series` 자료구조를 제공합니다.

### 1.1 Pandas의 특징

- **표 형태 데이터 처리**: 엑셀과 유사한 테이블 데이터 조작
- **데이터 읽기/쓰기**: CSV, Excel, JSON, SQL 등 다양한 형식 지원
- **데이터 정제**: 결측치 처리, 중복 제거, 데이터 변환
- **데이터 분석**: 그룹화, 집계, 통계 함수 제공
- **시계열 데이터**: 날짜/시간 데이터 처리에 특화

### 1.2 Pandas 설치 및 import

```python
# Pandas 설치 (터미널/명령 프롬프트)
# pip install pandas

# Pandas import (관례적으로 pd로 축약)
import pandas as pd

# 버전 확인
print(pd.__version__)  # 예: 2.0.3
```

> 💡 **Tip**: Pandas는 `pd`로 import하는 것이 관례입니다. NumPy와 함께 사용하는 경우가 많으므로 `import numpy as np`, `import pandas as pd`를 함께 사용합니다.

---

## 2. Series 생성 및 조작

### 2.1 Series란?

**Series**는 1차원 배열과 유사하지만 인덱스(라벨)를 가진 데이터 구조입니다.

### 2.2 Series 생성

```python
import pandas as pd

# 리스트에서 Series 생성
s1 = pd.Series([10, 20, 30, 40, 50])
print(s1)
# 0    10
# 1    20
# 2    30
# 3    40
# 4    50
# dtype: int64

# 인덱스 지정
s2 = pd.Series([10, 20, 30, 40, 50], index=['a', 'b', 'c', 'd', 'e'])
print(s2)
# a    10
# b    20
# c    30
# d    40
# e    50
# dtype: int64

# 딕셔너리에서 Series 생성
s3 = pd.Series({'이름': '홍길동', '나이': 25, '직업': '학생'})
print(s3)
# 이름    홍길동
# 나이     25
# 직업     학생
# dtype: object
```

### 2.3 Series 속성 및 메서드

```python
import pandas as pd

s = pd.Series([10, 20, 30, 40, 50], index=['a', 'b', 'c', 'd', 'e'])

# 속성
print(s.index)    # Index(['a', 'b', 'c', 'd', 'e'], dtype='object')
print(s.values)   # [10 20 30 40 50]
print(s.dtype)    # int64
print(s.size)     # 5
print(s.shape)    # (5,)

# 통계 메서드
print(s.sum())    # 150
print(s.mean())   # 30.0
print(s.std())    # 15.811388300841896
print(s.min())    # 10
print(s.max())    # 50
```

### 2.4 Series 인덱싱

```python
import pandas as pd

s = pd.Series([10, 20, 30, 40, 50], index=['a', 'b', 'c', 'd', 'e'])

# 인덱스로 접근
print(s['a'])     # 10
print(s[0])       # 10 (위치 인덱스도 가능)

# 슬라이싱
print(s['a':'c'])  # a: 10, b: 20, c: 30
print(s[0:3])      # a: 10, b: 20, c: 30

# 조건부 선택
print(s[s > 30])   # d: 40, e: 50
```

---

## 3. DataFrame 생성

### 3.1 DataFrame이란?

**DataFrame**은 2차원 표 형태의 데이터 구조로, 행과 열로 구성됩니다. 엑셀의 시트와 유사합니다.

### 3.2 DataFrame 생성

```python
import pandas as pd

# 딕셔너리에서 DataFrame 생성
data = {
    '이름': ['홍길동', '김철수', '이영희', '박민수'],
    '나이': [25, 30, 28, 35],
    '직업': ['학생', '회사원', '교사', '의사']
}
df = pd.DataFrame(data)
print(df)
#     이름  나이   직업
# 0  홍길동  25   학생
# 1  김철수  30  회사원
# 2  이영희  28   교사
# 3  박민수  35   의사

# 리스트의 리스트에서 생성
data_list = [
    ['홍길동', 25, '학생'],
    ['김철수', 30, '회사원'],
    ['이영희', 28, '교사']
]
df2 = pd.DataFrame(data_list, columns=['이름', '나이', '직업'])
print(df2)

# 빈 DataFrame 생성
df_empty = pd.DataFrame()
print(df_empty)  # Empty DataFrame
```

### 3.3 DataFrame 속성

```python
import pandas as pd

df = pd.DataFrame({
    '이름': ['홍길동', '김철수', '이영희'],
    '나이': [25, 30, 28],
    '직업': ['학생', '회사원', '교사']
})

# 기본 정보
print(df.shape)      # (3, 3) - (행, 열)
print(df.size)       # 9 - 총 원소 개수
print(df.ndim)       # 2 - 차원 수
print(df.index)      # RangeIndex(start=0, stop=3, step=1)
print(df.columns)    # Index(['이름', '나이', '직업'], dtype='object')
print(df.dtypes)     # 각 열의 데이터 타입
```

---

## 4. 데이터 읽기 및 쓰기

### 4.1 CSV 파일 읽기/쓰기

```python
import pandas as pd

# CSV 파일 읽기
df = pd.read_csv('data.csv')
print(df.head())  # 처음 5행 출력

# 옵션 지정
df = pd.read_csv('data.csv', 
                 encoding='utf-8',      # 인코딩
                 sep=',',               # 구분자
                 header=0,              # 헤더 행 번호
                 index_col=0)           # 인덱스 열

# CSV 파일 쓰기
df.to_csv('output.csv', index=False, encoding='utf-8-sig')
```

### 4.2 Excel 파일 읽기/쓰기

```python
import pandas as pd

# Excel 파일 읽기
df = pd.read_excel('data.xlsx', sheet_name='Sheet1')

# Excel 파일 쓰기
df.to_excel('output.xlsx', index=False, sheet_name='Sheet1')
```

> 💡 **Tip**: Excel 파일을 읽고 쓰려면 `openpyxl` 또는 `xlrd` 라이브러리가 필요합니다. `pip install openpyxl`로 설치할 수 있습니다.

### 4.3 기타 파일 형식

```python
import pandas as pd

# JSON 파일
df = pd.read_json('data.json')
df.to_json('output.json')

# HTML 테이블 읽기
df = pd.read_html('https://example.com/table.html')[0]

# 클립보드에서 읽기 (엑셀에서 복사한 데이터)
df = pd.read_clipboard()
```

---

## 5. 데이터 선택 및 필터링

### 5.1 열 선택

```python
import pandas as pd

df = pd.DataFrame({
    '이름': ['홍길동', '김철수', '이영희'],
    '나이': [25, 30, 28],
    '직업': ['학생', '회사원', '교사']
})

# 단일 열 선택 (Series 반환)
print(df['이름'])
# 0    홍길동
# 1    김철수
# 2    이영희
# Name: 이름, dtype: object

# 단일 열 선택 (DataFrame 반환)
print(df[['이름']])

# 여러 열 선택
print(df[['이름', '나이']])
```

### 5.2 행 선택: loc와 iloc

```python
import pandas as pd

df = pd.DataFrame({
    '이름': ['홍길동', '김철수', '이영희', '박민수'],
    '나이': [25, 30, 28, 35],
    '직업': ['학생', '회사원', '교사', '의사']
})

# loc: 라벨 기반 인덱싱
print(df.loc[0])           # 첫 번째 행
print(df.loc[0:2])         # 0~2행 (끝 포함)
print(df.loc[0, '이름'])   # 0행, '이름'열

# iloc: 위치 기반 인덱싱
print(df.iloc[0])          # 첫 번째 행
print(df.iloc[0:2])        # 0~1행 (끝 제외, Python 슬라이싱)
print(df.iloc[0, 0])       # 0행, 0열

# 조건부 선택
print(df.loc[df['나이'] > 28])  # 나이가 28보다 큰 행
```

### 5.3 조건부 필터링

```python
import pandas as pd

df = pd.DataFrame({
    '이름': ['홍길동', '김철수', '이영희', '박민수'],
    '나이': [25, 30, 28, 35],
    '직업': ['학생', '회사원', '교사', '의사']
})

# 단일 조건
print(df[df['나이'] > 28])
#     이름  나이   직업
# 1  김철수  30  회사원
# 3  박민수  35   의사

# 여러 조건 (and: &, or: |, not: ~)
print(df[(df['나이'] > 25) & (df['나이'] < 35)])
#     이름  나이   직업
# 1  김철수  30  회사원
# 2  이영희  28   교사

# 문자열 조건
print(df[df['직업'] == '학생'])
print(df[df['이름'].str.contains('길')])  # 이름에 '길' 포함
```

### 5.4 query 메서드

```python
import pandas as pd

df = pd.DataFrame({
    '이름': ['홍길동', '김철수', '이영희', '박민수'],
    '나이': [25, 30, 28, 35],
    '직업': ['학생', '회사원', '교사', '의사']
})

# query로 조건 표현
print(df.query('나이 > 28'))
print(df.query('나이 > 25 and 나이 < 35'))
```

---

## 6. 데이터 탐색

### 6.1 기본 정보 확인

```python
import pandas as pd

df = pd.DataFrame({
    '이름': ['홍길동', '김철수', '이영희', '박민수'],
    '나이': [25, 30, 28, 35],
    '직업': ['학생', '회사원', '교사', '의사']
})

# 처음/끝 n행
print(df.head(3))   # 처음 3행
print(df.tail(2))   # 마지막 2행

# 기본 정보
print(df.info())    # 데이터 타입, 결측치 정보
print(df.describe())  # 수치형 열의 통계 요약
```

### 6.2 통계 함수

```python
import pandas as pd

df = pd.DataFrame({
    '이름': ['홍길동', '김철수', '이영희', '박민수'],
    '나이': [25, 30, 28, 35],
    '키': [175, 180, 165, 178]
})

# 열별 통계
print(df['나이'].sum())    # 118
print(df['나이'].mean())   # 29.5
print(df['나이'].std())    # 표준편차
print(df['나이'].min())    # 25
print(df['나이'].max())    # 35
print(df['나이'].median()) # 29.0

# 전체 DataFrame 통계
print(df.describe())
```

### 6.3 값 개수 및 고유값

```python
import pandas as pd

df = pd.DataFrame({
    '이름': ['홍길동', '김철수', '이영희', '박민수'],
    '직업': ['학생', '회사원', '교사', '회사원']
})

# 값 개수
print(df['직업'].value_counts())
# 회사원    2
# 학생      1
# 교사      1
# Name: 직업, dtype: int64

# 고유값
print(df['직업'].unique())  # ['학생' '회사원' '교사']
print(df['직업'].nunique()) # 3 (고유값 개수)
```

---

## 7. 데이터 정렬 및 그룹화

### 7.1 정렬

```python
import pandas as pd

df = pd.DataFrame({
    '이름': ['홍길동', '김철수', '이영희', '박민수'],
    '나이': [25, 30, 28, 35],
    '키': [175, 180, 165, 178]
})

# 단일 열 기준 정렬
print(df.sort_values('나이'))          # 오름차순
print(df.sort_values('나이', ascending=False))  # 내림차순

# 여러 열 기준 정렬
print(df.sort_values(['나이', '키'], ascending=[True, False]))
```

### 7.2 그룹화 (GroupBy)

```python
import pandas as pd

df = pd.DataFrame({
    '직업': ['학생', '회사원', '교사', '회사원', '학생'],
    '나이': [25, 30, 28, 35, 22],
    '급여': [0, 3000, 2500, 4000, 0]
})

# 그룹별 집계
grouped = df.groupby('직업')
print(grouped['나이'].mean())
# 직업
# 교사     28.0
# 학생     23.5
# 회사원   32.5
# Name: 나이, dtype: float64

# 여러 집계 함수
print(grouped.agg({
    '나이': ['mean', 'min', 'max'],
    '급여': 'sum'
}))
```

### 7.3 피벗 테이블

```python
import pandas as pd

df = pd.DataFrame({
    '직업': ['학생', '회사원', '교사', '회사원'],
    '성별': ['남', '남', '여', '여'],
    '나이': [25, 30, 28, 35]
})

# 피벗 테이블 생성
pivot = df.pivot_table(values='나이', index='직업', columns='성별', aggfunc='mean')
print(pivot)
```

---

## 8. 실습

### 실습 1: 학생 성적 데이터 분석

```python
import pandas as pd

# 데이터 생성
data = {
    '이름': ['홍길동', '김철수', '이영희', '박민수', '최지영'],
    '국어': [85, 92, 78, 95, 88],
    '영어': [90, 87, 91, 88, 85],
    '수학': [88, 95, 82, 92, 90]
}
df = pd.DataFrame(data)

# 평균 점수 추가
df['평균'] = (df['국어'] + df['영어'] + df['수학']) / 3

# 평균 점수로 정렬
df = df.sort_values('평균', ascending=False)

print(df)
print(f"\n전체 평균: {df['평균'].mean():.2f}")
print(f"최고 평균: {df['평균'].max():.2f}")
print(f"최저 평균: {df['평균'].min():.2f}")
```

### 실습 2: 데이터 필터링 및 집계

```python
import pandas as pd

# 판매 데이터
data = {
    '제품': ['노트북', '마우스', '키보드', '노트북', '마우스'],
    '수량': [5, 20, 15, 3, 25],
    '가격': [1000, 30, 50, 1200, 25]
}
df = pd.DataFrame(data)

# 매출 계산
df['매출'] = df['수량'] * df['가격']

# 제품별 총 매출
product_sales = df.groupby('제품')['매출'].sum()
print("제품별 총 매출:")
print(product_sales)

# 매출이 100 이상인 제품만 필터링
high_sales = df[df['매출'] >= 100]
print("\n매출 100 이상:")
print(high_sales)
```

---

## 9. 요약

### 핵심 정리

1. **Series**: 1차원 인덱스가 있는 배열
2. **DataFrame**: 2차원 표 형태의 데이터 구조
3. **데이터 읽기/쓰기**: `read_csv()`, `to_csv()`, `read_excel()`, `to_excel()` 등
4. **데이터 선택**: `loc` (라벨), `iloc` (위치), 조건부 필터링
5. **데이터 탐색**: `head()`, `tail()`, `info()`, `describe()`, `value_counts()`
6. **그룹화**: `groupby()`로 그룹별 집계 수행

### AICE 실전 팁

- **인덱싱**: `loc`는 끝 포함, `iloc`는 끝 제외 (Python 슬라이싱)
- **조건 필터링**: 여러 조건은 `&`, `|`, `~` 사용 (괄호 필수)
- **결측치**: `isna()`, `fillna()`, `dropna()`로 처리
- **성능**: 대용량 데이터는 `chunksize` 옵션 사용
- **메모리**: 불필요한 열은 `drop()`으로 제거하여 메모리 절약

---

## ✅ 체크리스트

- [ ] Series와 DataFrame 생성 방법 이해
- [ ] 데이터 읽기/쓰기 함수 숙지
- [ ] loc, iloc를 이용한 데이터 선택 방법 숙지
- [ ] 조건부 필터링 방법 이해
- [ ] 데이터 탐색 함수 활용 가능
- [ ] 그룹화 및 집계 함수 이해
- [ ] 실습 코드 작성 및 실행 완료

---

## 📚 참고 자료

- [Pandas 공식 문서](https://pandas.pydata.org/docs/)
- [Pandas 튜토리얼](https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html)

---

**작성일**: 2025-11-19  
**이전 학습**: [03_01_Numpy기초](03_01_Numpy기초.md)  
**다음 학습**: [04_01_데이터전처리](../04_전처리/04_01_데이터전처리.md)

