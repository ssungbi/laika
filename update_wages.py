import requests
import re
import os
import datetime
import sys

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
}

def extract_via_formula(queries):
    formula_pattern = r'(\d{3}[,\.]\d{3})\s*원?\s*\+\s*(\d{2,3}[,\.]\d{3})\s*원?\s*\)?\s*[\/÷]\s*2'
    
    for query in queries:
        url = f"https://search.naver.com/search.naver?query={requests.utils.quote(query)}"
        try:
            r = requests.get(url, headers=headers, timeout=10)
            if r.status_code != 200:
                continue
            
            text = re.sub(r'<[^>]+>', ' ', r.text)
            text = re.sub(r'\s+', ' ', text)
            
            matches = re.finditer(formula_pattern, text)
            candidates = []
            for m in matches:
                c_val = int(re.sub(r'\D', '', m.group(1)))
                m_val = int(re.sub(r'\D', '', m.group(2)))
                # Range validation
                if (150000 <= c_val <= 250000) and (80000 <= m_val <= 140000):
                    candidates.append((c_val, m_val))
            
            if candidates:
                # Return the most frequent pair (mode)
                best_pair = max(set(candidates), key=candidates.count)
                print(f"Success extracting via formula from query '{query}': Construction = {best_pair[0]} won, Manufacturing = {best_pair[1]} won")
                return best_pair[0], best_pair[1]
        except Exception as e:
            print(f"Exception during formula extraction for query '{query}': {e}")
            
    return None

def extract_individual(query, context_patterns, val_min, val_max):
    url = f"https://search.naver.com/search.naver?query={requests.utils.quote(query)}"
    try:
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code != 200:
            return None
        
        text = re.sub(r'<[^>]+>', ' ', r.text)
        text = re.sub(r'\s+', ' ', text)
        
        candidates = []
        for pattern in context_patterns:
            matches = re.finditer(pattern, text)
            for m in matches:
                val = int(re.sub(r'\D', '', m.group(1)))
                if val_min <= val <= val_max:
                    candidates.append(val)
                    
        if candidates:
            best_val = max(set(candidates), key=candidates.count)
            print(f"Extracted individual wage for '{query}': {best_val} won")
            return best_val
    except Exception as e:
        print(f"Exception during individual extraction for query '{query}': {e}")
        
    return None

def main():
    # 1. Parse date from argument if provided (for simulation/testing)
    now = datetime.datetime.now()
    if len(sys.argv) > 1:
        try:
            arg_date = sys.argv[1]
            now = datetime.datetime.strptime(arg_date, "%Y-%m-%d")
            print(f"Using simulated server date: {now.strftime('%Y-%m-%d')}")
        except Exception as e:
            print(f"Failed to parse argument '{sys.argv[1]}' as YYYY-MM-DD. Using current system date instead.")
            
    year = now.year
    month = now.month
    
    # 2. Determine target period and construction/manufacturing halves based on the 3 periods
    # - 상반기 (Jan 1 - June 30): Construction 상반기, Manufacturing 상반기
    # - 중반기 (July 1 - Aug 31): Construction 상반기, Manufacturing 하반기
    # - 하반기 (Sept 1 - Dec 31): Construction 하반기, Manufacturing 하반기
    if month < 7:
        period = "상반기"
        c_half = "상반기"
        m_half = "상반기"
    elif month < 9:
        period = "중반기"
        c_half = "상반기"
        m_half = "하반기"
    else:
        period = "하반기"
        c_half = "하반기"
        m_half = "하반기"
        
    print(f"Target Period for Wage Update: {year}년 {period} (Construction: {c_half}, Manufacturing: {m_half})")
    
    # 3. Create queries for formula extraction based on the period
    if period == "상반기":
        queries = [
            f"{year}년 상반기 자동차보험 일용근로자 임금",
            f"{year}년 상반기 도시일용노임",
            f"{year}년 상반기 보통인부 단순노무종사원"
        ]
    elif period == "중반기":
        queries = [
            f"{year}년 7월 자동차보험 일용근로자 임금",
            f"{year}년 7월 도시일용노임",
            f"{year}년 7월 일용근로자 임금",
            f"{year}년 하반기 제조노임 적용 자동차보험 임금"
        ]
    else: # 하반기
        queries = [
            f"{year}년 하반기 자동차보험 일용근로자 임금",
            f"{year}년 하반기 도시일용노임",
            f"{year}년 하반기 보통인부 단순노무종사원",
            f"{year}년 9월 자동차보험 일용근로자 임금"
        ]
        
    wages = extract_via_formula(queries)
    
    if wages:
        construction_wage, manufacturing_wage = wages
    else:
        print("Formula extraction failed. Trying individual context-aware extraction...")
        
        c_query = f"{year}년 {c_half} 보통인부 노임단가"
        c_patterns = [
            r'보통인부[^\d]{0,30}?(\d{3}[,\.]\d{3})',
            r'보통인부[^\d]{0,30}?(\d{6})'
        ]
        
        m_query = f"{year}년 {m_half} 단순노무종사원 노임단가"
        m_patterns = [
            r'단순노무[^\d]{0,30}?(\d{2,3}[,\.]\d{3})',
            r'단순노무[^\d]{0,30}?(\d{5,6})'
        ]
        
        construction_wage = extract_individual(c_query, c_patterns, 150000, 250000)
        manufacturing_wage = extract_individual(m_query, m_patterns, 80000, 140000)
        
    if not construction_wage or not manufacturing_wage:
        print("CRITICAL: Failed to extract wage standards automatically. Keeping previous wage_data.js.")
        return
        
    daily_average = int(round((construction_wage + manufacturing_wage) / 2))
    monthly_common = daily_average * 25
    monthly_court = construction_wage * 20
    
    print(f"\nFinal Extracted Standards:")
    print(f" - Construction Ordinary Wage: {construction_wage:,} won")
    print(f" - Manufacturing Simple Labor Wage: {manufacturing_wage:,} won")
    print(f" - Daily Average (Insurance standard): {daily_average:,} won")
    print(f" - Monthly Common (Daily Average * 25 days): {monthly_common:,} won")
    print(f" - Monthly Court (Construction Wage * 20 days): {monthly_court:,} won")
    
    # Update wage_data.js
    script_dir = os.path.dirname(os.path.abspath(__file__))
    target_path = os.path.join(script_dir, "wage_data.js")
    
    js_content = f"""// 이 파일은 GitHub Actions에 의해 자동으로 업데이트됩니다.
// 마지막 업데이트: {now.strftime('%Y-%m-%d %H:%M:%S')}
window.WAGE_DATA = {{
    lastUpdated: "{now.strftime('%Y-%m-%d')}",
    year: {year},
    period: "{period}",
    constructionDaily: {construction_wage},
    manufacturingDaily: {manufacturing_wage},
    dailyAverage: {daily_average},
    monthlyCommon: {monthly_common},
    monthlyCourt: {monthly_court}
}};
"""
    
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(js_content)
        
    print(f"\nSuccessfully wrote updated wage data to {target_path}")

if __name__ == "__main__":
    main()
