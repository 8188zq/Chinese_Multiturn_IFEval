import json
import random
import re
random.seed(42)
path = ".\Chinese_Multiturn_IFEval\data\data_v1.1_release.jsonl"
questions = []
with open(path,"r", encoding='utf-8') as f:
    data = [json.loads(line) for line in f]
    for item in data:
        if item["category"] in ["综合问答","角色扮演","文本写作","中文理解","基本任务","专业能力"]:
            questions.append(item)

output_path = ".\Chinese_Multiturn_IFEval\data\multi_turn.jsonl"
new_data = []

DEFAULT_WORD_LIST = ["西方", "句子", "信号", "倾倒", "地点", "相反", "底部", "土豆", "行政", "工作", "欢迎", "早晨", "好", "代理", "主要", "愿望", "责任", "新闻", "问题", "总统", "偷", "刷子", "读", "类型", "节拍", "教练", "成长", "锁", "骨头", "案例", "平等", "舒适", "区域", "替代", "表现", "伙伴", "走", "药物", "电影", "事物", "岩石", "轻拍", "总计", "竞争", "轻松", "南", "建立", "聚集", "停车", "世界", "充足", "呼吸", "声明", "酒精", "贸易", "亲爱的", "亮点", "街道", "问题", "决定", "混乱", "协议", "工作室", "教练", "协助", "大脑", "翅膀", "风格", "私人", "顶部", "棕色", "腿", "购买", "程序", "方法", "速度", "高", "公司", "有价值", "派", "分析师", "会议", "模式", "区", "愉快", "晚餐", "游泳", "笑话", "订单", "盘子", "部门", "马达", "细胞", "花费", "柜子", "差异", "力量", "考试", "引擎", "马", "维度", "支付", "脚趾", "曲线", "文学", "打扰", "火", "可能性", "辩论", "活动", "通过", "你好", "周期", "背景", "安静", "作者", "效果", "演员", "页面", "自行车", "错误", "喉咙", "攻击", "字符", "电话", "茶", "增加", "结果", "文件", "具体", "检查员", "内部", "潜力", "员工", "建筑", "雇主", "鞋子", "手", "方向", "花园", "购买", "面试", "学习", "认知", "成员", "精神", "烤箱", "三明治", "怪异", "乘客", "特别", "反应", "反应", "大小", "变化", "一个", "取消", "糖果", "出口", "客人", "条件", "飞", "价格", "弱点", "转换", "酒店", "伟大", "嘴", "心", "歌", "糖", "怀疑", "电话", "耳", "屋顶", "油漆", "冰箱", "组织", "陪审团", "奖励", "工程", "日", "所有物", "船员", "酒吧", "道路", "描述", "庆祝", "分数", "标记", "信", "淋浴", "建议", "先生", "运气", "国家", "进展", "大厅", "中风", "理论", "报价", "故事", "税", "定义", "历史", "骑", "中等", "开幕", "玻璃", "电梯", "胃", "问题", "能力", "领导", "村庄", "计算机", "城市", "宏伟", "自信", "蜡烛", "神父", "推荐", "点", "必要", "身体", "桌子", "秘密", "恐怖", "噪音", "文化", "警告", "水", "圆", "饮食", "花", "公共汽车", "坚韧", "许可", "周", "提示", "连接", "虐待", "高度", "保存", "角落", "边界", "压力", "驾驶", "停止", "撕裂", "餐", "听", "混乱", "女朋友", "生活", "关系", "重要性", "计划", "创意", "气氛", "责备", "邀请", "住房", "纸", "饮料", "卷", "银", "醉", "年龄", "损害", "烟", "环境", "包装", "储蓄", "影响", "游客", "雨", "邮寄", "标志", "祖母", "跑", "利润", "推动", "职员", "最终", "葡萄酒", "游泳", "暂停", "东西", "歌手", "葬礼", "平均", "来源", "场景", "传统", "个人", "雪", "没有人", "距离", "排序", "敏感", "动物", "主要", "谈判", "点击", "心情", "期间", "到达", "表达", "假期", "重复", "尘土", "衣柜", "金", "坏", "航行", "组合", "衣服", "强调", "责任", "黑", "步骤", "学校", "跳跃", "文件", "专业", "嘴唇", "化学", "前面", "醒来", "而", "内部", "观看", "排", "主题", "惩罚", "平衡", "可能", "成人", "旁边", "样本", "上诉", "婚礼", "深度", "国王", "奖励", "妻子", "吹", "网站", "营地", "音乐", "安全", "礼物", "故障", "猜", "行为", "羞耻", "戏剧", "资本", "考试", "愚蠢", "记录", "声音", "秋千", "小说", "最小", "比例", "机器", "形状", "铅", "操作", "薪水", "云", "事务", "打击", "章节", "舞台", "数量", "访问", "军队", "链", "交通", "踢", "分析", "机场", "时间", "假期", "哲学", "球", "胸部", "谢谢", "地方", "山", "广告", "红", "过去", "租", "返回", "旅游", "房子", "建筑", "网", "本地", "战争", "图形", "费用", "喷雾", "用户", "污垢", "射击", "任务", "粘", "朋友", "软件", "晋升", "互动", "包围", "区块", "目的", "实践", "冲突", "日常", "需求", "奖金", "洞", "状态", "初级", "甜", "捕捉", "眼泪", "折叠", "墙", "编辑", "生活", "位置", "英镑", "尊重", "浴室", "外套", "脚本", "工作", "教", "出生", "观点", "解决", "主题", "雇员", "怀疑", "市场", "教育", "服务", "恢复", "语调", "伤害", "错过", "工会", "理解", "奶牛", "河流", "协会", "概念", "训练", "食谱", "关系", "保留", "抑郁", "证明", "头发", "收入", "独立", "提升", "任务", "临时", "数量", "损失", "边缘", "轨道", "检查", "绳索", "估算", "污染", "稳定", "信息", "交付", "视角", "镜子", "助手", "代表", "证人", "自然", "法官", "水果", "小费", "魔鬼", "城镇", "紧急", "上面", "掉落", "保持", "人类", "脖子", "扬声器", "网络", "唱", "抗拒", "联盟", "旅行", "签名", "律师", "重要性", "气体", "选择", "工程师", "成功", "部分", "外部", "工人", "简单", "四分之一", "学生", "心脏", "通过", "尽管", "变化", "粗糙", "女士", "草", "社区", "车库", "年轻", "标准", "裙子", "承诺", "盲", "电视", "疾病", "委员会", "积极", "能量", "冷静", "存在", "调", "基础", "偏好", "头", "共同", "割", "某处", "展示", "当前", "思维", "革命", "努力", "大师", "实施", "共和国", "楼", "原则", "陌生人", "肩膀", "年级", "按钮", "网球", "警察", "收集", "账户", "登记", "手套", "分配", "教授", "椅子", "优先", "结合", "和平", "扩展", "也许", "开始", "法院", "记录", "论文", "白色", "假设", "选项", "添加", "申请", "钥匙", "设计", "举起", "湖", "保存", "日历", "考生", "称呼", "责任", "粉", "广告", "改善", "冷", "停车", "认识", "关键", "大", "方向", "男孩", "潜在", "未来", "医院", "可能", "非常", "早餐", "四", "紧张", "点", "压力", "土壤", "批评", "歌曲", "挑战", "工程", "经济", "表演", "表面", "可能", "女孩", "复习", "报告", "发生", "计划", "斗争", "厕所", "对比", "种子", "学校", "数据", "讨论", "公司", "注意", "心态", "条形", "课程", "答案", "原始", "组织", "文化", "鸡", "逐渐", "讲座", "结论", "电话", "艺术", "机会", "未来", "朋友", "姿势", "警告", "改善", "参与", "女性", "设计", "女孩", "流", "花费", "依赖", "战争", "前", "条件", "现金", "修复", "建立", "天", "建筑", "获取", "沟通", "申请", "主角", "心灵", "地方", "责任", "秘密", "打击", "增加", "设定", "请求", "材料", "资金", "破裂", "可能", "体育", "周边", "门", "减轻", "学习", "进展", "生活", "医生", "买", "识别", "吸引", "证书", "记者", "城市", "安全", "绿色", "设计", "重要", "思维", "背景", "更改", "胜利", "模块", "选择", "选项", "顶部", "活动", "音乐", "病", "实施", "关卡", "舞蹈", "深度", "极限", "引导", "极性", "吸引", "参与", "沉默", "代替", "需要", "单元", "前进", "导航", "精力", "目标", "记住", "退出", "速度", "重要", "策略", "能力", "应用", "关键", "检查", "声明", "粉碎", "公司", "获得", "转换", "管理", "信号", "人才", "标准", "数量", "电话", "分析", "刺激", "稳定", "避免", "策略", "计划", "年", "循环", "活动", "继续", "员工", "管理", "创建", "网站", "角色", "市场", "方法", "目标", "合作", "方法", "游戏", "文化", "家庭", "团队", "分配", "影响", "设计", "个人", "障碍", "演员", "信号", "小心", "跟进", "完美", "早期", "发明", "关卡", "工作", "火车", "详细", "阻力", "加油", "工具", "通信", "思维", "障碍", "进程", "后续", "优化", "设备", "专注", "行动", "创意", "工具", "政策", "回答", "解释", "主题", "发生", "种类", "展示", "预定", "主题", "确认", "展示", "外形", "点缀", "演讲", "反应", "战术", "观察", "演示", "稳定", "意识", "任务", "玩家", "动机", "方法", "进程", "批判", "影响", "增长", "转化", "目标", "调查", "计算", "有效", "景观", "专业", "自信", "思考", "反馈", "任务", "公司", "控制", "安全", "决策", "人类", "反馈", "说明", "重要", "前进", "管理", "数据", "个人", "评估", "显示", "规则", "控制", "反馈", "筛选", "重要", "调查", "过程", "优势", "系统", "工具", "管理", "结构", "前进", "行动", "管理", "解决", "数据", "成员", "目标", "新", "反馈", "稳定", "基于", "基础", "控制", "发展", "计划", "结构", "管理", "市场", "挑战", "信号", "管理", "分析", "优化", "规则", "实验", "进程", "管理", "信号", "进展", "确认", "管理", "调查", "步骤", "方案", "策略", "事件"]  
_KEYWORD = "keywords:"
_TOTAL_NUMS=600
# _LANGUAGE = "language:"

_LENGTH = "length_constraints:"

_COMBINATION = "combination:"

_SYMBOLS = "symbols:"

_CHINESE = "chinese:"
from .. import instructions_registry
# from ..instruction_checker import ResponseLanguageChecker

INSTRUCTION_List = [
    _KEYWORD + "existence",
    _KEYWORD + "frequency",
    _KEYWORD + "forbidden_words",
    # _LANGUAGE + "response_language",
    _LENGTH + "number_paragraphs",
    _LENGTH + "number_words",
    _LENGTH + "number_words_range",
    _LENGTH + "number_of_ith_paragraph",
    _LENGTH + "number_of_ith_paragraph_range",
    _COMBINATION + "repeat_question_first",
    _COMBINATION + "two_response",
    _SYMBOLS + "bookname",
    _SYMBOLS + "each_paragragh_head",
    _SYMBOLS + "each_paragragh_tail",
    _SYMBOLS + "first_line_head",
    _SYMBOLS + "last_line_tail",
    _SYMBOLS + "json",
    _SYMBOLS + "markdown_bold",
    _SYMBOLS + "number_of_list",
    _SYMBOLS + "number_of_declarative",
    _SYMBOLS + "number_of_exlamatory",
    _SYMBOLS + "number_of_interrogative",
    _CHINESE + "two_part_with_tone",
    _CHINESE + "pinyin_checker",
    _CHINESE + "parallelism_checker",
    _CHINESE + "no_punctuation_checker",
]

def filter_punctuation(word_list):
    pattern = re.compile(r'^[\u4e00-\u9fa5]+$')  # 只匹配中文字符
    return [word for word in word_list if pattern.match(word)] # 只保留中文字符

def auto_generate_kwargs(instruction_id, ref, question):
    kwargs_list = [] 
    if instruction_id == _KEYWORD + "existence":
        import jieba
        words = jieba.cut(ref)
        word_list = list(words)
        word_list = filter_punctuation(word_list)
        if len(word_list) >= 2:
            keywords = random.sample(word_list, 2)  
        else:
            keywords = random.sample(DEFAULT_WORD_LIST, 2)
        kwargs = {"keywords": keywords}
        kwargs_list.append(kwargs)
        return kwargs_list
    if instruction_id == _KEYWORD + "frequency":
        import jieba
        words = jieba.cut(ref)
        word_list = list(words)
        word_list = filter_punctuation(word_list)
        try:
            keyword = random.choice(word_list)
        except:
            keyword = random.choice(DEFAULT_WORD_LIST)
            
        kwargs = {"keyword": keyword, "frequency": random.randint(2,3)}
        kwargs_list.append(kwargs)
        return kwargs_list
    if instruction_id == _KEYWORD + "forbidden_words":
        forbidden_words = random.sample([
    "和", "或", "但是", "而", "所以", "因为", "如果", "既然", "虽然", "即使", "在", "不过", "因此", "然后", "否则", 
    "同时", "除非", "只有", "即", "虽然", "但是", "然后", "而且", "此外", "的", "了", "是", "我", "你", "他", "她", "它", "我们", "你们", "他们", "这", "那", "有", "在", "和", "就", "不", "也", 
    "很", "对", "把", "把", "而", "所以", "但是", "如果", "因为", "虽然", "或", "或者", "与", "为", "被", "被", "在", "到", 
    "上", "下", "里", "前", "后", "中", "对", "与", "着", "从", "给", "向", "但", "即", "且", "如", "则", "也", "更", "只", 
    "都", "及", "及其", "并", "即使", "然而", "就", "也", "所", "能", "至", "此", "未"], 4)
        kwargs = {"forbidden_words": forbidden_words}
        kwargs_list.append(kwargs)
        return kwargs_list
    if instruction_id == _LENGTH + "number_paragraphs":
        kwargs = {"num_paragraphs": random.randint(1,3)}
        kwargs_list.append(kwargs)
        return kwargs_list
    if instruction_id == _LENGTH + "number_words":
        kwargs = {"num_words": random.choice([100,200,300]), "relation": random.choice(["超过","少于"])}
        kwargs_list.append(kwargs)
        return kwargs_list
    if instruction_id == _LENGTH + "number_words_range":
        kwargs = {"lower_limit_num_words": random.choice([100,200,300]), "upper_limit_num_words": random.choice([400,500,600])}
        kwargs_list.append(kwargs)
        return kwargs_list
    if instruction_id == _LENGTH + "number_of_ith_paragraph":
        kwargs = {"num_words": random.choice([100,200,300]), "relation": random.choice(["超过","少于"]),"ith": random.randint(1,3)}
        kwargs_list.append(kwargs)
        return kwargs_list
    if instruction_id == _LENGTH + "number_of_ith_paragraph_range":
        kwargs = {"lower_limit_num_words": random.choice([100,200,300]), "upper_limit_num_words": random.choice([400,500,600]),"ith": random.randint(1,3)}
        kwargs_list.append(kwargs)
        return kwargs_list
    if instruction_id == _COMBINATION + "repeat_question_first":
        prompt_to_repeat = question
        kwargs = {"prompt_to_repeat": prompt_to_repeat}
        kwargs_list.append(kwargs)
        return kwargs_list
    if instruction_id == _COMBINATION + "two_response":
        return [{}]
    if instruction_id == _SYMBOLS + "bookname":
        return [{}]
    if instruction_id == _SYMBOLS + "each_paragragh_head":
        special_word = random.choice(["我认为","我觉得","我想","客观地说","可以说","某种程度上","似乎","某种意义上","一般来说","事实上","实际上","总的来说","值得注意的是"])
        kwargs = {"special_word": special_word}
        kwargs_list.append(kwargs)
        return kwargs_list
    if instruction_id == _SYMBOLS + "each_paragragh_tail":
        special_word = random.choice(["吧","呀", "呢", "啊", "了", "的", "吧", "呢", "嘛", "哦", "哈", "啊", "啦", "对吧", "对不对", "是不是", "对吧", "啥的", "什么的"])
        kwargs = {"special_word": special_word}
        kwargs_list.append(kwargs)
        return kwargs_list
    if instruction_id == _SYMBOLS + "first_line_head":
        special_word = random.choice(["我认为","我觉得","我想","客观地说","可以说","某种程度上","似乎","某种意义上","一般来说","事实上","实际上","总的来说","值得注意的是"])
        kwargs = {"special_word": special_word}
        kwargs_list.append(kwargs)
        return kwargs_list
    if instruction_id == _SYMBOLS + "last_line_tail":
        special_word = random.choice(["吧","呀", "呢", "啊", "了", "的", "吧", "呢", "嘛", "哦", "哈", "啊", "啦", "对吧", "对不对", "是不是", "对吧", "啥的", "什么的"])
        kwargs = {"special_word": special_word}
        kwargs_list.append(kwargs)
        return kwargs_list
    if instruction_id == _SYMBOLS + "json":
        return [{}]
    if instruction_id == _SYMBOLS + "markdown_bold":
        num_bold = random.randint(1,5)
        kwargs = {"num_bold": num_bold}
        kwargs_list.append(kwargs)
        return kwargs_list
    if instruction_id == _SYMBOLS + "number_of_list":
        num_lists = random.randint(1,3)
        kwargs = {"num_lists": num_lists}
        kwargs_list.append(kwargs)
        return kwargs_list
    if instruction_id == _SYMBOLS + "number_of_declarative":
        special_word = random.choice(["对不对？","是不是？","对吧？","难道不是吗？"])
        kwargs = {"special_word": special_word}
        kwargs_list.append(kwargs)
        return kwargs_list
    if instruction_id == _SYMBOLS + "number_of_exlamatory":
        special_word = random.choice(["对不对？","是不是？","对吧？","难道不是吗？"])
        kwargs = {"special_word": special_word}
        kwargs_list.append(kwargs)
        return kwargs_list
    if instruction_id == _SYMBOLS + "number_of_interrogative":
        special_word = random.choice(["对不对？","是不是？","对吧？","难道不是吗？"])
        kwargs = {"special_word": special_word}
        kwargs_list.append(kwargs)
        return kwargs_list
    if instruction_id == _CHINESE + "two_part_with_tone":
        return [{}]
    if instruction_id == _CHINESE + "pinyin_checker":
        return [{}]
    if instruction_id == _CHINESE + "parallelism_checker":
        return [{}]
    if instruction_id == _CHINESE + "no_punctuation_checker":
        return [{}]
    print(f"instruction_id: {instruction_id}  not found!")
    return [{}]

conflicts = {
    _COMBINATION + "two_response":[
        f"{_LENGTH}number_paragraphs",
        f"{_LENGTH}number_of_ith_paragraph",
        f"{_LENGTH}number_of_ith_paragraph_range",
        f"{_SYMBOLS}each_paragragh_head",
        f"{_SYMBOLS}each_paragragh_tail",
    ],


    # 拼音检查与JSON格式规则冲突
    f"{_CHINESE}pinyin_checker": [
        f"{_SYMBOLS}json",
        f"{_LENGTH}number_paragraphs",  # 拼音和段落数相关要求也有冲突
        f"{_SYMBOLS}bookname",
        f"{_SYMBOLS}each_paragragh_head",
        f"{_SYMBOLS}each_paragragh_tail",
        # f"{_SYMBOLS}first_line_head",
        f"{_SYMBOLS}last_line_tail",
        # f"{_SYMBOLS}markdown_bold",
        # f"{_SYMBOLS}number_of_list",
        f"{_SYMBOLS}number_of_declarative",
        f"{_SYMBOLS}number_of_exlamatory",
        f"{_SYMBOLS}number_of_interrogative",
        f"{_COMBINATION}two_response",
        f"{_CHINESE}two_part_with_tone",  # 拼音检查与“两部分”要求冲突
        # f"{_CHINESE}parallelism_checker",
        f"{_CHINESE}no_punctuation_checker"
    ],

    f"{_SYMBOLS}bookname":[
        f"{_SYMBOLS}first_line_head",
        f"{_SYMBOLS}each_paragragh_head",
    ],

    # JSON格式与其他自然语言或语言规则冲突
    f"{_SYMBOLS}json": [
        f"{_LENGTH}number_paragraphs",
        # f"{_LENGTH}number_words",
        f"{_SYMBOLS}bookname",
        f"{_SYMBOLS}each_paragragh_head",
        f"{_SYMBOLS}each_paragragh_tail",
        f"{_SYMBOLS}first_line_head",
        f"{_SYMBOLS}last_line_tail",
        # f"{_SYMBOLS}markdown_bold",
        # f"{_SYMBOLS}number_of_list",
        # f"{_SYMBOLS}number_of_declarative",
        # f"{_SYMBOLS}number_of_exlamatory",
        # f"{_SYMBOLS}number_of_interrogative",
        f"{_CHINESE}two_part_with_tone",
        f"{_CHINESE}pinyin_checker",
        # f"{_CHINESE}parallelism_checker",
        f"{_CHINESE}no_punctuation_checker",
        f"{_COMBINATION}two_response"
    ],

    # 两段分隔规则与其他段落数或语言规则冲突
    f"{_CHINESE}two_part_with_tone": [
        f"{_CHINESE}pinyin_checker",  # 拼音检查与两段要求冲突
        f"{_CHINESE}no_punctuation_checker",
        f"{_SYMBOLS}json",  # JSON格式与两段分隔冲突
        f"{_LENGTH}number_paragraphs",
        f"{_SYMBOLS}each_paragragh_head",
        f"{_SYMBOLS}each_paragragh_tail",
        # f"{_SYMBOLS}first_line_head",
        f"{_SYMBOLS}last_line_tail",
        f"{_SYMBOLS}markdown_bold",
        f"{_SYMBOLS}number_of_list",
        # f"{_SYMBOLS}number_of_declarative",
        # f"{_SYMBOLS}number_of_exlamatory",
        # f"{_SYMBOLS}number_of_interrogative",
        f"{_COMBINATION}two_response"
    ],

    # 重复问题与双回答规则冲突
    f"{_COMBINATION}repeat_question_first": [
        f"{_COMBINATION}two_response",
        f"{_SYMBOLS}first_line_head",
        f"{_SYMBOLS}each_paragragh_head",
        f"{_CHINESE}no_punctuation_checker",
        f"{_CHINESE}pinyin_checker",
        f"{_SYMBOLS}number_of_declarative",
        f"{_SYMBOLS}number_of_interrogative",
        f"{_SYMBOLS}json",
        f"{_CHINESE}two_part_with_tone", 
    ],

    # 两段分隔与段落字数或段落要求冲突
    f"{_LENGTH}number_of_ith_paragraph": [
        f"{_CHINESE}two_part_with_tone",  # ith段落字数要求与两段分隔规则冲突
        f"{_SYMBOLS}json",
        # f"{_SYMBOLS}bookname",
        # f"{_SYMBOLS}each_paragragh_head",
        # f"{_SYMBOLS}each_paragragh_tail",
        # f"{_SYMBOLS}first_line_head",
        # f"{_SYMBOLS}last_line_tail",
        # f"{_SYMBOLS}markdown_bold",
        # f"{_SYMBOLS}number_of_list",
        # f"{_SYMBOLS}number_of_declarative",
        # f"{_SYMBOLS}number_of_exlamatory",
        # f"{_SYMBOLS}number_of_interrogative",
        f"{_COMBINATION}two_response",
        f"{_CHINESE}pinyin_checker",
        # f"{_CHINESE}parallelism_checker",
        f"{_CHINESE}no_punctuation_checker"
    ],
    f"{_LENGTH}number_of_ith_paragraph_range": [
        f"{_CHINESE}two_part_with_tone",  # ith段落字数要求与两段分隔规则冲突
        f"{_SYMBOLS}json",
        f"{_COMBINATION}two_response",
        f"{_CHINESE}pinyin_checker",
        f"{_CHINESE}no_punctuation_checker"
    ],

    # 拼音检查与文言文（无标点）规则冲突
    f"{_CHINESE}no_punctuation_checker": [
        _LENGTH + "number_paragraphs",
        _LENGTH + "number_of_ith_paragraph",
        _LENGTH + "number_of_ith_paragraph_range",
        _COMBINATION + "repeat_question_first"
        f"{_CHINESE}pinyin_checker",  # 拼音标注与无标点文言文冲突
        f"{_CHINESE}two_part_with_tone",
        f"{_SYMBOLS}json",
        f"{_SYMBOLS}bookname",
        f"{_SYMBOLS}each_paragragh_head",
        f"{_SYMBOLS}each_paragragh_tail",
        # f"{_SYMBOLS}first_line_head",
        # f"{_SYMBOLS}last_line_tail",
        f"{_SYMBOLS}markdown_bold",
        f"{_SYMBOLS}number_of_list",
        f"{_SYMBOLS}number_of_declarative",
        f"{_SYMBOLS}number_of_exlamatory",
        f"{_SYMBOLS}number_of_interrogative",
        f"{_COMBINATION}two_response",
        f"{_CHINESE}parallelism_checker"
    ],

    # 排比句检查与其他格式规则冲突
    f"{_CHINESE}parallelism_checker": [
        f"{_SYMBOLS}json",
        f"{_SYMBOLS}bookname",
        # f"{_SYMBOLS}each_paragragh_head",
        # f"{_SYMBOLS}each_paragragh_tail",
        # f"{_SYMBOLS}first_line_head",
        # f"{_SYMBOLS}last_line_tail",
        # f"{_SYMBOLS}markdown_bold",
        # f"{_SYMBOLS}number_of_list",
        f"{_SYMBOLS}number_of_declarative",
        # f"{_SYMBOLS}number_of_exlamatory",
        # f"{_SYMBOLS}number_of_interrogative",
        # f"{_CHINESE}two_part_with_tone",
        f"{_CHINESE}no_punctuation_checker",
        # f"{_CHINESE}pinyin_checker",
        # f"{_COMBINATION}two_response"
    ]
}



def check_conflict(group, item):
    """检查 group 中是否有与 item 冲突的元素"""
    for existing_item in group:
        if item in conflicts.get(existing_item, []):
            return True
    return False

def generate_instruction_id_list(instruction_list, nums):
    instruction_id_list = []
    
    # 用来统计每个元素使用的次数
    usage_count = {item: 0 for item in instruction_list}
    
    # 生成 nums 组，每组 3 个元素
    for _ in range(nums):
        group = []
        available_instructions = instruction_list[:]  # 拷贝列表，避免修改原始列表
        flag_min_used = True  # 是否优先尝试 usage_count 最小的元素

        while len(group) < 3:
            if not available_instructions:
                raise ValueError("没有足够的可用元素来生成更多的组。请检查元素数量或冲突规则。")
            
            if flag_min_used:  # 优先尝试使用次数最少的元素
                min_usage = min(usage_count[item] for item in available_instructions)
                candidates = [item for item in available_instructions if usage_count[item] == min_usage]
                item = random.choice(candidates)  # 选择 usage_count 最小的一个
                flag_min_used = False  # 只在第一次选择时启用
            else:  # 之后随机选择
                item = random.choice(available_instructions)
            
            # 检查是否和当前组内的元素有冲突
            if not check_conflict(group, item):
                group.append(item)
                usage_count[item] += 1
                available_instructions.remove(item)  # 将已选的元素从可选列表中移除

        instruction_id_list.append(group)

    return instruction_id_list,usage_count

INSTRUCTION_List_multiturn,usage_count = generate_instruction_id_list(INSTRUCTION_List, nums = _TOTAL_NUMS)
# print(INSTRUCTION_List_multiturn)
# print(len(INSTRUCTION_List_multiturn))
# print(usage_count)
# exit(0)

for index, item in enumerate(questions):
    try:
        instruction_id = INSTRUCTION_List_multiturn[index]
    except:
        break
    temp = {}
    kwargs_list = []
    prompt_list = []
    for turn, single_turn_instruction_id in enumerate(instruction_id):
        instruction_cls = instructions_registry.INSTRUCTION_DICT.get(single_turn_instruction_id)
        instruction = instruction_cls(single_turn_instruction_id)
        kwargs = auto_generate_kwargs(single_turn_instruction_id, item["reference"], item["question"])
        kwargs_list.extend(kwargs)
        try:
            if len(kwargs) == 0:
                require = instruction.build_description()
            else:
                require = instruction.build_description(**kwargs[0])
        except:
            print(f"error: {single_turn_instruction_id}")
            continue
        if turn == 0:
            prompt = item["question"] + "\n" + require
        else:
            prompt = require
        prompt_list.append(prompt)
        if turn == 2:
            temp = {
                "key": index,
                "prompt": prompt_list,
                "question": item["question"],
                "instruction_id_list": instruction_id,
                "kwargs": kwargs_list,
            }
            new_data.append(temp)
    
with open(output_path, "w", encoding='utf-8') as g:
    for item in new_data:
        g.write(json.dumps(item,ensure_ascii=False) + "\n")
        g.flush()