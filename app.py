"""Mumbai TransitLens - a beginner learning prototype.
ALL DATA IS SAMPLE / SIMULATED. This is NOT live Mumbai bus information."""

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Mumbai TransitLens", page_icon="🚌", layout="wide")

YELLOW, INK, RED, TEAL = "#F6B800", "#1B1F2A", "#C8102E", "#0E7C86"

# ---------- Custom CSS (colours inspired by Mumbai's black-and-yellow taxis and red buses) ----------
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700&display=swap');
h1, h2, h3 {{ font-family: 'Barlow Condensed', sans-serif !important; }}
.banner {{ background:{INK}; border-bottom:4px solid {YELLOW}; border-radius:10px;
          padding:14px 18px; margin-bottom:12px; }}
.banner h1 {{ color:#fff; margin:0; font-size:2.2rem; }}
.banner p {{ color:#D9DCE3; margin:4px 0 0; }}
.sample-tag {{ background:#FFF4CC; color:#6B4E00; border-left:5px solid {YELLOW};
              border-radius:6px; padding:8px 12px; font-size:0.9rem; margin-bottom:14px; }}
.card {{ background:#fff; color:{INK}; border-radius:10px; padding:14px 16px;
        border-left:6px solid {YELLOW}; box-shadow:0 1px 4px rgba(0,0,0,.15); margin-bottom:10px; }}
.card.red {{ border-left-color:{RED}; }}
.card.teal {{ border-left-color:{TEAL}; }}
.card .label {{ font-size:.85rem; color:#555; }}
.card .value {{ font-family:'Barlow Condensed',sans-serif; font-size:2.2rem; font-weight:700; line-height:1.1; }}
.card .note {{ font-size:.78rem; color:#777; }}
@media (max-width:640px) {{
  .banner h1 {{ font-size:1.7rem; }}
  .card .value {{ font-size:1.8rem; }}
}}
</style>
""", unsafe_allow_html=True)


def card(label, value, note, style=""):
    """Show one statistic card."""
    st.markdown(
        f'<div class="card {style}"><div class="label">{label}</div>'
        f'<div class="value">{value}</div><div class="note">{note}</div></div>',
        unsafe_allow_html=True,
    )


def go_to(page_name):
    """Button callback: switch the sidebar page."""
    st.session_state["page"] = page_name


def style_chart(fig):
    fig.update_layout(margin=dict(l=10, r=10, t=50, b=10), height=380)
    return fig


# ---------- Load the sample data ----------
data = pd.read_csv("sample_bus_data.csv")
data["period"] = data["hour"].apply(lambda h: "Peak" if h in [8, 9, 10, 17, 18, 19] else "Off-peak")

# ---------- Sidebar: navigation + filters ----------
PAGES = ["🏠 Home", "🛣️ Route Analysis", "👥 Passenger Demand",
         "⏱️ Delay Analysis", "🗂️ Data Explorer", "📘 About Project"]

st.sidebar.title("🚌 TransitLens")
page = st.sidebar.radio("Go to", PAGES, key="page")

st.sidebar.divider()
st.sidebar.subheader("Filters")
all_routes = sorted(data["route_id"].unique())
chosen_routes = st.sidebar.multiselect("Routes", all_routes, default=all_routes)
hour_range = st.sidebar.slider("Hours of the day", 6, 20, (6, 20))

df = data[data["route_id"].isin(chosen_routes) & data["hour"].between(hour_range[0], hour_range[1])]

# ---------- Header shown on every page ----------
st.markdown(
    '<div class="banner"><h1>Mumbai TransitLens</h1>'
    "<p>Public transport delay and passenger demand analyzer</p></div>"
    '<div class="sample-tag"><b>Sample data only.</b> Every number here is fictional and '
    "simulated for learning. This is not live Mumbai bus information.</div>",
    unsafe_allow_html=True,
)

# Stop early if filters leave nothing to show (the About page does not need data)
if df.empty and page != PAGES[5]:
    st.warning("No records match your filters. Pick at least one route in the sidebar.")
    st.stop()

# Summary tables used by several pages
route_stats = (df.groupby(["route_id", "route_name"], as_index=False)
                 .agg(avg_delay_min=("delay_min", "mean"),
                      avg_passengers=("passengers", "mean"),
                      trips=("record_id", "count"))
                 .round(1))
hourly = df.groupby(["hour", "period"], as_index=False)["passengers"].mean().round(1)

# ================= 1. HOME =================
if page == PAGES[0]:
    st.header("Dashboard")
    busiest_hour = int(hourly.loc[hourly["passengers"].idxmax(), "hour"])
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        card("Bus routes", df["route_id"].nunique(), "in the sample data")
    with c2:
        card("Average delay", f"{df['delay_min'].mean():.1f} min", "across all trips", "red")
    with c3:
        card("Passengers", f"{df['passengers'].sum():,}", "total in sample", "teal")
    with c4:
        card("Busiest hour", f"{busiest_hour}:00", "highest average load")

    st.subheader("Where to next?")
    b1, b2, b3 = st.columns(3)
    b1.button("Compare route delays", on_click=go_to, args=(PAGES[3],))
    b2.button("See busy hours", on_click=go_to, args=(PAGES[2],))
    b3.button("Learn about Hadoop", on_click=go_to, args=(PAGES[5],))
    st.caption("Tip: on a phone, open the sidebar with the arrow at the top left.")

# ================= 2. ROUTE ANALYSIS =================
elif page == PAGES[1]:
    st.header("Route analysis")
    st.dataframe(route_stats.sort_values("avg_delay_min", ascending=False),
                 hide_index=True, width="stretch")

    picked = st.selectbox("Look closer at one route", route_stats["route_id"])
    one = df[df["route_id"] == picked].sort_values("hour")
    fig = px.line(one, x="hour", y="delay_min", markers=True,
                  title=f"Delay by hour on {picked} (sample data)",
                  labels={"hour": "Hour of day", "delay_min": "Delay (minutes)"},
                  color_discrete_sequence=[RED])
    st.plotly_chart(style_chart(fig), width="stretch")

# ================= 3. PASSENGER DEMAND =================
elif page == PAGES[2]:
    st.header("Passenger demand")
    fig = px.bar(hourly, x="hour", y="passengers", color="period",
                 title="Average passengers per bus by hour (sample data)",
                 labels={"hour": "Hour of day", "passengers": "Avg passengers"},
                 color_discrete_map={"Peak": RED, "Off-peak": TEAL})
    st.plotly_chart(style_chart(fig), width="stretch")
    top = hourly.sort_values("passengers", ascending=False).head(3)["hour"].tolist()
    st.info(f"Busiest hours in this sample: {', '.join(str(h) + ':00' for h in top)}")

# ================= 4. DELAY ANALYSIS =================
elif page == PAGES[3]:
    st.header("Delay analysis")
    limit = st.slider("Flag routes with an average delay above (minutes)", 0, 20, 8)
    route_stats["status"] = route_stats["avg_delay_min"].apply(
        lambda d: "Above limit" if d > limit else "Within limit")
    fig = px.bar(route_stats.sort_values("avg_delay_min"), x="avg_delay_min", y="route_id",
                 orientation="h", color="status",
                 title="Average delay by route (sample data)",
                 labels={"avg_delay_min": "Avg delay (minutes)", "route_id": "Route"},
                 color_discrete_map={"Above limit": RED, "Within limit": TEAL})
    st.plotly_chart(style_chart(fig), width="stretch")

    late = route_stats[route_stats["status"] == "Above limit"]["route_id"].tolist()
    if late:
        st.warning("Above the limit: " + ", ".join(late))
    else:
        st.success("No route is above the limit.")

    by_period = df.groupby("period", as_index=False)["delay_min"].mean().round(1)
    fig2 = px.bar(by_period, x="period", y="delay_min", title="Peak vs off-peak delay",
                  labels={"delay_min": "Avg delay (minutes)", "period": ""},
                  color_discrete_sequence=[YELLOW])
    st.plotly_chart(style_chart(fig2), width="stretch")

# ================= 5. DATA EXPLORER =================
elif page == PAGES[4]:
    st.header("Data explorer")
    search = st.text_input("Search by route name (for example: Dadar)")
    shown = df[df["route_name"].str.contains(search, case=False)] if search else df
    st.write(f"Showing {len(shown)} of {len(data)} sample records")
    st.dataframe(shown, hide_index=True, width="stretch")
    st.download_button("Download this table as CSV", shown.to_csv(index=False),
                       file_name="sample_bus_data_filtered.csv", mime="text/csv")

# ================= 6. ABOUT =================
else:
    st.header("About this project")
    st.write(
        "Mumbai TransitLens is a student learning project. It shows how transport data "
        "(delays and passenger counts) can be summarised and charted with Python, Pandas, "
        "Plotly and Streamlit. The data is fictional, and the app does not connect to any "
        "real transport system."
    )

    st.subheader("Big Data ideas, in plain words")
    with st.expander("What is Hadoop?"):
        st.write("Hadoop is free software that lets many ordinary computers work together "
                 "on data that is too big for one computer.")
    with st.expander("What is HDFS?"):
        st.write("HDFS (Hadoop Distributed File System) is Hadoop's storage. It splits big "
                 "files into blocks and keeps copies on several machines, so the data "
                 "survives if one machine fails.")
    with st.expander("What is MapReduce?"):
        st.write("MapReduce is a way to process data in two steps. **Map** turns every record "
                 "into a (key, value) pair. **Reduce** combines all values that share a key.")
    with st.expander("Mapper and Reducer"):
        st.write("The *mapper* is the small function used in the Map step. The *reducer* is "
                 "the small function used in the Reduce step. Between them, Hadoop groups "
                 "the pairs by key (this is called the shuffle).")

    st.subheader("Illustrative example: average delay per route")
    st.caption("Illustrative only. This runs in plain Python on 9 sample rows. "
               "It does not use Hadoop or a cluster.")
    st.code(
        "def mapper(record):\n"
        "    return (record['route_id'], record['delay_min'])   # emit (key, value)\n\n"
        "def reducer(route_id, delays):\n"
        "    return (route_id, sum(delays) / len(delays))       # combine one key's values",
        language="python",
    )

    if st.button("Run the illustrative example"):
        rows = data.sample(9, random_state=1).to_dict("records")
        pairs = [(r["route_id"], r["delay_min"]) for r in rows]          # Map
        groups = {}
        for key, value in pairs:                                          # Shuffle
            groups.setdefault(key, []).append(value)
        results = [(k, round(sum(v) / len(v), 1)) for k, v in groups.items()]  # Reduce
        st.write("**1. Map:** each record becomes (route, delay)")
        st.write(pairs)
        st.write("**2. Shuffle:** pairs are grouped by route")
        st.write(groups)
        st.write("**3. Reduce:** each group becomes an average delay")
        st.write(dict(results))

    st.subheader("Limits of this prototype")
    st.write("Sample data only, no live feeds, no real Hadoop cluster, and no claim of "
             "accuracy for any real Mumbai route.")
