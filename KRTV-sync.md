# KRTV 自动同步

- 来源：https://github.com/krtv322/kortv/blob/main/symftv.M3U
- 精确筛选分类：`🐉한국방송🦆`
- 输出分类统一改写为：`한국생방송`。
- 输出：仓库根目录 `KRTV.m3u`，保留原频道顺序、名称、图标及播放选项。
- 时间：北京时间每天 00:17、02:17、04:17、06:17、08:17、10:17、12:17、14:17、16:17、18:17、20:17、22:17。GitHub 调度可能延迟。
- 手动执行：Actions → Sync KRTV Korean channels → Run workflow。
- 下载失败、格式错误、分类不存在或选中频道缺少有效地址时，任务失败并保留原文件；内容相同不重复提交。
- 固定订阅地址：https://raw.githubusercontent.com/mjpark-dev/iptv/master/KRTV.m3u
- 同步只更新列表，不代理视频流，也不保证每个频道在所有网络上可播放。
- 公开仓库连续 60 天无活动时，GitHub 可能停用定时任务；可在 Actions 页面重新启用。

本项目的其他直播源文件不参与这个同步任务。
