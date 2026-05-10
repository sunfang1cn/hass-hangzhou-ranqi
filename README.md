# Hangzhou Ranqi for Home Assistant

![Hangzhou Ranqi icon](custom_components/hangzhou_ranqi/brand/icon.png)

杭州燃气 Home Assistant 自定义集成，用于从杭州天然气有限公司线上服务接口获取每日燃气数据。

## 功能

- 通过 UI 配置用户编号和地址。
- 默认每 2 小时刷新一次数据。
- 提供两个传感器：
  - `燃气用量`：最新一天的燃气用量，单位 `m³`。
  - `当前读数`：最新一天的燃气表读数，单位 `m³`。
- 传感器属性包含日期、表号、地址和用户编号。

## 安装

### HACS

1. 在 HACS 中打开“自定义仓库”。
2. 添加本仓库地址，类别选择 `Integration`。
3. 安装 `Hangzhou Ranqi`。
4. 重启 Home Assistant。

### 手动安装

1. 将 `custom_components/hangzhou_ranqi` 复制到 Home Assistant 配置目录的 `custom_components/` 下。
2. 重启 Home Assistant。

## 配置

1. 打开 Home Assistant 的“设置” -> “设备与服务”。
2. 点击“添加集成”。
3. 搜索 `Hangzhou Ranqi` 或 `杭州燃气`。
4. 输入：
   - `用户编号`：杭州燃气用户编号，例如 `0023649600`。
   - `地址`：杭州燃气页面中的地址文本。

配置完成后，集成会自动获取用户对应的 NB 燃气表，并读取最近 7 天数据中的最新一天记录。

## 数据来源

本集成使用杭州天然气有限公司线上服务接口：

- 用户信息：`https://ht-service.hzgas.cn/OnlineService/transferSystem/userBaseInfo`
- 每日用量：`https://ht-service.hzgas.cn/OnlineService/transferSystem/queryMeterDate`



## 开发验证

```bash
python -m json.tool hacs.json
python -m json.tool custom_components/hangzhou_ranqi/manifest.json
python -m json.tool custom_components/hangzhou_ranqi/strings.json
python -m json.tool custom_components/hangzhou_ranqi/translations/zh-Hans.json
python -c "import pathlib; [compile(p.read_text(encoding='utf-8'), str(p), 'exec') for p in pathlib.Path('custom_components/hangzhou_ranqi').rglob('*.py')]; print('syntax ok')"
```

也可以使用随仓库提供的 GitHub Action 运行 HACS 校验。

## 免责声明

本项目不是杭州天然气有限公司的官方项目。接口和返回字段可能随官方服务变更而变化。
