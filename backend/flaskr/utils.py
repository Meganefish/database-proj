# 用于生成关键词频率柱状图 HTML


def generate_bar_chart_html(labels, counts):
    from pyecharts.charts import Bar
    from pyecharts import options as opts

    bar = (
        Bar()
        .add_xaxis(list(labels))
        .add_yaxis("关键词", list(counts), category_gap="50%")
        .set_global_opts(
            title_opts=opts.TitleOpts(title="关键词频率分析", subtitle="前20项关键词"),
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=45)),
        )
    )
    return bar.dump_options_with_quotes()  # 导出为 JSON 字符串    #render_embed()

# 用于生成关键词平均薪资柱状图 HTML
def generate_salary_bar_chart_html(keywords, avg_salaries):
    from pyecharts.charts import Bar
    from pyecharts import options as opts

    bar = (
        Bar()
        .add_xaxis(list(keywords))
        .add_yaxis("平均薪资 (元/日)", list(avg_salaries), 
                   itemstyle_opts=opts.ItemStyleOpts(color="#FF7F0E"),  # 设置柱子的颜色为橙色
                   category_gap="50%")
        .set_global_opts(
            title_opts=opts.TitleOpts(title="关键词对应的平均薪资", subtitle="前20项关键词"),
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=45)),  # 旋转X轴标签，使其更易读
            yaxis_opts=opts.AxisOpts(name="平均薪资 (元/日)", 
                                      axislabel_opts=opts.LabelOpts(font_size=12))  # Y轴标签设置字体大小
        )
        .set_series_opts(
            label_opts=opts.LabelOpts(is_show=True, position="top", font_size=14, color="#333333")  # 显示数据标签，顶部显示，字体设置为清晰的颜色
        )
    )
    return bar.dump_options_with_quotes()  # 导出为 JSON 字符串 #render_embed()


# 用于生成饼图 HTML
def generate_pie_chart_html(labels, counts):
    from pyecharts.charts import Pie
    from pyecharts import options as opts

    pie = (
        Pie()
        .add(
            "关键词频率分布",
            [list(z) for z in zip(list(labels), list(counts))],
            radius=["30%", "70%"],
            rosetype="radius",
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="关键词频率分布（玫瑰饼图）"),
            legend_opts=opts.LegendOpts(is_show=False),
        )
        .set_series_opts(label_opts=opts.LabelOpts(is_show=True, formatter="{b}: {c}"))
    )
    return pie.dump_options_with_quotes()  # 导出为 JSON 字符串 #render_embed()
