# encoding: utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from bs4 import BeautifulSoup as bs
import urllib.request

from github_issue import make_github_issue
from config import NEW_SUB_URL, KEYWORD_LIST

def main():
    #change: iterate over sub url to search bothcond-mat and quant-ph
    keyword_list = KEYWORD_LIST
    keyword_dict = {key: [] for key in keyword_list}
    paper_dict = {} #key=paper_number, content=url,number,abstract,keywords,authors,..
        
    for sub_url in NEW_SUB_URL:
        page = urllib.request.urlopen(sub_url)
        soup = bs(page)
        content = soup.body.find("div", {'id': 'content'})

        issue_title = content.find("h3").text
        dt_list = content.dl.find_all("dt")
        dd_list = content.dl.find_all("dd")
        
        dt_list = content.find_all("dt")
        dd_list = content.find_all("dd")

        arxiv_base = "https://arxiv.org/abs/"

        assert len(dt_list) == len(dd_list)
        
        for i in range(len(dt_list)):
            # print('i=',i,'\n dt_list[i]=',dt_list[i].text)
            paper = {}
            # paper_number = dt_list[i].text.strip().split(" ")[2].split(":")[-1] ## old outdated version
            paper_number = dt_list[i].text.strip().split('\n')[2].strip() ## corrected version

            # paper_number = dt_list[i].text.strip().split(" ")[0].split(":")[-1] ##UNCOMMENT FOR CUSTOM DATE ARXIV SERACH
            paper['main_page'] = arxiv_base + paper_number
            paper['pdf'] = arxiv_base.replace('abs', 'pdf') + paper_number

            paper['title'] = dd_list[i].find("div", {"class": "list-title mathjax"}).text.replace("Title:", "").strip() ## corrected
            # if i<10:
            #     print('paper title is:',paper['title'])

            paper['authors'] = dd_list[i].find("div", {"class": "list-authors"}).text.replace("Authors:\n", "").replace(
                "\n", "").strip()
            paper['subjects'] = dd_list[i].find("div", {"class": "list-subjects"}).text.replace("Subjects: ", "").strip()
            paper['abstract'] = dd_list[i].find("p", {"class": "mathjax"}).text.replace("\n", " ").strip()

            #check if keywords are in paper
            for keyword in keyword_list:
                if keyword.lower() in paper['abstract'].lower() or keyword.lower() in paper['title'].lower():
                    #if it is, add paper to paper_dict if not already added. Otherwise, just add new keyword to paper entry
                    ## first check if paper is not added yet
                    if paper['main_page'] not in paper_dict:
                        # if its a new paper, add it to dict
                        paper['keyword']=[keyword]
                        # print('new paper found with keyword',paper['keyword'])
                        paper_dict[paper['main_page']] = paper
                    else:
                        # print('already added paper with second keyword',keyword)
                        paper_dict[paper['main_page']]['keyword'] = paper_dict[paper['main_page']]['keyword'] + [keyword]
                        # print('new keyword for this paper is:', paper_dict[paper['main_page']]['keyword'])
                    
                    # keyword_dict[keyword].append(paper)

    full_report = ''
    for paper in paper_dict.values():
        # print('first paper in paper_dict is\n',paper)
        full_report = full_report + f'## {paper["title"]}\n'
        full_report = full_report + '- **Keywords:** {}\n - **Authors:** {}\n - **Subjects:** {}\n - **Arxiv link:** {}\n - **Pdf link:** {}\n - **Abstract**\n {}\n' \
                .format(paper['keyword'], paper['authors'], paper['subjects'], paper['main_page'], paper['pdf'],paper['abstract'])

    # for keyword in keyword_list:
    #     full_report = full_report + '## Keyword: ' + keyword + '\n'

    #     if len(keyword_dict[keyword]) == 0:
    #         full_report = full_report + 'There is no result \n'

    #     for paper in keyword_dict[keyword]:
    #         report = '### {}\n - **Authors:** {}\n - **Subjects:** {}\n - **Arxiv link:** {}\n - **Pdf link:** {}\n - **Abstract**\n {}' \
    #             .format(paper['title'], paper['authors'], paper['subjects'], paper['main_page'], paper['pdf'],
    #                     paper['abstract'])
    #         full_report = full_report + report + '\n'

    print(full_report)
    make_github_issue(title=issue_title, body=full_report, labels=keyword_list)

if __name__ == '__main__':
    main()
