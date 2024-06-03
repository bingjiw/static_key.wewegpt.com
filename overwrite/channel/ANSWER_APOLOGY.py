import re

def contains_apology(text):
    apology_phrases = [
        "很抱歉", "对不起", "抱歉", "无法提供", "不能提供", "不能浏览", "无法实时",
        "不能查询", "无法查询", "作为AI", "作为人工智能", "作为一个基于", "历史数据训练", "语言模型"
    ]
    matched_phrases = []
    for phrase in apology_phrases:
        if phrase in text:
            position = text.index(phrase)
            # 如果文字不足100字，则按100字计算，目的是增加不足100字的文字的各项评分值
            score = 1 - (position / max(100, len(text)))
            matched_phrases.append((phrase, score))
    return matched_phrases


def contains_alternative_suggestion(text):
    suggestion_phrases = [
        "建议您", "查阅", "查看", "访问", "使用", "通过", "联系", "获取", "查找"
    ]
    matched_phrases = []
    for phrase in suggestion_phrases:
        if phrase in text:
            position = text.index(phrase)
            # 如果文字不足100字，则按100字计算，目的是增加不足100字的文字的各项评分值
            score = 1 - (position / max(100, len(text)))
            matched_phrases.append((phrase, score))
    return matched_phrases


def contains_information_terms(text):
    information_terms = [
        "信息", "数据", "消息", "动态", "最新预报", "天气", "气象", "最新的", "新闻"
    ]
    matched_terms = []
    for term in information_terms:
        if term in text:
            position = text.index(term)
            # 如果文字不足100字，则按100字计算，目的是增加不足100字的文字的各项评分值
            score = 1 - (position / max(100, len(text)))
            score = round(score, 1)   ### 将 score 四舍五入保留一位小数。这样，无论在哪里使用 score，它都只会显示一位小数。
            matched_terms.append((term, score))
    return matched_terms

#判断 AI回复的文本 决定要不要实时搜索
def analyze_text_features__need_search(text):
    matched_apologies = contains_apology(text)
    matched_suggestions = contains_alternative_suggestion(text)
    matched_info_terms = contains_information_terms(text)
    
    matched_count = (len(matched_apologies) > 0) + (len(matched_suggestions) > 0) + (len(matched_info_terms) > 0)
    matched_features = {
        "抱歉类": matched_apologies,
        "建议类": matched_suggestions,
        "信息类": matched_info_terms
    }
    
    # 计算总评分值
    sum_of_scores = sum(score for _, score in matched_apologies + matched_suggestions + matched_info_terms)
    
    return matched_count, matched_features, sum_of_scores
