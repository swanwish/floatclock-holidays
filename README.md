# FloatClock Holidays

[FloatClock](https://github.com/swanwish/floatclock) 的节假日数据订阅源。

App 启动时会从这里拉取 `manifest.json`，按需下载启用的区域文件。**完全离线**的用户可以在偏好设置里关闭自动更新。

## 仓库结构

```
.
├── manifest.json                    # 顶层索引，App 拉这一个文件就知道一切
├── regions/
│   ├── cn-statutory/                # 中国大陆法定节假日
│   │   ├── holidays-2026.fch
│   │   └── holidays-2027.fch
│   ├── cn-gis-school/               # 国际学校校历（示例）
│   └── ...                          # 添加新区域：建文件夹 + manifest 注册
├── scripts/
│   └── update-manifest.py           # 重生成 manifest.json（计算 sha256）
└── README.md
```

## 数据格式（`.fch`）

JSON，schema 详见 [FloatClock 主仓库](https://github.com/swanwish/floatclock) 的 `HolidayFile.swift`。最小例子：

```json
{
  "schema": "floatclock.holidays/v4",
  "source": "cn-statutory",
  "year": 2026,
  "locale": "zh-CN",
  "entries": [
    {"name": "元旦", "type": "off", "start": "2026-01-01"},
    {"name": "春节", "type": "off", "start": "2026-02-16", "end": "2026-02-22"},
    {"name": "春节调休", "type": "workday", "dates": ["2026-02-14", "2026-02-28"]}
  ]
}
```

支持三种条目格式（任选其一）：

- `start` only — 单天
- `start` + `end` — 连续多天范围
- `dates: [...]` — 非连续日期列表（适合调休）

## 添加新数据

### 新增某区域的某年

1. 把 `.fch` 文件放到 `regions/{region-id}/holidays-{year}.fch`
2. 跑 `python3 scripts/update-manifest.py`
3. 提交 PR

### 新增一个区域

1. 在 `regions/` 下建文件夹（命名规范：`{locale}-{type}`，如 `us-federal`、`hk-statutory`、`cn-gis-school`）
2. 放入至少一年的 `holidays-{year}.fch`
3. 编辑 `scripts/update-manifest.py` 在 `REGIONS_META` 字典里加该区域的元信息
4. 跑 `python3 scripts/update-manifest.py`
5. 提交 PR

## 校验

每个文件的 `sha256` 在 `manifest.json` 里。App 下载后会校验，不一致则丢弃。

## License

MIT（数据本身是公开信息）。
