from multiprocessing import Value, Process, Manager
import requests
from datetime import datetime, timedelta
from time import sleep
import json

def runInParallel(tasks):
    running_tasks = [Process(target=task["func"], args=task["args"]) for task in tasks]

    for running_task in running_tasks:
        running_task.start()
    for running_task in running_tasks:
        running_task.join()


def fetchThenAdd(catalogue, withinTimespan, author, page, timespanDays):    
    url = "https://api.github.com/search/commits"

    params = {
        "q": f"author:{author}",
        "sort": "committer-date",
        "order": "desc",
        "per_page": 100,
        "page": page
    }

    r = requests.get(url, params=params)
    obj = r.json()



    if not "items" in obj: # in case: API rate limit exceeded for [ip address], then try again 3 times with 2 seconds delay in between
        success = False
        for attempt in range(1,4):
            sleep(2)
            r = requests.get(url, params=params)
            obj = r.json()
            success = "items" in obj
            if success:
                break

        if not success:
            print(f"after {attempt+1} tries:", obj)
            withinTimespan.value = False
            return

    if not obj["items"]: # in case no results
        withinTimespan.value = False
        return



    for commit in obj["items"]:
        commitTime = datetime.fromisoformat( commit["commit"]["author"]["date"] )
        lastDatetimeToInclude = datetime.now(commitTime.tzinfo) - timedelta(days=timespanDays)
        
        if commitTime < lastDatetimeToInclude:
            withinTimespan.value = False
            return

        repo = commit["repository"]["name"]

        s = (commitTime - lastDatetimeToInclude).days / timespanDays 
        index = int(s * len(catalogue))

        if (len(catalogue) > 0):
            if (not repo in catalogue[index]):
                catalogue[index][repo] = 1
            else:
                catalogue[index][repo] += 1



divisor = {
    "day": 1,
    "week": 7,
    "month": 30,
    "year": 365
}

def getCommits(author="sharpness-b", setting="month", timespanDays=365):
    with Manager() as manager:
        
        catalogue = [manager.dict() for n in range( int( timespanDays/divisor[setting] ) )]
        
        withinTimespan = Value("i", True)

        page = 0
        while withinTimespan.value:
            tasks = [
                {"func": fetchThenAdd, "args": (catalogue, withinTimespan, author, page+1, timespanDays,)}, 
                {"func": fetchThenAdd, "args": (catalogue, withinTimespan, author, page+2, timespanDays,)}, 
                {"func": fetchThenAdd, "args": (catalogue, withinTimespan, author, page+3, timespanDays,)}
            ]

            runInParallel(tasks)

            page += len(tasks)

        return [dict(result) for result in catalogue]


if __name__ == '__main__':
    catalogue = getCommits()

    for n in catalogue:
        print(n)