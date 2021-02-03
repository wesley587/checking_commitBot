import github
from time import sleep

g = github.Github('10e9464aef4e42ebb72b80402ff926c3b78b9fb7')
count = 0
sha = ''
while True:
    teste_repos = g.get_repo('f0rbid3n/testing')
    parsing = teste_repos.get_branch('main').commit
    body = parsing.raw_data
    if count == 0:
        sha = body['sha']
        print(body)
    else:
        if body['sha'] != sha:
            sha = body['sha']
            base = body['files']
            if len(base) > 1:
                for k in body['files'][:]:
                    print(k['filename'])
            else:
                print(base[0]['filename'])
    count += 1
    sleep(10)
