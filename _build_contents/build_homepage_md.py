import math
import os
from collections import defaultdict
import re
from datetime import datetime
from typing import List

import gspread
import pandas as pd
from gspread import Spreadsheet


def get_tab_df(sheet: Spreadsheet, sheet_path_list: List[str], tab_name) -> pd.DataFrame:
    for sheet_path in sheet_path_list:
        try:
            df = pd.read_excel(sheet_path, tab_name)
            return df.fillna("")
        except FileNotFoundError:
            pass
    else:
        return pd.DataFrame(sheet.worksheet(tab_name).get_all_records())


def _build_md_files(sheet: Spreadsheet, sheet_path_list: List[str], name: str, output_dir):
    tab = get_tab_df(sheet, sheet_path_list, name)

    def kv_escape(k, v):
        if "'" not in str(v):
            return f"{k}: '{v}'"
        else:
            return f'{k}: "{v}"'

    for i, r in tab.iterrows():
        ym = re.compile(r"\d\d\d\d-\d\d").search(r.date).group()
        try:
            sv = re.compile(r"\((.*?)\)").search(r.venue).group(1)
        except AttributeError:
            sv = r.venue
        file_name = f"{ym}-{sv.replace(' ', '-').replace('/', '').lower()}.md"
        file_path = os.path.join(output_dir, file_name)

        kv = [f"{kv_escape(k, v)}\n" for k, v in r.items() if k != "contents" and not k.endswith("url")]
        urls = [f"{k}: '{v}'\n" for k, v in r.items() if k.endswith("url") and v != ""]
        lines = ["---\n", *kv, *urls, "---\n\n"]
        if hasattr(r, "contents"):
            lines.append(r.contents)
        with open(file_path, "w") as f:
            f.writelines(lines)
            print("".join(lines))
            print(f"Saved at {file_path}")

def _build_md_files_2(sheet: Spreadsheet, sheet_path_list: List[str], name: str, output_dir):
    tab = get_tab_df(sheet, sheet_path_list, name)

    for i, r in tab.iterrows():
        ym_match = re.search(r"\d\d\d\d-\d\d", str(r.date))
        if not ym_match:
            continue
        ym = ym_match.group()

        full_date = datetime.strptime(str(r.date), "%Y-%m-%d").date()

        date_snippet = str(r.date).replace("-", "")
        file_name = f"{date_snippet}.md"
        file_path = os.path.join(output_dir, file_name)

        # front matter
        front_matter = [
            "---\n",
            f"title: \"{r.title}\"\n",
            f"date: {full_date}\n",
            f"layout: post\n",
            f"permalink: /news/{date_snippet}\n",
            "---\n\n"
        ]

        # 본문
        body = f"{r.title}\n"

        # 파일 쓰기
        with open(file_path, "w") as f:
            f.writelines(front_matter)
            f.write(body)
            print(f"Saved at {file_path}")



def build_publications(sheet: Spreadsheet, sheet_path_list: List[str],
                       output_dir="./_publications/"):
    _build_md_files(sheet, sheet_path_list, "publications", output_dir)

def build_latest_news(sheet: Spreadsheet, sheet_path_list: List[str],
                       output_dir="./_news/"):
    _build_md_files_2(sheet, sheet_path_list, "latest news", output_dir)


def build_talks(sheet: Spreadsheet, sheet_path_list: List[str],
                output_dir="./_talks/"):
    _build_md_files(sheet, sheet_path_list, "talks", output_dir)

def build_about(sheet: Spreadsheet, sheet_path_list: List[str],
                out_dir="./_pages/about.md"):

    def _education(df: pd.DataFrame):
        for i, r in df.iterrows():
            dobj = datetime.strptime(r.date, "%Y-%m-%d")
            lines.append(f"- {r.degree}, *{r.institution}*, {dobj.strftime('%b %Y')}\n")
            if len(r.bullets) > 1:
                lines.append(f"  - {r.bullets}\n")       

    def _academic_services(df: pd.DataFrame):
        position_and_org_to_rs = defaultdict(lambda: defaultdict(list))
        for i, r in df.iterrows():
            position_and_org_to_rs[r.position][r.organization].append(r)
        for p, o_to_rs in position_and_org_to_rs.items():
            _o_ys = []
            for o, rs in o_to_rs.items():
                _years = [f"{r.year}" if r.url == "" else f"[{r.year}]({r.url})" for r in rs]
                _o_ys.append(f"{o} ({', '.join(_years)})")
            lines.append(f"- {p}: {', '.join(_o_ys)}\n")

    def _teaching_experiences(df: pd.DataFrame):
        course_to_rs = defaultdict(list)
        for i, r in df.iterrows():
            course_to_rs[r.course].append(r)
        for c, rs in course_to_rs.items():
            positions = [r.position for r in rs]
            positions = set(positions) if len(set(positions)) == 1 else positions
            head = ", ".join(positions)
            semesters = ", ".join(f"{r.semester}" if r.url == "" else f"[{r.semester}]({r.url})" for r in rs)
            notes = ", ".join(r.note for r in rs if r.note != "")
            if notes == "":
                lines.append(f"- {head} of {c} ({semesters})\n")
            else:
                lines.append(f"- {head} of {c} ({semesters}), *{notes}*\n")

    def _honors(df: pd.DataFrame):
        for i, r in df.iterrows():
            dobj = datetime.strptime(r.date, "%Y-%m-%d")
            if r.url == "":
                lines.append(f"- {r.title}, *{r.organization}*, {dobj.strftime('%Y')}\n")
            else:
                lines.append(f"- [{r.title}]({r.url}), *{r.organization}*, {dobj.strftime('%Y')}\n")
    
    def _latest_news(df: pd.DataFrame):
        for i, r in df.iterrows():
            dobj = datetime.strptime(r.date, "%Y-%m-%d")
            lines.append(f"- {dobj.strftime('%b %Y')}: {r.title} \n")

    def _open_source_contributions(df: pd.DataFrame):
        for i, r in df.iterrows():
            lines.append(f"- [{r.title}]({r.url})\n")

    lines = []

    # about = pd.DataFrame(sheet.worksheet("about-page").get_all_records())
    about = get_tab_df(sheet, sheet_path_list, "about-page")
    for idx, about_row in about.iterrows():

        if not bool(about_row.use):  # 이 부분에서 False일 경우 건너뛰도록 수정
            continue

        elif about_row.type == "text":
            lines += [about_row.content, "\n" * 2]

        elif about_row.type == "sheet":
            name: str = about_row.content
            tab = get_tab_df(sheet, sheet_path_list, name)

            if len(tab.values) > 0:
                if name.title().lower() == 'latest news':
                    lines.append("## Latest News ([See all](/news))\n\n")
                    func_name = "_" + name.replace(" ", "_")
                    locals()[func_name](tab)
                    lines.append("\n")
                else:
                    lines.append(f"## {name.title()}\n\n")
                    func_name = "_" + name.replace(" ", "_")
                    locals()[func_name](tab)
                    lines.append("\n")

        else:
            raise ValueError

    open(out_dir, "w").writelines(lines)
    print("".join(lines))
    print(f"Saved at {out_dir}")

def build_about(sheet: Spreadsheet, sheet_path_list: List[str],
                out_dir="./_pages/about.md"):

    def _education(df: pd.DataFrame):
        for i, r in df.iterrows():
            dobj = datetime.strptime(r.date, "%Y-%m-%d")
            lines.append(f"- {r.degree}, *{r.institution}*, {dobj.strftime('%b %Y')}\n")
            if len(r.bullets) > 1:
                lines.append(f"  - {r.bullets}\n")       

    def _academic_services(df: pd.DataFrame):
        position_and_org_to_rs = defaultdict(lambda: defaultdict(list))
        for i, r in df.iterrows():
            position_and_org_to_rs[r.position][r.organization].append(r)
        for p, o_to_rs in position_and_org_to_rs.items():
            _o_ys = []
            for o, rs in o_to_rs.items():
                _years = [f"{r.year}" if r.url == "" else f"[{r.year}]({r.url})" for r in rs]
                _o_ys.append(f"{o} ({', '.join(_years)})")
            lines.append(f"- {p}: {', '.join(_o_ys)}\n")

    def _teaching_experiences(df: pd.DataFrame):
        course_to_rs = defaultdict(list)
        for i, r in df.iterrows():
            course_to_rs[r.course].append(r)
        for c, rs in course_to_rs.items():
            positions = [r.position for r in rs]
            positions = set(positions) if len(set(positions)) == 1 else positions
            head = ", ".join(positions)
            semesters = ", ".join(f"{r.semester}" if r.url == "" else f"[{r.semester}]({r.url})" for r in rs)
            notes = ", ".join(r.note for r in rs if r.note != "")
            if notes == "":
                lines.append(f"- {head} of {c} ({semesters})\n")
            else:
                lines.append(f"- {head} of {c} ({semesters}), *{notes}*\n")

    def _honors(df: pd.DataFrame):
        for i, r in df.iterrows():
            dobj = datetime.strptime(r.date, "%Y-%m-%d")
            if r.url == "":
                lines.append(f"- {r.title}, *{r.organization}*, {dobj.strftime('%Y')}\n")
            else:
                lines.append(f"- [{r.title}]({r.url}), *{r.organization}*, {dobj.strftime('%Y')}\n")
    
    def _latest_news(df: pd.DataFrame):
        for i, r in df.iterrows():
            if i < 3:
                dobj = datetime.strptime(r.date, "%Y-%m-%d")
                lines.append(f"- {r.icon} [{dobj.strftime('%b %Y')}] {r.title} \n")

    def _open_source_contributions(df: pd.DataFrame):
        for i, r in df.iterrows():
            lines.append(f"- [{r.title}]({r.url})\n")

    lines = []

    # about = pd.DataFrame(sheet.worksheet("about-page").get_all_records())
    about = get_tab_df(sheet, sheet_path_list, "about-page")
    for idx, about_row in about.iterrows():

        if not bool(about_row.use):
            continue

        elif about_row.type == "text":
            lines += [about_row.content, "\n" * 2]

        elif about_row.type == "sheet":
            name: str = about_row.content
            tab = get_tab_df(sheet, sheet_path_list, name)

            if len(tab.values) > 0:
                if name.title().lower() == 'latest news':
                    lines.append("## Latest News ([See all](/news))\n\n")
                else:
                    lines.append(f"## {name.title()}\n\n")
                func_name = "_" + name.replace(" ", "_")
                locals()[func_name](tab)
                lines.append("\n")

        else:
            raise ValueError

    open(out_dir, "w").writelines(lines)
    print("".join(lines))
    print(f"Saved at {out_dir}")


if __name__ == '__main__':

    __target__ = "all"
    __gsheet__ = "https://docs.google.com/spreadsheets/d/12iVffjLlb7bXynkc725MP97YRQNB3HgpWLYPFSUgWZY/edit?gid=34293519#gid=34293519"
    __path_1__ = "./Data for CV (Jieun Han).xlsx"

    # try:
    #     gc = gspread.oauth()
    #     sh = gc.open_by_url(__gsheet__)
    # except:
    #     gc, sh = None, None
    credentials_filename = './_build_contents/credential.json' 
    gc = gspread.service_account(filename=credentials_filename)
    sh = gc.open_by_url(__gsheet__)
    if __target__ == "about" or __target__ == "all":
        build_about(sheet=sh, sheet_path_list=[__path_1__])

    if __target__ == "latest news" or __target__ == "all":
        build_latest_news(sheet=sh, sheet_path_list=[__path_1__])

    if __target__ == "publications" or __target__ == "all":
        build_publications(sheet=sh, sheet_path_list=[__path_1__])

    if __target__ == "talks" or __target__ == "all":
        build_talks(sheet=sh, sheet_path_list=[__path_1__])