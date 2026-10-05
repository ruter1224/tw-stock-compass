# 台股價值投資分析

## 專案簡介
台股價值投資分析系統 — 分析台灣股票市場的價值投資標的，提供數據驅動的投資決策支援。

## 資料夾結構
```
台股價值投資分析/
├── AGENTS.md              # 專案設定與工作指引
├── .gitignore             # Git 忽略規則
├── .python-version        # Python 版本（3.12.10）
├── uv.lock                # uv 鎖定檔
├── pyproject.toml         # 專案設定與工具配置
├── pyrightconfig.json     # basedpyright 設定
├── handoff.md             # 跨 session / 跨機器交接檔
├── compass/               # 主程式碼
│   ├── auxiliary/         # 輔助工具（資產配置建議等）
│   ├── core/              # 核心領域邏輯（五大維度、目標 PE、安全圈）
│   ├── data/              # 資料存取與 API（MOPS、TWSE、cache）
│   ├── industry/          # 產業分析
│   ├── risk/              # 風險儀表板
│   ├── ui/                # Flet 桌面 UI
│   │   └── pages/         # 8 個頁面
│   └── main.py            # 程式入口
├── tests/                 # 測試（pytest）
└── 規格書/                 # 規格文件與參考資料
    ├── README.md
    ├── CHANGELOG.md
    ├── 開發規範.md
    └── *.pdf              # 投資策略參考資料
```

## Obsidian 同步
- 工作記錄：`SecondBrain/投資分析/台股價值投資分析.md`
- 專案每日紀錄：`SecondBrain/OpenCode專區/tw-stock-compass/`
- 投資知識庫：`SecondBrain/知識庫/`
- 每日記錄：`SecondBrain/每日筆記/`

## 開發環境
- Python 3.12.10
- 套件管理：uv
- UI 框架：flet >= 0.25.0（本機 venv 實際安裝 1.0.3）
- 資料：pandas、requests、FinMind
- 虛擬環境：`.venv/`（repo 相對路徑）

## 檢查命令

每次修改程式碼後，必須自動執行以下命令驗證：

```powershell
.venv\Scripts\ruff.exe check .
.venv\Scripts\pytest.exe -q
.venv\Scripts\python.exe -c "import compass.ui.app"
basedpyright
```

## 目前狀態

- [x] venv 重建並鎖定 Python 3.12.10（uv.lock / .python-version）
- [x] ruff 錯誤清零（line-length 調整為 120）
- [x] pyright 環境設定完成（pyrightconfig.json）
- [x] basedpyright 錯誤清零（49 → 0）
- [x] pytest 21 passed
- [x] UI import 驗證通過
- [ ] 視覺樣式確認（ElevatedButton → FilledButton）
- [ ] 未來評估：mops_api None→0.0 語意、外部 .date 使用處
