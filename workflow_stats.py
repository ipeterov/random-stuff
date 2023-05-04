from collections import defaultdict
import matplotlib.pyplot as plt
from github import Github
from matplotlib.ticker import MultipleLocator, FuncFormatter

GITHUB_TOKEN = "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"
g = Github(GITHUB_TOKEN)

ORGANIZATION = "ivelum"
REPOSITORY = "teamplify"
START_WORKFLOW = "test.yaml"
END_WORKFLOW = "deploy.yaml"
LAST_N_RUNS = 50


def get_time_series():
    repo = g.get_organization(ORGANIZATION).get_repo(REPOSITORY)

    runs_by_sha = defaultdict(lambda: dict(workflow_names=[], start=None, end=None))
    for workflow_name in [START_WORKFLOW, END_WORKFLOW]:
        workflow = repo.get_workflow(workflow_name)

        all_runs = iter(workflow.get_runs(status="completed"))

        for _ in range(LAST_N_RUNS):
            workflow_run = next(all_runs)

            if workflow_run.status != "completed":
                continue

            if workflow_run.conclusion != "success":
                continue

            stats = runs_by_sha[workflow_run.head_sha]

            stats["workflow_names"].append(workflow_name)

            if not stats["start"] or stats["start"] > workflow_run.created_at:
                stats["start"] = workflow_run.created_at

            if not stats["end"] or stats["end"] < workflow_run.updated_at:
                stats["end"] = workflow_run.updated_at

    with_start_and_end = [
        stats
        for stats in runs_by_sha.values()
        if set(stats["workflow_names"]) == {START_WORKFLOW, END_WORKFLOW}
    ]
    by_start = sorted(with_start_and_end, key=lambda stats: stats["start"])

    starts = []
    durations = []
    for stats in by_start:
        starts.append(stats["start"].strftime("%-dth\n%H:%M"))
        duration = stats["end"] - stats["start"]
        durations.append(duration.seconds)

    return starts, durations


def format_seconds(total_seconds, position=None):
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    return f"{minutes:.0f}:{seconds:02.0f}"


if __name__ == "__main__":
    plt.style.use("seaborn-v0_8")

    starts, durations = get_time_series()

    ax = plt.subplot()
    bars = ax.bar(starts, durations)
    ax.bar_label(bars, labels=[format_seconds(duration) for duration in durations])
    ax.yaxis.set_major_locator(MultipleLocator(base=60))
    ax.yaxis.set_major_formatter(FuncFormatter(format_seconds))
    ax.set_ylim(bottom=0)
    plt.show()
