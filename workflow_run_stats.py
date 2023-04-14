from github import Github


g = Github("<access token here>")


print(list(g.get_organization("ivelum").get_repos()))

repo = g.get_organization("ivelum").get_repo("teamplify")


for workflow_run in repo.get_workflow_runs(status="success")[:40]:
    print(f"{workflow_run.id} {workflow_run.status} {workflow_run.conclusion}")
    print(workflow_run.timing())
