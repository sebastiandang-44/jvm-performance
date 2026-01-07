import json
import zstandard as zstd
import io
from datetime import datetime
import pandas as pd
import dash
from dash import dcc, html
import plotly.express as px
import plotly.graph_objects as go


event_log_path = "events_1_app-20260107064307-0009.zstd"


task_data = []

with open(event_log_path, "rb") as f:
    dctx = zstd.ZstdDecompressor()
    stream_reader = dctx.stream_reader(f)
    text_stream = io.TextIOWrapper(stream_reader, encoding="utf-8")

    for line in text_stream:
        try:
            event = json.loads(line)
            if event['Event'] in ['SparkListenerTaskStart', 'SparkListenerTaskEnd']:
                task_info = event['Task Info']
                task_data.append({
                    "task_id": task_info.get('Task ID', -1),
                    "stage_id": event.get('Stage ID', -1),
                    "event": event['Event'],
                    "launch_time": task_info.get('Launch Time', None),
                    "finish_time": task_info.get('Finish Time', None)
                })
        except json.JSONDecodeError:
            continue

df_tasks = pd.DataFrame(task_data)

# -------------------------------
# 3️⃣ Compute Task Durations
# -------------------------------
# Task execution time in milliseconds
df_tasks['exec_time_ms'] = df_tasks['finish_time'] - df_tasks['launch_time']

# Group by stage for stage metrics
stage_metrics = df_tasks.groupby('stage_id').agg(
    stage_start=pd.NamedAgg(column='launch_time', aggfunc='min'),
    stage_end=pd.NamedAgg(column='finish_time', aggfunc='max'),
    task_avg=pd.NamedAgg(column='exec_time_ms', aggfunc='mean'),
    task_max=pd.NamedAgg(column='exec_time_ms', aggfunc='max')
).reset_index()

stage_metrics['stage_duration_ms'] = stage_metrics['stage_end'] - stage_metrics['stage_start']
stage_metrics['stage_start_time'] = pd.to_datetime(stage_metrics['stage_start'], unit='ms')
stage_metrics['stage_end_time'] = pd.to_datetime(stage_metrics['stage_end'], unit='ms')

# Total job execution time
job_start = stage_metrics['stage_start'].min()
job_end = stage_metrics['stage_end'].max()
total_job_time = job_end - job_start  # in ms

print(f"Total Job Execution Time: {total_job_time} ms")

# -------------------------------
# 4️⃣ Dash App with Charts
# -------------------------------
app = dash.Dash(__name__)

# Chart 1: Stage Execution Time (ms)
fig_stage = px.bar(stage_metrics, x='stage_id', y='stage_duration_ms',
                   title='Stage Execution Time (ms)',
                   labels={'stage_id': 'Stage ID', 'stage_duration_ms': 'Duration (ms)'})

# Chart 2: Task Duration (avg / max)
fig_task = go.Figure()
fig_task.add_trace(go.Bar(
    x=stage_metrics['stage_id'],
    y=stage_metrics['task_avg'],
    name='Average Task Duration (ms)'
))
fig_task.add_trace(go.Bar(
    x=stage_metrics['stage_id'],
    y=stage_metrics['task_max'],
    name='Max Task Duration (ms)'
))
fig_task.update_layout(title="Task Duration per Stage", barmode='group',
                       xaxis_title="Stage ID", yaxis_title="Time (ms)")

# Chart 3: Total Job Execution Time (single value)
fig_job = go.Figure()
fig_job.add_trace(go.Indicator(
    mode="number",
    value=total_job_time,
    title={"text": "Total Job Execution Time (ms)"}
))

# Layout
app.layout = html.Div([
    html.H1("Spark Execution Metrics"),
    html.H3("Total Job Execution Time"),
    dcc.Graph(figure=fig_job),
    html.H3("Stage Execution Time"),
    dcc.Graph(figure=fig_stage),
    html.H3("Task Duration per Stage (avg / max)"),
    dcc.Graph(figure=fig_task)
])

if __name__ == "__main__":
    app.run(debug=True)
