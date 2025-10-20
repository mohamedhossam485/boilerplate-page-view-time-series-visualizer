import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import calendar

# ---------- Load & clean data ----------
# Read csv and set date as index (parsed as datetime)
df = pd.read_csv("fcc-forum-pageviews.csv", parse_dates=["date"], index_col="date")

# Filter out bottom 2.5% and top 2.5%
low, high = df["value"].quantile([0.025, 0.975])
df = df[(df["value"] >= low) & (df["value"] <= high)]


def draw_line_plot():
    """
    Line chart: Daily page views
    Title: Daily freeCodeCamp Forum Page Views 5/2016-12/2019
    x: Date, y: Page Views
    """
    df_line = df.copy()

    fig, ax = plt.subplots(figsize=(15, 5))
    ax.plot(df_line.index, df_line["value"])
    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")

    fig.savefig("line_plot.png")
    return fig


def draw_bar_plot():
    """
    Bar chart: average daily page views for each month grouped by year
    Legend title: Months | x: Years | y: Average Page Views
    """
    df_bar = df.copy()
    # Add year & month name
    df_bar["year"] = df_bar.index.year
    df_bar["month"] = df_bar.index.month

    # Pivot: rows=year, cols=month (ordered Jan..Dec), values=mean page views
    month_order = list(range(1, 13))
    table = (
        df_bar.pivot_table(
            values="value", index="year", columns="month", aggfunc="mean"
        )[month_order]
        .rename(columns={m: calendar.month_name[m] for m in month_order})
    )

    fig = table.plot(kind="bar", figsize=(12, 8)).get_figure()
    plt.xlabel("Years")
    plt.ylabel("Average Page Views")
    plt.legend(title="Months")

    fig.savefig("bar_plot.png")
    return fig


def draw_box_plot():
    """
    Two adjacent box plots:
    1) Year-wise Box Plot (Trend)
    2) Month-wise Box Plot (Seasonality) with Jan..Dec order
    """
    # Prepare data for box plots
    df_box = df.copy().reset_index()
    df_box["year"] = df_box["date"].dt.year
    df_box["month"] = df_box["date"].dt.strftime("%b")  # Jan, Feb, ...
    month_abbr_order = list(calendar.month_abbr)[1:]  # ['Jan', ... , 'Dec']

    # Draw the two plots
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))

    # Year-wise
    sns.boxplot(ax=axes[0], data=df_box, x="year", y="value")
    axes[0].set_title("Year-wise Box Plot (Trend)")
    axes[0].set_xlabel("Year")
    axes[0].set_ylabel("Page Views")

    # Month-wise (ordered)
    sns.boxplot(
        ax=axes[1],
        data=df_box,
        x="month",
        y="value",
        order=month_abbr_order,
    )
    axes[1].set_title("Month-wise Box Plot (Seasonality)")
    axes[1].set_xlabel("Month")
    axes[1].set_ylabel("Page Views")

    fig.savefig("box_plot.png")
    return fig
