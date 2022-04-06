import matplotlib.pyplot as plt
from github import divisor



def formatCatalogue(catalogue):
    # fill with 0
    repos = set([repo for sub in [vertical.keys() for vertical in catalogue] for repo in sub])
    values = {repo: [(i,0) for i in range(len(catalogue))] for repo in repos}

    # fill with values
    for i, vertical in enumerate(catalogue):
        for repo in vertical:
            values[repo][i] = (i, vertical[repo])
            
    return values



def plotCommits(catalogue, withinTimespan, setting, author):

    values = formatCatalogue(catalogue)
    for repo in values:
    #Plot a line graph
        points = values[repo]
        plt.plot([p[0] for p in points], [p[1] for p in points], label=repo)
    
    # Add labels and title
    plt.title(f"Commits by {author} last {withinTimespan} days")
    # plt.xlabel("X-axis")
    ax = plt.gca()
    ax.axes.xaxis.set_visible(False)
    plt.ylabel("Commits")
    
    plt.legend()
    plt.show()
        
        

if __name__ == '__main__':
    catalogue = [ {'Advancer': 5}, {}, {}, {'Advancer': 9}, {}, {'linked-practice': 19, 'sharpness-b': 3}, {'Advancer-2.0': 45}, {}, {}, {'sharpness-b': 17, 'quizzes-practice-app': 13}, {'unknown-source': 52, 'sharpness-b': 4, 'Advancer-2.0': 1, 'Advancer': 1}, {'bjergstedblaseensemble.no': 35, 'quick-git': 13}]

    plotCommits(catalogue, 365, "month", "sharpness-b")