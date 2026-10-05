# 跨 Session / 跨機器交接檔

## ⏯️ 目前做到哪
本次完成 tw-stock-compass 專案的全面 lint / type 清理：
- ruff 錯誤從 67 → 0
- basedpyright 錯誤從 49 → 0
- pytest 維持 21 passed
- UI import 驗證通過

主要交付：
1. 修復全部 I001 / F401 import 問題（階段一）
2. 將 line-length 從 100 調到 120，手動拆分剩餘 6 個超長行
3. 新增 `pyrightconfig.json`，讓 basedpyright 正確使用 `.venv`
4. 修復 49 個 basedpyright 錯誤，包含：
   - `PriceZoneRange.excessive_low` 拼字修正為 `expensive_low`
   - `CatalystSignal.date` 重新命名為 `signal_date` 避免遮蔽內建 `date`
   - `mops_api.py` pandas `to_datetime` 與 `float(None)` 防護
   - UI 頁面 flet API 更新（ElevatedButton → FilledButton、DataColumn label=、page.window.width）
   - `allocation.py` 改用 `AssetAllocationAdvisor` 計算配置

## 🚦 目前狀態
- ✅ `ruff check .` 全綠
- ✅ `pytest -q` 21 passed
- ✅ `.venv\Scripts\python.exe -c "import compass.ui.app"` 正常
- ✅ `basedpyright` 0 errors, 0 warnings, 0 notes
- ✅ 28 個檔案已修改、1 個新檔案 `pyrightconfig.json` 待 commit

## ➡️ 下一步
1. commit + push 本次改動
2. 確認 UI 視覺樣式（ElevatedButton → FilledButton 的差異）
3. 評估 `mops_api.py` 中「無資料回傳 0.0」是否要區分「真實 0」與「資料缺失」
4. 檢查外部是否有使用 `CatalystSignal.date` 的遺漏處

## ⚠️ 注意事項
- `CatalystSignal` 欄位已從 `date` 改為 `signal_date`，外部腳本若使用 `.date` 會 AttributeError
- `ElevatedButton` 在 flet 1.0.3 不存在，已統一換成 `FilledButton`；視覺會從帶陰影變為實色
- git diff 對所有改動檔案發出 LF→CRLF 預告，屬 Windows git 正常提醒
- 本次未更新 Chezmoi

## 🕐 最後更新
- 時間：2026-10-05
- 更新者：OpenCode @ $env:COMPUTERNAME
- Git push：待推
- Chezmoi push：無變動
