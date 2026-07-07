import requests
import re
import os
import datetime
import sys

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
}

WAGE_HISTORY = {
    2023: {
        "상반기": { "construction": 157068, "manufacturing": 84618 },
        "하반기": { "construction": 161858, "manufacturing": 86008 }
    },
    2024: {
        "상반기": { "construction": 165545, "manufacturing": 86008 },
        "하반기": { "construction": 167081, "manufacturing": 90085 }
    },
    2025: {
        "상반기": { "construction": 169804, "manufacturing": 90085 },
        "하반기": { "construction": 171037, "manufacturing": 90830 }
    },
    2026: {
        "상반기": { "construction": 172068, "manufacturing": 90694 },
        "하반기": { "construction": 172068, "manufacturing": 95767 }
    }
}

def get_expected_wage(category, survey_year, survey_half):
    if category == "construction":
        y_data = WAGE_HISTORY.get(survey_year)
        if y_data and survey_half in y_data:
            return y_data[survey_half]["construction"]
    else:  # manufacturing
        if survey_half == "하반기":
            target_y = survey_year + 1
            y_data = WAGE_HISTORY.get(target_y)
            if y_data and "상반기" in y_data:
                return y_data["상반기"]["manufacturing"]
        else:  # 상반기
            y_data = WAGE_HISTORY.get(survey_year)
            if y_data and "하반기" in y_data:
                return y_data["하반기"]["manufacturing"]
    return None

def get_latest_known_wage(category):
    max_year = max(WAGE_HISTORY.keys())
    if category == "construction":
        val = WAGE_HISTORY[max_year]["하반기"]["construction"]
        if val > 0: return val
        return WAGE_HISTORY[max_year]["상반기"]["construction"]
    else:
        val = WAGE_HISTORY[max_year]["하반기"]["manufacturing"]
        if val > 0: return val
        return WAGE_HISTORY[max_year]["상반기"]["manufacturing"]

def extract_via_formula(queries, period, year):
    if period == "상반기":
        exp_c = get_expected_wage("construction", year, "상반기")
        exp_m = get_expected_wage("manufacturing", year - 1, "하반기")
    elif period == "중반기":
        exp_c = get_expected_wage("construction", year, "상반기")
        exp_m = get_expected_wage("manufacturing", year, "상반기")
    else:
        exp_c = get_expected_wage("construction", year, "하반기")
        exp_m = get_expected_wage("manufacturing", year, "상반기")
        
    latest_c = get_latest_known_wage("construction")
    latest_m = get_latest_known_wage("manufacturing")
    
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
                if (150000 <= c_val <= 250000) and (80000 <= m_val <= 140000):
                    candidates.append((c_val, m_val))
            
            if candidates:
                best_pair = max(set(candidates), key=candidates.count)
                
                # Check if it matches expected hardcoded pair
                if exp_c and exp_m and best_pair[0] == exp_c and best_pair[1] == exp_m:
                    print(f"Success extracting expected formula from query '{query}': Construction = {best_pair[0]}, Manufacturing = {best_pair[1]}")
                    return best_pair[0], best_pair[1]
                
                # For future years/new wages: check if strictly greater than latest known
                is_new_and_valid = False
                if period == "상반기":
                    is_new_and_valid = (best_pair[0] > latest_c) and (best_pair[1] > latest_m)
                elif period == "중반기":
                    is_new_and_valid = (best_pair[0] >= latest_c) and (best_pair[1] > latest_m)
                else:
                    is_new_and_valid = (best_pair[0] > latest_c) and (best_pair[1] >= latest_m)
                    
                if is_new_and_valid:
                    print(f"Success extracting new formula from query '{query}': Construction = {best_pair[0]}, Manufacturing = {best_pair[1]}")
                    return best_pair[0], best_pair[1]
        except Exception as e:
            print(f"Exception during formula extraction for query '{query}': {e}")
            
    return None

def extract_individual(query, context_patterns, val_min, val_max, category, survey_year, survey_half):
    expected = get_expected_wage(category, survey_year, survey_half)
    latest_known = get_latest_known_wage(category)
    
    url = f"https://search.naver.com/search.naver?query={requests.utils.quote(query)}"
    try:
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code != 200:
            return expected if expected else latest_known
        
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
            # 1. If we have a hardcoded expected wage, and it is in the candidates, prefer it!
            if expected and expected in candidates:
                print(f"Extracted expected hardcoded wage for '{query}': {expected} won")
                return expected
                
            # 2. Filter candidates for future years/new wages: must be greater than latest known
            valid_candidates = [c for c in candidates if c > latest_known]
            if valid_candidates:
                best_val = max(set(valid_candidates), key=lambda x: (valid_candidates.count(x), x))
                print(f"Extracted new individual wage for '{query}': {best_val} won (Latest known: {latest_known} won)")
                return best_val
            
            # 3. If no new candidates are found, fall back to expected or latest known
            fallback = expected if expected else latest_known
            print(f"No new wage candidates found for '{query}' (Latest known: {latest_known} won). Falling back to {fallback} won.")
            return fallback
    except Exception as e:
        print(f"Exception during individual extraction for query '{query}': {e}")
        
    return expected if expected else latest_known

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
    
    # 2. Determine target period based on the 3 periods
    # - 상반기 (Jan 1 - June 30)
    # - 중반기 (July 1 - Aug 31)
    # - 하반기 (Sept 1 - Dec 31)
    if month < 7:
        period = "상반기"
    elif month < 9:
        period = "중반기"
    else:
        period = "하반기"
        
    # Determine the target survey names for querying based on the official publishing rules
    # Construction (대한건설협회):
    # - 상반기 (Jan 1) / 중반기 (July 1): Y년 상반기 시중노임단가 보통인부
    # - 하반기 (Sept 1): Y년 하반기 시중노임단가 보통인부
    # Manufacturing (중소기업중앙회):
    # - 상반기 (Jan 1): (Y-1)년 하반기 단순노무종사원 노임단가
    # - 중반기 (July 1) / 하반기 (Sept 1): Y년 상반기 단순노무종사원 노임단가
    if period == "상반기":
        c_query_year = year
        c_query_half = "상반기"
        m_query_year = year - 1
        m_query_half = "하반기"
    elif period == "중반기":
        c_query_year = year
        c_query_half = "상반기"
        m_query_year = year
        m_query_half = "상반기"
    else:  # 하반기
        c_query_year = year
        c_query_half = "하반기"
        m_query_year = year
        m_query_half = "상반기"
        
    print(f"Target Period for Wage Update: {year}년 {period}")
    print(f" - Target Construction Survey: {c_query_year}년 {c_query_half}")
    print(f" - Target Manufacturing Survey: {m_query_year}년 {m_query_half}")
    
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
            f"{year}년 상반기 중소제조업 생산직 조사노임 자동차보험 임금"
        ]
    else:  # 하반기
        queries = [
            f"{year}년 하반기 자동차보험 일용근로자 임금",
            f"{year}년 하반기 도시일용노임",
            f"{year}년 하반기 보통인부 단순노무종사원",
            f"{year}년 9월 자동차보험 일용근로자 임금"
        ]
        
    wages = extract_via_formula(queries, period, year)
    
    if wages:
        construction_wage, manufacturing_wage = wages
    else:
        print("Formula extraction failed or was stale. Trying individual context-aware extraction...")
        
        c_query = f"{c_query_year}년 {c_query_half} 보통인부 노임단가"
        c_patterns = [
            r'보통인부[^\d]{0,30}?(\d{3}[,\.]\d{3})',
            r'보통인부[^\d]{0,30}?(\d{6})'
        ]
        
        m_query = f"{m_query_year}년 {m_query_half} 단순노무종사원 노임단가"
        m_patterns = [
            r'단순노무[^\d]{0,30}?(\d{2,3}[,\.]\d{3})',
            r'단순노무[^\d]{0,30}?(\d{5,6})'
        ]
        
        construction_wage = extract_individual(c_query, c_patterns, 150000, 250000, "construction", c_query_year, c_query_half)
        manufacturing_wage = extract_individual(m_query, m_patterns, 80000, 140000, "manufacturing", m_query_year, m_query_half)
        
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
