from io import TextIOWrapper
import plotly.express as px
import plotly.graph_objects as go
import plotly as plt
import pandas as pd


class process:
    def __init__(self, s: str) -> None:
        splited = s.strip().split()
        self.pid = splited[0]
        self.command = splited[-1]
        self.virt = self.parse_top_format(splited[4])
        self.rss = self.parse_top_format(splited[5])

    def __str__(self) -> str:
        return self.pid

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, process):
            return self.pid == __value.pid
        return False

    def __hash__(self) -> int:
        return hash(pid)

    @staticmethod
    def parse_top_format(s: str):
        if s[-1] == "g":
            return float(s[:-1])
        return float(s) / 1000


def parse_mem(s: str):
    splited = s.strip().split()
    free = float(splited[5])
    used = float(splited[7])
    return (free, used)


def parse_swap(s: str):
    splited = s.strip().split()
    free = float(splited[4])
    used = float(splited[6])
    return (free, used)


def read_one_iter(file: TextIOWrapper):
    if not len(file.readline()):
        return None

    _ = file.readline()
    _ = file.readline()
    mem = parse_mem(file.readline())
    swap = parse_swap(file.readline())
    _ = file.readline()
    _ = file.readline()
    processes = [process(file.readline()) for _ in range(5)]

    return (processes, mem, swap)


data = []
with open("mem.stat") as file:
    pid = file.readline()

    res = read_one_iter(file)
    while res:
        data.append(res)
        res = read_one_iter(file)

x = [10 * i for i in range(len(data))]

fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x=x,
        y=[processes[0].virt for (processes, _, _) in data],
        name="virt",
    )
)
fig.add_trace(
    go.Scatter(
        x=x,
        y=[processes[0].rss for (processes, _, _) in data],
        name="rss",
    )
)
fig.add_trace(
    go.Scatter(
        x=x,
        y=[mem_used for (_, (_, mem_used), _) in data],
        name="mem",
    )
)
fig.add_trace(
    go.Scatter(
        x=x,
        y=[swap_used for (_, _, (_, swap_used)) in data],
        name="swap",
    )
)
fig.update_layout(
    xaxis_title="Seconds",
    yaxis_title="MB",
    font=dict(family="Courier New, monospace", size=18, color="RebeccaPurple"),
).show()


# top 5

d = []
for i, (processes, _, _) in enumerate(data):
    for p in processes:
        d.append(
            dict(pid_command=f"[{p.pid}] {p.command}", start=i * 10, end=i * 10 + 11)
        )
df = pd.DataFrame(d)

df["delta"] = df["end"] - df["start"]
fig = px.timeline(
    df, x_start="start", x_end="end", y="pid_command", color="pid_command"
)
fig.layout.xaxis.type = "linear"
for i in range(len(fig.data)):
    fig.data[i].x = df.delta.tolist()

fig.update_layout(
    xaxis_title="Seconds",
    font=dict(family="Courier New, monospace", size=18, color="RebeccaPurple"),
).show()
