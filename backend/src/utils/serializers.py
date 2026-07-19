from utils.dates import format_deadline


def serialize_task(task):
    if task is None:
        return None
    task = dict(task)
    task['deadline'] = format_deadline(task.get('deadline'))
    return task


def serialize_submission(submission):
    if submission is None:
        return None
    submission = dict(submission)
    if 'submitted_at' in submission:
        submission['submitted_at'] = format_deadline(submission['submitted_at'])
    return submission
