import re
import collections

def find_subjects(text):
    return [ (m.group(1).decode('utf8'), m.start()) for m in re.finditer('<b>([^<]+?): </b>', text) ]

def find_marks(text):
    return [ (m.group(3), m.start()) for m in re.finditer('href="/mobile/oceny/(.+?)"( *)>(.*?)</a>', text) ]

def get_marks(text):
    subj = list(find_subjects(text))
    subj.reverse()
    marks = list(find_marks(text))
    marks.reverse()
    subjects = collections.defaultdict(list)
    
    while subj:
        subj_name, subj_i = subj.pop()
        subj_list = []
        while marks:
            mark_name, mark_i = marks[-1]
            if subj and subj[-1][1] < mark_i:
                break
            marks.pop()
            subjects[subj_name].append(mark_name)
            #print subj_name, mark_name
    return dict(subjects)

if __name__ == '__main__':
    import sys, pprint
    t = sys.stdin.read()
    pprint.pprint(get_marks(t))