import streamlit as st
import numpy as np
import time

# ============================================================================
# 文本分析函數（在頁面配置之前定義）
# ============================================================================

def count_repeated_phrases(text):
    """計算重複的三詞短語"""
    words = text.lower().split()
    if len(words) < 3:
        return 0
    
    phrases = {}
    for i in range(len(words) - 2):
        phrase = ' '.join(words[i:i+3])
        phrases[phrase] = phrases.get(phrase, 0) + 1
    
    return sum(1 for count in phrases.values() if count > 2)


def detect_formal_language(text):
    """檢測正式措辭"""
    formal_words = [
        'furthermore', 'moreover', 'consequently', 'therefore',
        'nevertheless', 'however', 'regarding', 'facilitate',
        'implement', 'subsequent', 'adjacent', '因此', '然而', '儘管'
    ]
    
    text_lower = text.lower()
    count = sum(1 for word in formal_words if word in text_lower)
    return min(1.0, count / 3)


def check_grammar_perfection(text):
    """檢查語法完美度"""
    errors = 0
    
    if '  ' in text:
        errors += text.count('  ')
    
    sentences = text.split('。')
    cap_errors = sum(1 for s in sentences if s.strip() and not s.strip()[0].isupper())
    errors += cap_errors
    
    return max(0, 1 - (errors / max(1, len(text.split()) / 10)))


def check_formulaic_patterns(text):
    """檢查模式化表述"""
    patterns = [
        'in today\'s world',
        'it is important to',
        'in conclusion',
        'furthermore',
        '在當今世界',
        '重要的是',
        '總之',
        '此外'
    ]
    
    text_lower = text.lower()
    count = sum(1 for p in patterns if p in text_lower)
    return count >= 2


def analyze_structure(text):
    """分析句子結構規律性"""
    sentences = [s.strip() for s in text.split('。') if s.strip()]
    if len(sentences) < 2:
        return 0
    
    lengths = [len(s.split()) for s in sentences]
    variance = np.var(lengths) if len(lengths) > 1 else 0
    mean_len = np.mean(lengths) if lengths else 1
    
    cv = variance / (mean_len + 1)
    return 1 - min(1.0, cv / 3)


def count_contractions(text):
    """計算縮寫數量"""
    contractions = [
        "can't", "don't", "won't", "isn't", "hasn't",
        "haven't", "shouldn't", "couldn't", "wouldn't",
        "that's", "it's", "i'm", "you're", "i've"
    ]
    
    text_lower = text.lower()
    return sum(text_lower.count(c) for c in contractions)


def detect_natural_errors(text):
    """檢測打字錯誤"""
    errors = 0
    
    double_words = ['the the', 'and and', 'a a', '的的', '和和']
    for word in double_words:
        errors += text.lower().count(word)
    
    return errors / max(1, len(text.split()) / 10)


def detect_emotional_language(text):
    """檢測情感詞彙"""
    emotional = [
        'love', 'hate', 'beautiful', 'terrible', 'wonderful',
        'awful', 'amazing', 'fantastic', 'horrible', 'feel',
        '喜歡', '討厭', '美', '可怕', '棒', '糟糕', '感受'
    ]
    
    text_lower = text.lower()
    count = sum(1 for word in emotional if word in text_lower)
    return count / max(1, len(text.split()) / 5)


def detect_casual_language(text):
    """檢測口語表達"""
    casual = [
        'like', 'you know', 'basically', 'literally',
        'actually', 'honestly', 'pretty', 'kind of',
        'sort of', 'gonna', 'wanna', '就像', '你知道', '基本上'
    ]
    
    text_lower = text.lower()
    count = sum(1 for word in casual if word in text_lower)
    return count / max(1, len(text.split()) / 5)


def detect_personal_opinions(text):
    """檢測個人觀點"""
    opinions = [
        'i think', 'i believe', 'my opinion', 'i would say',
        'personally', 'to me', 'in my view',
        '我認為', '我相信', '我的看法', '個人來說'
    ]
    
    text_lower = text.lower()
    count = sum(1 for op in opinions if op in text_lower)
    return count / max(1, len(text.split()) / 5)


def analyze_text(text, sensitivity):
    """分析文本並返回 AI/Human 分數"""
    
    # === AI 特徵 ===
    ai_features = {}
    ai_scores = []
    
    # 1. 重複短語
    repeated = count_repeated_phrases(text)
    ai_features['重複短語多'] = repeated > 3
    if repeated > 3:
        ai_scores.append(0.15)
    
    # 2. 正式措辭
    formal = detect_formal_language(text)
    ai_features['過度正式'] = formal > 0.6
    if formal > 0.6:
        ai_scores.append(0.12)
    
    # 3. 完美語法
    grammar = check_grammar_perfection(text)
    ai_features['語法完美'] = grammar > 0.8
    if grammar > 0.8:
        ai_scores.append(0.12)
    
    # 4. 模式化表述
    formulaic = check_formulaic_patterns(text)
    ai_features['模式化短語'] = formulaic
    if formulaic:
        ai_scores.append(0.10)
    
    # 5. 結構規律
    structure = analyze_structure(text)
    ai_features['結構過規律'] = structure > 0.7
    if structure > 0.7:
        ai_scores.append(0.10)
    
    # === 人類特徵 ===
    human_features = {}
    human_scores = []
    
    # 1. 縮寫使用
    contractions = count_contractions(text)
    human_features['使用縮寫'] = contractions > 1
    if contractions > 1:
        human_scores.append(0.15)
    
    # 2. 自然錯誤
    errors = detect_natural_errors(text)
    human_features['自然錯誤'] = errors > 0.01
    if errors > 0.01:
        human_scores.append(0.12)
    
    # 3. 情感詞彙
    emotion = detect_emotional_language(text)
    human_features['情感表現'] = emotion > 0.05
    if emotion > 0.05:
        human_scores.append(0.15)
    
    # 4. 口語表達
    casual = detect_casual_language(text)
    human_features['口語用詞'] = casual > 0.05
    if casual > 0.05:
        human_scores.append(0.12)
    
    # 5. 個人觀點
    opinion = detect_personal_opinions(text)
    human_features['個人觀點'] = opinion > 0.05
    if opinion > 0.05:
        human_scores.append(0.10)
    
    # 計算分數
    ai_base = min(0.95, sum(ai_scores) + 0.15)
    human_base = min(0.95, sum(human_scores) + 0.1)
    
    total = ai_base + human_base
    ai_score = ai_base / total if total > 0 else 0.5
    human_score = 1 - ai_score
    
    # 應用靈敏度
    if sensitivity < 0.75:
        ai_score = ai_score * 0.85
        human_score = 1 - ai_score
    elif sensitivity > 0.85:
        ai_score = min(0.99, ai_score * 1.15)
        human_score = 1 - ai_score
    
    details = {
        'ai_features': ai_features,
        'human_features': human_features
    }
    
    return ai_score, human_score, details


# ============================================================================
# Streamlit 應用頁面
# ============================================================================

# 設定頁面
st.set_page_config(
    page_title="AI vs Human 文章偵測器",
    page_icon="📝",
    layout="wide"
)

# 標題
st.title("🤖 AI vs Human 文章偵測器")
st.markdown("### 使用文本特徵分析技術辨別文章來源")
st.markdown("---")

# 側邊欄設定
with st.sidebar:
    st.header("⚙️ 設定")
    sensitivity = st.slider("檢測靈敏度", 0.5, 1.0, 0.75, 0.05)
    st.info("靈敏度越高，對 AI 文本越敏感")

# 主容器
col1, col2 = st.columns([3, 1])

with col1:
    st.subheader("📄 輸入文本")
    user_text = st.text_area(
        "貼上你要檢測的文章",
        height=300,
        placeholder="至少20個字元...",
        label_visibility="collapsed"
    )

with col2:
    st.subheader("📊 統計")
    if user_text:
        words = user_text.split()
        st.metric("字元", len(user_text))
        st.metric("詞數", len(words))
    else:
        st.info("輸入文本後顯示統計")

st.markdown("---")

# 分析按鈕
if st.button("🔍 開始分析", use_container_width=True):
    if not user_text or len(user_text.strip()) < 20:
        st.error("❌ 請輸入至少 20 個字元")
    else:
        with st.spinner("分析中..."):
            time.sleep(0.5)
            
            # 執行分析
            ai_score, human_score, details = analyze_text(user_text, sensitivity)
            
            st.markdown("---")
            st.subheader("🎯 檢測結果")
            
            col_ai, col_human = st.columns(2)
            with col_ai:
                st.metric("🤖 AI 生成", f"{ai_score*100:.1f}%")
            with col_human:
                st.metric("👤 人類撰寫", f"{human_score*100:.1f}%")
            
            # 進度條
            st.progress(ai_score, text="AI 可能性")
            
            st.markdown("---")
            st.subheader("📋 詳細特徵分析")
            
            col_ai_feat, col_human_feat = st.columns(2)
            with col_ai_feat:
                st.write("**AI 特徵**")
                for feat, score in details['ai_features'].items():
                    st.write(f"{'✅' if score else '❌'} {feat}")
            
            with col_human_feat:
                st.write("**人類特徵**")
                for feat, score in details['human_features'].items():
                    st.write(f"{'✅' if score else '❌'} {feat}")
            
            st.markdown("---")
            st.subheader("💡 結論")
            
            if ai_score > 0.75:
                st.error("⚠️ **高度可能是 AI 生成**")
                st.write("特徵: 高度結構化、語法完美、缺乏個人風格")
            elif ai_score > 0.55:
                st.warning("🤔 **可能包含 AI 成分**")
                st.write("這篇文章可能由 AI 部分撰寫或大量編輯")
            else:
                st.success("✅ **很可能是人類撰寫**")
                st.write("特徵: 自然表達、個人風格、情感表現")

st.markdown("---")
st.markdown("<div style='text-align: center; color: #888; font-size: 11px;'>AI vs Human 文章偵測器 | HW5 Q1</div>", unsafe_allow_html=True)

