from __future__ import annotations

from _tasks import load_task_catalog


def main() -> None:
    tasks = load_task_catalog()
    if not tasks:
        print("No tasks found.")
        return

    for task in tasks:
        source = task.source or "-"
        print(
            f"{task.task_id:<28} "
            f"{task.objective:<8} "
            f"{task.primary_metric:<16} "
            f"{source}"
        )


if __name__ == "__main__":
    main()
