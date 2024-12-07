# coding=utf-8
# Copyright 2024 The Google Research Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Utility library of instructions."""

import functools
import random
import re
from typing import List

import immutabledict
import nltk

WORD_LIST = ["西方", "句子", "信号", "倾倒", "地点", "相反", "底部", "土豆", "行政", "工作", "欢迎", "早晨", "好", "代理", "主要", "愿望", "责任", "新闻", "问题", "总统", "偷", "刷子", "读", "类型", "节拍", "教练", "成长", "锁", "骨头", "案例", "平等", "舒适", "区域", "替代", "表现", "伙伴", "走", "药物", "电影", "事物", "岩石", "轻拍", "总计", "竞争", "轻松", "南", "建立", "聚集", "停车", "世界", "充足", "呼吸", "声明", "酒精", "贸易", "亲爱的", "亮点", "街道", "问题", "决定", "混乱", "协议", "工作室", "教练", "协助", "大脑", "翅膀", "风格", "私人", "顶部", "棕色", "腿", "购买", "程序", "方法", "速度", "高", "公司", "有价值", "派", "分析师", "会议", "模式", "区", "愉快", "晚餐", "游泳", "笑话", "订单", "盘子", "部门", "马达", "细胞", "花费", "柜子", "差异", "力量", "考试", "引擎", "马", "维度", "支付", "脚趾", "曲线", "文学", "打扰", "火", "可能性", "辩论", "活动", "通过", "你好", "周期", "背景", "安静", "作者", "效果", "演员", "页面", "自行车", "错误", "喉咙", "攻击", "字符", "电话", "茶", "增加", "结果", "文件", "具体", "检查员", "内部", "潜力", "员工", "建筑", "雇主", "鞋子", "手", "方向", "花园", "购买", "面试", "学习", "认知", "成员", "精神", "烤箱", "三明治", "怪异", "乘客", "特别", "反应", "反应", "大小", "变化", "一个", "取消", "糖果", "出口", "客人", "条件", "飞", "价格", "弱点", "转换", "酒店", "伟大", "嘴", "心", "歌", "糖", "怀疑", "电话", "耳", "屋顶", "油漆", "冰箱", "组织", "陪审团", "奖励", "工程", "日", "所有物", "船员", "酒吧", "道路", "描述", "庆祝", "分数", "标记", "信", "淋浴", "建议", "先生", "运气", "国家", "进展", "大厅", "中风", "理论", "报价", "故事", "税", "定义", "历史", "骑", "中等", "开幕", "玻璃", "电梯", "胃", "问题", "能力", "领导", "村庄", "计算机", "城市", "宏伟", "自信", "蜡烛", "神父", "推荐", "点", "必要", "身体", "桌子", "秘密", "恐怖", "噪音", "文化", "警告", "水", "圆", "饮食", "花", "公共汽车", "坚韧", "许可", "周", "提示", "连接", "虐待", "高度", "保存", "角落", "边界", "压力", "驾驶", "停止", "撕裂", "餐", "听", "混乱", "女朋友", "生活", "关系", "重要性", "计划", "创意", "气氛", "责备", "邀请", "住房", "纸", "饮料", "卷", "银", "醉", "年龄", "损害", "烟", "环境", "包装", "储蓄", "影响", "游客", "雨", "邮寄", "标志", "祖母", "跑", "利润", "推动", "职员", "最终", "葡萄酒", "游泳", "暂停", "东西", "歌手", "葬礼", "平均", "来源", "场景", "传统", "个人", "雪", "没有人", "距离", "排序", "敏感", "动物", "主要", "谈判", "点击", "心情", "期间", "到达", "表达", "假期", "重复", "尘土", "衣柜", "金", "坏", "航行", "组合", "衣服", "强调", "责任", "黑", "步骤", "学校", "跳跃", "文件", "专业", "嘴唇", "化学", "前面", "醒来", "而", "内部", "观看", "排", "主题", "惩罚", "平衡", "可能", "成人", "旁边", "样本", "上诉", "婚礼", "深度", "国王", "奖励", "妻子", "吹", "网站", "营地", "音乐", "安全", "礼物", "故障", "猜", "行为", "羞耻", "戏剧", "资本", "考试", "愚蠢", "记录", "声音", "秋千", "小说", "最小", "比例", "机器", "形状", "铅", "操作", "薪水", "云", "事务", "打击", "章节", "舞台", "数量", "访问", "军队", "链", "交通", "踢", "分析", "机场", "时间", "假期", "哲学", "球", "胸部", "谢谢", "地方", "山", "广告", "红", "过去", "租", "返回", "旅游", "房子", "建筑", "网", "本地", "战争", "图形", "费用", "喷雾", "用户", "污垢", "射击", "任务", "粘", "朋友", "软件", "晋升", "互动", "包围", "区块", "目的", "实践", "冲突", "日常", "需求", "奖金", "洞", "状态", "初级", "甜", "捕捉", "眼泪", "折叠", "墙", "编辑", "生活", "位置", "英镑", "尊重", "浴室", "外套", "脚本", "工作", "教", "出生", "观点", "解决", "主题", "雇员", "怀疑", "市场", "教育", "服务", "恢复", "语调", "伤害", "错过", "工会", "理解", "奶牛", "河流", "协会", "概念", "训练", "食谱", "关系", "保留", "抑郁", "证明", "头发", "收入", "独立", "提升", "任务", "临时", "数量", "损失", "边缘", "轨道", "检查", "绳索", "估算", "污染", "稳定", "信息", "交付", "视角", "镜子", "助手", "代表", "证人", "自然", "法官", "水果", "小费", "魔鬼", "城镇", "紧急", "上面", "掉落", "保持", "人类", "脖子", "扬声器", "网络", "唱", "抗拒", "联盟", "旅行", "签名", "律师", "重要性", "气体", "选择", "工程师", "成功", "部分", "外部", "工人", "简单", "四分之一", "学生", "心脏", "通过", "尽管", "变化", "粗糙", "女士", "草", "社区", "车库", "年轻", "标准", "裙子", "承诺", "盲", "电视", "疾病", "委员会", "积极", "能量", "冷静", "存在", "调", "基础", "偏好", "头", "共同", "割", "某处", "展示", "当前", "思维", "革命", "努力", "大师", "实施", "共和国", "楼", "原则", "陌生人", "肩膀", "年级", "按钮", "网球", "警察", "收集", "账户", "登记", "手套", "分配", "教授", "椅子", "优先", "结合", "和平", "扩展", "也许", "开始", "法院", "记录", "论文", "白色", "假设", "选项", "添加", "申请", "钥匙", "设计", "举起", "湖", "保存", "日历", "考生", "称呼", "责任", "粉", "广告", "改善", "冷", "停车", "认识", "关键", "大", "方向", "男孩", "潜在", "未来", "医院", "可能", "非常", "早餐", "四", "紧张", "点", "压力", "土壤", "批评", "歌曲", "挑战", "工程", "经济", "表演", "表面", "可能", "女孩", "复习", "报告", "发生", "计划", "斗争", "厕所", "对比", "种子", "学校", "数据", "讨论", "公司", "注意", "心态", "条形", "课程", "答案", "原始", "组织", "文化", "鸡", "逐渐", "讲座", "结论", "电话", "艺术", "机会", "未来", "朋友", "姿势", "警告", "改善", "参与", "女性", "设计", "女孩", "流", "花费", "依赖", "战争", "前", "条件", "现金", "修复", "建立", "天", "建筑", "获取", "沟通", "申请", "主角", "心灵", "地方", "责任", "秘密", "打击", "增加", "设定", "请求", "材料", "资金", "破裂", "可能", "体育", "周边", "门", "减轻", "学习", "进展", "生活", "医生", "买", "识别", "吸引", "证书", "记者", "城市", "安全", "绿色", "设计", "重要", "思维", "背景", "更改", "胜利", "模块", "选择", "选项", "顶部", "活动", "音乐", "病", "实施", "关卡", "舞蹈", "深度", "极限", "引导", "极性", "吸引", "参与", "沉默", "代替", "需要", "单元", "前进", "导航", "精力", "目标", "记住", "退出", "速度", "重要", "策略", "能力", "应用", "关键", "检查", "声明", "粉碎", "公司", "获得", "转换", "管理", "信号", "人才", "标准", "数量", "电话", "分析", "刺激", "稳定", "避免", "策略", "计划", "年", "循环", "活动", "继续", "员工", "管理", "创建", "网站", "角色", "市场", "方法", "目标", "合作", "方法", "游戏", "文化", "家庭", "团队", "分配", "影响", "设计", "个人", "障碍", "演员", "信号", "小心", "跟进", "完美", "早期", "发明", "关卡", "工作", "火车", "详细", "阻力", "加油", "工具", "通信", "思维", "障碍", "进程", "后续", "优化", "设备", "专注", "行动", "创意", "工具", "政策", "回答", "解释", "主题", "发生", "种类", "展示", "预定", "主题", "确认", "展示", "外形", "点缀", "演讲", "反应", "战术", "观察", "演示", "稳定", "意识", "任务", "玩家", "动机", "方法", "进程", "批判", "影响", "增长", "转化", "目标", "调查", "计算", "有效", "景观", "专业", "自信", "思考", "反馈", "任务", "公司", "控制", "安全", "决策", "人类", "反馈", "说明", "重要", "前进", "管理", "数据", "个人", "评估", "显示", "规则", "控制", "反馈", "筛选", "重要", "调查", "过程", "优势", "系统", "工具", "管理", "结构", "前进", "行动", "管理", "解决", "数据", "成员", "目标", "新", "反馈", "稳定", "基于", "基础", "控制", "发展", "计划", "结构", "管理", "市场", "挑战", "信号", "管理", "分析", "优化", "规则", "实验", "进程", "管理", "信号", "进展", "确认", "管理", "调查", "步骤", "方案", "策略", "事件"]  

# ISO 639-1 codes to language names.
LANGUAGE_CODES = immutabledict.immutabledict({
    "en": "English",
    "es": "Spanish",
    "pt": "Portuguese",
    "ar": "Arabic",
    "hi": "Hindi",
    "fr": "French",
    "ru": "Russian",
    "de": "German",
    "ja": "Japanese",
    "it": "Italian",
    "bn": "Bengali",
    "uk": "Ukrainian",
    "th": "Thai",
    "ur": "Urdu",
    "ta": "Tamil",
    "te": "Telugu",
    "bg": "Bulgarian",
    "ko": "Korean",
    "pl": "Polish",
    "he": "Hebrew",
    "fa": "Persian",
    "vi": "Vietnamese",
    "ne": "Nepali",
    "sw": "Swahili",
    "kn": "Kannada",
    "mr": "Marathi",
    "gu": "Gujarati",
    "pa": "Punjabi",
    "ml": "Malayalam",
    "fi": "Finnish",
    })

_ALPHABETS = "([A-Za-z])"
_PREFIXES = "(Mr|St|Mrs|Ms|Dr)[.]"
_SUFFIXES = "(Inc|Ltd|Jr|Sr|Co)"
_STARTERS = r"(Mr|Mrs|Ms|Dr|Prof|Capt|Cpt|Lt|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
_ACRONYMS = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
_WEBSITES = "[.](com|net|org|io|gov|edu|me)"
_DIGITS = "([0-9])"
_MULTIPLE_DOTS = r"\.{2,}"


def split_into_sentences(text):
  """Split the text into sentences.

  Args:
    text: A string that consists of more than or equal to one sentences.

  Returns:
    A list of strings where each string is a sentence.
  """
  text = " " + text + "  "
  text = text.replace("\n", " ")
  text = re.sub(_PREFIXES, "\\1<prd>", text)
  text = re.sub(_WEBSITES, "<prd>\\1", text)
  text = re.sub(_DIGITS + "[.]" + _DIGITS, "\\1<prd>\\2", text)
  text = re.sub(
      _MULTIPLE_DOTS,
      lambda match: "<prd>" * len(match.group(0)) + "<stop>",
      text,
  )
  if "Ph.D" in text:
    text = text.replace("Ph.D.", "Ph<prd>D<prd>")
  text = re.sub(r"\s" + _ALPHABETS + "[.] ", " \\1<prd> ", text)
  text = re.sub(_ACRONYMS + " " + _STARTERS, "\\1<stop> \\2", text)
  text = re.sub(
      _ALPHABETS + "[.]" + _ALPHABETS + "[.]" + _ALPHABETS + "[.]",
      "\\1<prd>\\2<prd>\\3<prd>",
      text,
  )
  text = re.sub(
      _ALPHABETS + "[.]" + _ALPHABETS + "[.]", "\\1<prd>\\2<prd>", text
  )
  text = re.sub(" " + _SUFFIXES + "[.] " + _STARTERS, " \\1<stop> \\2", text)
  text = re.sub(" " + _SUFFIXES + "[.]", " \\1<prd>", text)
  text = re.sub(" " + _ALPHABETS + "[.]", " \\1<prd>", text)
  if "”" in text:
    text = text.replace(".”", "”.")
  if '"' in text:
    text = text.replace('."', '".')
  if "!" in text:
    text = text.replace('!"', '"!')
  if "?" in text:
    text = text.replace('?"', '"?')
  text = text.replace(".", ".<stop>")
  text = text.replace("?", "?<stop>")
  text = text.replace("!", "!<stop>")
  text = text.replace("<prd>", ".")
  sentences = text.split("<stop>")
  sentences = [s.strip() for s in sentences]
  if sentences and not sentences[-1]:
    sentences = sentences[:-1]
  return sentences


def count_words(text):
  """Counts the number of words."""
  tokenizer = nltk.tokenize.RegexpTokenizer(r"\w+")
  tokens = tokenizer.tokenize(text)
  num_words = len(tokens)
  return num_words


@functools.lru_cache(maxsize=None)
def _get_sentence_tokenizer():
  return nltk.data.load("nltk:tokenizers/punkt/english.pickle")


def count_sentences(text):
  """Count the number of sentences."""
  tokenizer = _get_sentence_tokenizer()
  tokenized_sentences = tokenizer.tokenize(text)
  return len(tokenized_sentences)


def generate_keywords(num_keywords):
  """Randomly generates a few keywords."""
  return random.sample(WORD_LIST, k=num_keywords)
