import streamlit as st
import streamlit.components.v1 as components

# 页面基础配置：全宽无侧栏沉浸式展现
st.set_page_config(
    page_title="Gestalt Circle - 完形错觉之圆",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 隐藏 Streamlit 默认的白边和导航外框
st.markdown("""
    <style>
        .block-container {
            padding: 0rem !important;
            margin: 0rem !important;
            max-width: 100% !important;
        }
        header {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# 嵌入 0 警告、带三语切换与 8 三角形负空间错觉的前端代码
gestalt_html_code = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>The Illusory Circle - 完形错觉之圆</title>
    <style>
        * {
            box-sizing: border-box;
            user-select: none;
            margin: 0;
            padding: 0;
        }

        body {
            background-color: #0e1117;
            color: #ffffff;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Microsoft YaHei", "Malgun Gothic", sans-serif;
            overflow: hidden;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            width: 100vw;
        }

        canvas {
            display: block;
            background-color: #0e1117;
        }

        .ui-container {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
        }

        .header-box {
            position: absolute;
            top: 28px;
            left: 28px;
            max-width: 520px;
        }

        .title {
            font-size: 19px;
            font-weight: 600;
            color: #f3f4f6;
            margin-bottom: 8px;
            letter-spacing: 1px;
        }

        .philosophy-text {
            font-size: 14px;
            line-height: 1.6;
            color: #9ca3af;
        }

        .controls-box {
            position: absolute;
            top: 28px;
            right: 28px;
            display: flex;
            flex-direction: column;
            align-items: flex-end;
            gap: 12px;
            pointer-events: auto;
        }

        .lang-group {
            display: flex;
            gap: 6px;
        }

        button {
            border: 1px solid #4b5563;
            background-color: #1f2937;
            color: #9ca3af;
            border-radius: 6px;
            padding: 6px 14px;
            font-size: 13px;
            cursor: pointer;
            transition: all 0.15s ease;
        }

        button:hover {
            background-color: #374151;
            color: #f3f4f6;
        }

        button.active {
            background-color: #2563eb;
            border-color: #60a5fa;
            color: #ffffff;
        }

        .btn-action {
            background-color: rgba(31, 41, 55, 0.85);
            backdrop-filter: blur(8px);
            border: 1px solid #4b5563;
            color: #e5e7eb;
            padding: 8px 18px;
            font-weight: 500;
        }

        .btn-action:hover {
            background-color: #374151;
            border-color: #9ca3af;
            color: #ffffff;
        }

        .btn-action[data-active="true"] {
            background-color: #b91c1c;
            border-color: #ef4444;
            color: #ffffff;
        }
    </style>
</head>
<body>

<canvas id="stage"></canvas>

<div class="ui-container">
    <div class="header-box">
        <div id="uiTitle" class="title">格式塔之圆：被心智补完的虚无</div>
        <div id="uiDesc" class="philosophy-text">
            “屏幕上没有画过任何一条封闭轮廓。向外辐射的星芒基底被一道弧线所截断，观者的心智自发构筑出了这个挡在光芒前方的‘虚幻实体之圆’。”
        </div>
    </div>

    <div class="controls-box">
        <div class="lang-group">
            <button id="btnZh" class="active" onclick="switchLang('zh')">中文</button>
            <button id="btnEn" onclick="switchLang('en')">EN</button>
            <button id="btnKo" onclick="switchLang('ko')">한국어</button>
        </div>
        <button id="btnAction" class="btn-action" data-active="false" onclick="toggleDisplay()">展示</button>
    </div>
</div>

<script>
    const canvas = document.getElementById("stage");
    const ctx = canvas.getContext("2d");

    let width = window.innerWidth;
    let height = window.innerHeight;
    canvas.width = width;
    canvas.height = height;

    window.addEventListener("resize", () => {
        width = window.innerWidth;
        height = window.innerHeight;
        canvas.width = width;
        canvas.height = height;
    });

    // noinspection SpellCheckingInspection
    const texts = {
        zh: {
            title: "格式塔之圆：被心智补完的虚无",
            desc: "“屏幕上没有画过任何一条封闭轮廓。向外辐射的星芒基底被一道弧线所截断，观者的心智自发构筑出了这个挡在光芒前方的‘虚幻实体之圆’。”",
            btnShow: "展示",
            btnReset: "复原"
        },
        en: {
            title: "Gestalt Circle: Void Completed by Mind",
            desc: "'Not a single closed contour is drawn. Radiating starbursts are truncated at the core, leading your mind to construct an illusory disc eclipsing the rays.'",
            btnShow: "Show",
            btnReset: "Restore"
        },
        ko: {
            title: "게슈탈트의 원: 마음이 완성한 허무",
            desc: "'화면에는 단 하나의 닫힌 윤곽선도 없습니다. 바깥으로 방사되는 광선들이 중앙에서 잘려 나가며, 뇌는 광선을 가로막는 보이지 않는 원형 디스크를 스스로 완성합니다.'",
            btnShow: "표시",
            btnReset: "복원"
        }
    };

    let currentLang = "zh";
    let isShowingCircle = false;

    function updateActionBtn() {
        const t = texts[currentLang];
        const btn = document.getElementById("btnAction");
        if (isShowingCircle) {
            btn.innerText = t.btnReset;
            btn.setAttribute("data-active", "true");
        } else {
            btn.innerText = t.btnShow;
            btn.setAttribute("data-active", "false");
        }
    }

    function switchLang(lang) {
        currentLang = lang;
        const t = texts[lang];
        document.getElementById("uiTitle").innerText = t.title;
        document.getElementById("uiDesc").innerText = t.desc;
        updateActionBtn();

        document.getElementById("btnZh").className = lang === "zh" ? "active" : "";
        document.getElementById("btnEn").className = lang === "en" ? "active" : "";
        document.getElementById("btnKo").className = lang === "ko" ? "active" : "";
    }

    function toggleDisplay() {
        isShowingCircle = !isShowingCircle;
        updateActionBtn();
    }

    const NUM_TRIANGLES = 8;

    function draw() {
        ctx.fillStyle = "#0e1117";
        ctx.fillRect(0, 0, width, height);

        const cx = width / 2;
        const cy = height / 2;

        const illusoryRadius = Math.min(width, height) * 0.22;
        const triHeight = illusoryRadius * 0.95;
        const halfBase = illusoryRadius * 0.32;

        const baseDist = illusoryRadius * 0.70;
        const tipDist = baseDist + triHeight;

        for (let i = 0; i < NUM_TRIANGLES; i++) {
            const angle = (i * 2 * Math.PI) / NUM_TRIANGLES;
            const cos = Math.cos(angle);
            const sin = Math.sin(angle);

            const perpX = -sin;
            const perpY = cos;

            const tipX = cx + cos * tipDist;
            const tipY = cy + sin * tipDist;

            const baseMidX = cx + cos * baseDist;
            const baseMidY = cy + sin * baseDist;

            const corner1X = baseMidX + perpX * halfBase;
            const corner1Y = baseMidY + perpY * halfBase;

            const corner2X = baseMidX - perpX * halfBase;
            const corner2Y = baseMidY - perpY * halfBase;

            ctx.beginPath();
            ctx.moveTo(tipX, tipY);
            ctx.lineTo(corner1X, corner1Y);
            ctx.lineTo(corner2X, corner2Y);
            ctx.closePath();

            ctx.fillStyle = "#f1f5f9";
            ctx.fill();
        }

        ctx.beginPath();
        ctx.arc(cx, cy, illusoryRadius, 0, Math.PI * 2);
        ctx.fillStyle = "#0e1117";
        ctx.fill();

        if (isShowingCircle) {
            ctx.beginPath();
            ctx.arc(cx, cy, illusoryRadius, 0, Math.PI * 2);
            ctx.strokeStyle = "#ef4444";
            ctx.lineWidth = 2.5;
            ctx.stroke();
        }

        requestAnimationFrame(draw);
    }

    requestAnimationFrame(draw);
</script>
</body>
</html>
"""

# 将纯前端 Canvas 渲染到页面，高度设为 920px
components.html(gestalt_html_code, height=920, scrolling=False)