import streamlit as st
import random
import pandas as pd
import numpy as np
import time
from datetime import datetime
import hashlib

# ==========================================
# 1. 配置与样式 (Mobile UI Optimization)
# ==========================================
st.set_page_config(
    page_title="时空彩票预测",
    page_icon="🔮",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 自定义CSS，让界面看起来像原生App，并绘制彩票球
st.markdown("""
<style>
    /* 全局样式调整 */
    .main {
        background-color: #f0f2f6;
    }
    h1, h2, h3 {
        font-family: 'Helvetica Neue', sans-serif;
        color: #333;
    }
    
    /* 彩票球样式 */
    .ball-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 8px;
        margin: 20px 0;
    }
    .ball {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        color: white;
        font-size: 16px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
    }
    .red-ball {
        background: radial-gradient(circle at 10px 10px, #ff5e62, #ff0000);
        border: 2px solid #ffcccc;
    }
    .blue-ball {
        background: radial-gradient(circle at 10px 10px, #56ccf2, #2f80ed);
        border: 2px solid #cceeff;
    }
    
    /* 卡片样式 */
    .card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        text-align: center;
    }
    
    /* 按钮样式优化 */
    .stButton>button {
        width: 100%;
        border-radius: 25px;
        height: 50px;
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        font-size: 18px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. 核心逻辑类 (Backend Logic)
# ==========================================

class LotteryEngine:
    def __init__(self):
        # 双色球规则: 红球33选6, 蓝球16选1
        self.ssq_rule = {'red_max': 33, 'red_count': 6, 'blue_max': 16, 'blue_count': 1}
        # 大乐透规则: 红球35选5, 蓝球12选2
        self.dlt_rule = {'red_max': 35, 'red_count': 5, 'blue_max': 12, 'blue_count': 2}

    def _get_spacetime_seed(self):
        """
        获取时空种子：
        结合当前时间戳(微秒)、日期哈希、以及用户会话ID模拟的空间信息
        """
        now = datetime.now()
        # 基础时间因子
        time_factor = now.timestamp()
        # 模拟的空间因子 (在真实App中可调用GPS API，这里用随机模拟位置变化)
        space_mock = random.uniform(0, 1000) 
        # 组合生成唯一种子
        seed_str = f"{time_factor}-{space_mock}-{now.farthest_clock_check if hasattr(now, 'farthest_clock_check') else 'chaos'}"
        seed_hash = int(hashlib.sha256(seed_str.encode('utf-8')).hexdigest(), 16)
        return seed_hash % (10**8) # 取一个合适的整数范围

    def get_hot_numbers(self, lottery_type, ball_type, max_num, history_df):
        """
        基于历史数据计算热号权重
        """
        # 模拟权重计算：统计过去100期出现的频率
        # 这里为了演示，如果没有真实数据，生成一个正态分布的偏好
        freq = history_df[f"{lottery_type}_{ball_type}"].value_counts()
        weights = []
        for i in range(1, max_num + 1):
            w = freq.get(i, 0) + 1 # 基础权重为1，避免0概率
            weights.append(w)
        return weights

    def predict(self, lottery_type, algorithm="spacetime"):
        """
        核心预测函数
        :param lottery_type: 'ssq' or 'dlt'
        :param algorithm: 'spacetime' (时空), 'random' (纯随机), 'hot' (热号追踪)
        """
        rule = self.ssq_rule if lottery_type == 'ssq' else self.dlt_rule
        
        red_pool = list(range(1, rule['red_max'] + 1))
        blue_pool = list(range(1, rule['blue_max'] + 1))
        
        # 设置随机种子
        if algorithm == "spacetime":
            seed = self._get_spacetime_seed()
            random.seed(seed)
            np.random.seed(seed)
            
        elif algorithm == "hot":
            # 热号模式使用加权随机，这里简化模拟
            # 实际上应该基于历史数据加权
            pass 

        # 生成红球 (不重复)
        if algorithm == "hot":
            # 模拟热号：给中间数字更高权重
            weights = [1 + np.sin(x/3) for x in red_pool] # 假装的分布
            weights = np.array(weights) / sum(weights)
            red_balls = np.random.choice(red_pool, size=rule['red_count'], replace=False, p=weights)
        else:
            red_balls = random.sample(red_pool, rule['red_count'])
            
        red_balls = sorted(list(red_balls))
        
        # 生成蓝球
        if algorithm == "hot":
             blue_balls = np.random.choice(blue_pool, size=rule['blue_count'], replace=False)
        else:
            blue_balls = random.sample(blue_pool, rule['blue_count'])
            
        blue_balls = sorted(list(blue_balls))
        
        return red_balls, blue_balls

# ==========================================
# 3. 模拟数据生成 (Mock Data)
# ==========================================
@st.cache_data
def generate_history_data():
    """生成模拟的近期开奖记录用于分析展示"""
    data = []
    # 生成最近30期双色球数据
    for i in range(30):
        reds = random.sample(range(1, 34), 6)
        blue = random.randint(1, 16)
        data.append({
            "issue": 2025001 + i,
            "type": "ssq",
            "reds": reds,
            "blue": blue,
            # 扁平化用于统计
            **{f"ssq_red": r for r in reds}, # 简化统计逻辑
            "ssq_blue": blue
        })
    return pd.DataFrame(data)

# ==========================================
# 4. 前端界面 (Streamlit Frontend)
# ==========================================

def draw_balls_html(reds, blues):
    """生成彩票球的HTML组件"""
    html = '<div class="ball-container">'
    for r in reds:
        html += f'<div class="ball red-ball">{r:02d}</div>'
    for b in blues:
        html += f'<div class="ball blue-ball">{b:02d}</div>'
    html += '</div>'
    return html

def main():
    engine = LotteryEngine()
    
    # --- 侧边栏 ---
    with st.sidebar:
        st.title("⚙️ 设置")
        algo = st.radio("预测算法模型", ["时空共振 (推荐)", "大数据热号", "纯量子随机"])
        
        algo_map = {
            "时空共振 (推荐)": "spacetime",
            "大数据热号": "hot",
            "纯量子随机": "random"
        }
        selected_algo = algo_map[algo]
        
        st.info("💡 说明：\n\n'时空共振'算法抓取当前毫秒级时间戳与模拟的空间场作为随机熵源，为您寻找当下的'缘分号码'。")

    # --- 主界面 ---
    st.markdown("<div style='text-align: center; margin-bottom: 20px;'><h1>🎰 幸运预测大师</h1></div>", unsafe_allow_html=True)
    
    # 选项卡切换彩种
    tab1, tab2 = st.tabs(["双色球 (Union Lotto)", "超级大乐透 (Super Lotto)"])
    
    # --- 双色球 Tab ---
    with tab1:
        st.markdown("<div class='card'><h3>双色球预测</h3><p style='color:gray; font-size:12px;'>6个红球 + 1个蓝球</p>", unsafe_allow_html=True)
        
        # 显示时空信息
        now = datetime.now()
        st.caption(f"当前时空坐标: {now.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}")
        
        if st.button("🔮 开启时空预测 (SSQ)", key="btn_ssq"):
            with st.spinner("正在链接时空能量场..."):
                time.sleep(0.8) # 增加仪式感
                reds, blues = engine.predict('ssq', selected_algo)
                
                st.markdown(draw_balls_html(reds, blues), unsafe_allow_html=True)
                
                st.success(f"预测成功！这是属于您此刻的 {algo} 推荐。")
                
                # 解析结果
                st.markdown(f"""
                <div style='background:#f9f9f9; padding:10px; border-radius:8px; margin-top:10px; font-size:14px;'>
                    <b>红球:</b> {', '.join([f"{r:02d}" for r in reds])}<br>
                    <b>蓝球:</b> {', '.join([f"{b:02d}" for b in blues])}
                </div>
                """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # --- 大乐透 Tab ---
    with tab2:
        st.markdown("<div class='card'><h3>超级大乐透预测</h3><p style='color:gray; font-size:12px;'>5个红球 + 2个蓝球</p>", unsafe_allow_html=True)
        
        st.caption(f"当前时空坐标: {now.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}")
        
        if st.button("🔮 开启时空预测 (DLT)", key="btn_dlt"):
            with st.spinner("正在计算历史走势与熵值..."):
                time.sleep(0.8)
                reds, blues = engine.predict('dlt', selected_algo)
                
                st.markdown(draw_balls_html(reds, blues), unsafe_allow_html=True)
                
                st.success(f"预测成功！祝您好运连连。")
                
                 # 解析结果
                st.markdown(f"""
                <div style='background:#f9f9f9; padding:10px; border-radius:8px; margin-top:10px; font-size:14px;'>
                    <b>红球:</b> {', '.join([f"{r:02d}" for r in reds])}<br>
                    <b>蓝球:</b> {', '.join([f"{b:02d}" for b in blues])}
                </div>
                """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # --- 底部数据分析展示 ---
    st.markdown("---")
    st.subheader("📊 历史大数据走势 (模拟)")
    
    # 简单的图表展示
    chart_data = pd.DataFrame(
        np.random.randint(1, 10, size=(33, 1)),
        columns=["出现频率"],
        index=[f"{i}" for i in range(1, 34)]
    )
    st.bar_chart(chart_data, color="#ff5e62", height=200)
    st.caption("注：以上为红球历史热度趋势模拟图")

if __name__ == "__main__":
    main()